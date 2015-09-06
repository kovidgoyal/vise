#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2015, Kovid Goyal <kovid at kovidgoyal.net>

import os
import json
import weakref
import subprocess
import shlex
from contextlib import closing
from tempfile import NamedTemporaryFile
from threading import Thread
from gettext import gettext as _

from PyQt5.Qt import (
    QWebEngineView, QWebEnginePage, QSize, QNetworkRequest, QIcon,
    QApplication, QPixmap, pyqtSignal, QWebChannel, pyqtSlot, QObject,
    QGridLayout, QCheckBox, QLabel
)

from .auth import get_http_auth_credentials, get_proxy_auth_credentials
from .certs import cert_exceptions
from .message_box import question_dialog
from .popup import Popup
from .utils import Dialog, safe_disconnect

view_id = 0


class Alert(Dialog):  # {{{

    suppressed_alerts = set()

    def __init__(self, title, qurl, msg, parent):
        title = title or qurl.host() or qurl.toString()
        self.msg = msg
        self.key = qurl.toString()
        Dialog.__init__(self, _('Alert from') + ': ' + title, 'alert', parent)

    def setup_ui(self):
        self.l = l = QGridLayout(self)
        self.la = la = QLabel(self.msg)
        la.setWordWrap(True)
        l.addWidget(la, 0, 0, 1, -1)
        self.setMaximumWidth(self.parent().width())
        self.setMaximumHeight(self.parent().height())
        self.cb = cb = QCheckBox(_('&Suppress future alerts from this site'), self)
        cb.toggled.connect(lambda: cb.isChecked() and Alert.suppressed_alerts.add(self.key))
        l.addWidget(cb, 1, 0)
        l.addWidget(self.bb, 1, 1), self.bb.setStandardButtons(self.bb.Close)

    def sizeHint(self):
        ans = Dialog.sizeHint(self)
        ans.setWidth(min(self.maximumWidth(), ans.width() + 150))
        return ans
# }}}


def edit_text(pageref, text, eid):  # {{{
    editor = shlex.split(os.environ.get('EDITOR', 'gvim -f'))
    with NamedTemporaryFile(suffix='.txt') as f:
        f.write(text.encode('utf-8'))
        f.flush()
        ret = subprocess.Popen(editor + [f.name]).wait()
        if ret == 0:
            page = pageref()
            if page is not None:
                f.seek(0)
                text = f.read().decode('utf-8')
                page.runJavaScript('vise_set_editable_text(%s, %s)' % (
                    json.dumps(text), json.dumps(eid)))
# }}}


class Bridge(QObject):

    middle_clicked = pyqtSignal(object)
    focus_changed = pyqtSignal(object)

    @pyqtSlot(str)
    def middle_clicked_link(self, href):
        if href:
            self.middle_clicked.emit(href)

    @pyqtSlot(bool)
    def element_focused(self, is_text_input):
        self.focus_changed.emit(bool(is_text_input))

    @pyqtSlot(str, str)
    def edit_text(self, text, eid):
        pageref = weakref.ref(self.parent())
        t = Thread(name='EditText', target=edit_text, args=(pageref, text, eid))
        t.daemon = True
        t.start()

    def break_cycles(self):
        for s in 'middle_clicked focus_changed'.split():
            safe_disconnect(getattr(self, s))


class WebPage(QWebEnginePage):

    def __init__(self, profile, parent):
        QWebEnginePage.__init__(self, profile, parent)
        self.bridge = Bridge(self)
        self.channel = QWebChannel(self)
        self.setWebChannel(self.channel)
        self.channel.registerObject('bridge', self.bridge)
        self.authenticationRequired.connect(self.authentication_required)
        self.proxyAuthenticationRequired.connect(self.proxy_authentication_required)

    def javaScriptConsoleMessage(self, level, msg, linenumber, source_id):
        try:
            print('%s:%s: %s' % (source_id, linenumber, msg))
        except OSError:
            pass

    def certificateError(self, err):
        code = err.error()
        qurl = err.url()
        domain = qurl.host()
        if cert_exceptions.has_exception(domain, code):
            return True
        if not err.isOverridable():
            cert_exceptions.show_error(domain, err.errorDescription(), self.parent())
            return False
        return cert_exceptions.ask(domain, code, err.errorDescription(), self.parent())

    def authentication_required(self, qurl, authenticator):
        get_http_auth_credentials(qurl, authenticator, parent=self.parent())

    def proxy_authentication_required(self, qurl, authenticator, proxy_host):
        get_proxy_auth_credentials(qurl, authenticator, proxy_host, parent=self.parent())

    def javaScriptAlert(self, qurl, msg):
        key = qurl.toString()
        if key in Alert.suppressed_alerts:
            print('Suppressing alert from:', qurl.toString())
            return
        self.parent().raise_tab()
        Alert(self.title(), qurl, msg, self.parent()).exec_()

    def break_cycles(self):
        self.bridge.break_cycles()
        for s in ('authenticationRequired proxyAuthenticationRequired linkHovered featurePermissionRequested'
                  ' featurePermissionRequestCanceled windowCloseRequested').split():
            safe_disconnect(getattr(self, s))


class WebView(QWebEngineView):

    icon_changed = pyqtSignal(object)
    open_in_new_tab = pyqtSignal(object)
    loading_status_changed = pyqtSignal(object)
    focus_changed = pyqtSignal(object, object)
    link_hovered = pyqtSignal(object)
    window_close_requested = pyqtSignal(object)
    resized = pyqtSignal()
    moved = pyqtSignal()
    passthrough_changed = pyqtSignal(object, object)

    def __init__(self, profile, main_window):
        global view_id
        QWebEngineView.__init__(self, main_window)
        self.main_window = main_window
        self.create_page(profile)
        self.view_id = view_id
        view_id += 1
        self.iconUrlChanged.connect(self.icon_url_changed)
        self._icon_reply = None
        self.icon = QIcon()
        self._page.bridge.middle_clicked.connect(self.open_in_new_tab.emit)
        self._page.bridge.focus_changed.connect(self.on_focus_change)
        self.loadStarted.connect(lambda: self.loading_status_changed.emit(True))
        self.loadFinished.connect(lambda: self.loading_status_changed.emit(False))
        self._page.linkHovered.connect(self.link_hovered.emit)
        self._page.windowCloseRequested.connect(lambda: self.window_close_requested.emit(self))
        self.popup = Popup(self)
        self._page.featurePermissionRequested.connect(self.feature_permission_requested)
        self._page.featurePermissionRequestCanceled.connect(self.feature_permission_request_canceled)
        self.feature_permission_map = {}
        self.text_input_focused = False
        self._force_passthrough = False

    @property
    def force_passthrough(self):
        return self._force_passthrough

    @force_passthrough.setter
    def force_passthrough(self, val):
        self._force_passthrough = bool(val)
        self.passthrough_changed.emit(self._force_passthrough, self)

    def on_focus_change(self, is_text_input):
        self.text_input_focused = is_text_input
        self.focus_changed.emit(is_text_input, self)

    def feature_permission_requested(self, qurl, feature):
        key = (qurl.toString(), feature)
        what = {QWebEnginePage.Geolocation: _('current location'), QWebEnginePage.MediaAudioCapture: _('microphone'),
                QWebEnginePage.MediaVideoCapture: _('webcam'), QWebEnginePage.MediaAudioVideoCapture: _('microphone and webcam')
                }[feature]
        self.feature_permission_map[key] = self.popup(
            _('Grant this site access to your <b>%s</b>?') % what,
            lambda ok: self._page.setFeaturePermission(qurl, feature, (
                QWebEnginePage.PermissionGrantedByUser if ok else QWebEnginePage.PermissionDeniedByUser))
        )

    def feature_permission_request_canceled(self, qurl, feature):
        key = (qurl.toString(), feature)
        qid = self.feature_permission_map.pop(key, None)
        if qid is not None:
            self.popup.abort_question(qid)

    def resizeEvent(self, ev):
        self.resized.emit()
        return QWebEngineView.resizeEvent(self, ev)

    def moveEvent(self, ev):
        self.moved.emit()
        return QWebEngineView.moveEvent(self, ev)

    def break_cycles(self):
        self._page.break_cycles()
        for s in ('resized moved icon_changed open_in_new_tab loading_status_changed link_hovered'
                  ' loadStarted loadFinished window_close_requested focus_changed passthrough_changed').split():
            safe_disconnect(getattr(self, s))

    def create_page(self, profile):
        self._page = WebPage(profile, self)
        self.setPage(self._page)

    def sizeHint(self):
        return QSize(800, 600)

    def icon_url_changed(self, qurl):
        if qurl.isEmpty():
            self.icon_loaded()
            return
        self.icon = QIcon()
        f = QApplication.instance().disk_cache.data(qurl)
        if f is not None:
            with closing(f):
                raw = bytes(f.readAll())
                p = QPixmap()
                p.loadFromData(raw)
                if not p.isNull():
                    self.icon.addPixmap(p)

        req = QNetworkRequest(qurl)
        self._icon_reply = QApplication.instance().network_access_manager.get(req)
        self._icon_reply.setParent(self)
        self._icon_reply.finished.connect(self.icon_loaded)
        self.icon_changed.emit(self.icon)

    def icon_loaded(self):
        self.icon = QIcon()
        if self._icon_reply is not None:
            if self._icon_reply.error() == self._icon_reply.NoError:
                data = self._icon_reply.readAll()
                pixmap = QPixmap()
                pixmap.loadFromData(data)
                self.icon.addPixmap(pixmap)
                self._icon_reply.deleteLater()
                self._icon_reply = None
            else:
                QApplication.instance().error('Failed to download favicon from %s with error: %s' % (
                    self._icon_reply.url().toString(), self._icon_reply.errorString()))
        self.icon_changed.emit(self.icon)

    def raise_tab(self):
        self.main_window.raise_tab(self)

    def createWindow(self, window_type):
        if window_type in (QWebEnginePage.WebBrowserTab, QWebEnginePage.WebBrowserWindow):
            site = '<b>%s</b>' % self.title() or self.url().host() or self.url().toString()
            if question_dialog(self, _('Allow new window?'), _(
                    'The site {0} wants to open a new tab, allow it?').format(site)):
                return self.main_window.get_tab_for_load(in_current_tab=False)
