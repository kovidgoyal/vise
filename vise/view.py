#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2015, Kovid Goyal <kovid at kovidgoyal.net>

import os
import json
import weakref
import subprocess
import shlex
from time import monotonic
from base64 import standard_b64encode
from tempfile import NamedTemporaryFile
from threading import Thread
from gettext import gettext as _
from functools import partial
from itertools import count

from PyQt5.Qt import (
    QWebEngineView, QWebEnginePage, QSize, QApplication, pyqtSignal,
    QGridLayout, QCheckBox, QLabel, Qt, QWebEngineScript, QUrl, QPageSize,
    QPageLayout, QMarginsF
)

from .auth import get_http_auth_credentials, get_proxy_auth_credentials
from .certs import cert_exceptions
from .communicate import python_to_js, js_to_python, connect_signal
from .config import misc_config
from .constants import FOLLOW_LINK_KEY_MAP
from .downloads import get_download_dir
from .message_box import question_dialog
from .places import places
from .popup import Popup
from .utils import Dialog, safe_disconnect, ascii_lowercase, icon_to_data, open_local_file
from .passwd.db import password_db, key_from_url, password_exclusions
from .settings import gprefs
from .site_permissions import site_permissions

view_id = count()
certificate_error_domains = set()


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


def edit_text(viewref, text, frame_id, eid):  # {{{
    editor = shlex.split(misc_config('editor', default=os.environ.get('EDITOR', 'gvim -f')))
    with NamedTemporaryFile(suffix='.txt') as f:
        f.write(text.encode('utf-8'))
        f.flush()
        ret = subprocess.Popen(editor + [f.name]).wait()
        if ret == 0:
            f.seek(0)
            text = f.read().decode('utf-8')
            # This signal can only be emitted in the GUI thread as it is
            # connected to JavaScript code
            view = viewref()
            if view is not None:
                view.set_editable_text_in_gui_thread.emit(text, frame_id, eid)
# }}}


class WebPage(QWebEnginePage):

    poll_for_messages = pyqtSignal()

    def __init__(self, profile, parent):
        QWebEnginePage.__init__(self, profile, parent)
        self.authenticationRequired.connect(self.authentication_required)
        self.proxyAuthenticationRequired.connect(self.proxy_authentication_required)
        self.callbacks = {'vise_downloads_page': (self.downloads_callback, (), {})}
        self.poll_for_messages.connect(self.check_for_messages_from_js, type=Qt.QueuedConnection)

    def register_callback(self, name, func, *args, **kw):
        self.callbacks[name] = (func, args, kw)

    def downloads_callback(self, *args, **kw):
        return QApplication.instance().downloads.callback(*args, **kw)

    def check_for_messages_from_js(self):
        self.runJavaScript('try { window.get_messages_from_javascript() } catch(TypeError) {}',
                           QWebEngineScript.ApplicationWorld, self.messages_received_from_js)

    def messages_received_from_js(self, messages):
        if messages and messages != '[]':
            for msg in json.loads(messages):
                mtype = msg['type']
                if mtype == 'callback':
                    self.called_back(msg['name'], msg['data'])
                elif mtype == 'js_to_python':
                    js_to_python(self, msg['name'], msg['args'])
                else:
                    print('Unknown message type %s received from javascript' % mtype)

    def called_back(self, name, data):
        try:
            func, args, kw = self.callbacks[name]
        except KeyError:
            pass
        else:
            return func(self.view(), data, *args, **kw)
        raise KeyError('No callback named %r is registered' % name)

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
            certificate_error_domains.add(domain)
            return True
        if not err.isOverridable():
            cert_exceptions.show_error(domain, err.errorDescription(), self.parent())
            return False
        allow = cert_exceptions.ask(domain, code, err.errorDescription(), self.parent())
        if allow:
            certificate_error_domains.add(domain)
        return allow

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
        self.callbacks.clear()
        for s in ('authenticationRequired proxyAuthenticationRequired linkHovered featurePermissionRequested'
                  ' featurePermissionRequestCanceled fullScreenRequested windowCloseRequested poll_for_messages').split():
            safe_disconnect(getattr(self, s))

    def acceptNavigationRequest(self, qurl, navtype, is_main_frame):
        try:
            places.on_visit(qurl, navtype, is_main_frame)
        except Exception:
            import traceback
            traceback.print_exc()
        return True


class WebView(QWebEngineView):

    icon_changed = pyqtSignal(object)
    loading_status_changed = pyqtSignal(object)
    focus_changed = pyqtSignal(object, object)
    link_hovered = pyqtSignal(object)
    window_close_requested = pyqtSignal(object)
    resized = pyqtSignal()
    moved = pyqtSignal()
    passthrough_changed = pyqtSignal(object, object)
    title_changed = pyqtSignal(object)
    toggle_full_screen = pyqtSignal(object)
    set_editable_text_in_gui_thread = pyqtSignal(str, int, str)

    def __init__(self, profile, main_window):
        QWebEngineView.__init__(self, main_window)
        self.middle_click_soon = 0
        self.setAttribute(Qt.WA_DeleteOnClose)  # needed otherwise object is not deleted on close which means, it keeps running
        self.setMinimumWidth(300)
        self.follow_link_pending = None
        self.setFocusPolicy(Qt.ClickFocus | Qt.WheelFocus)
        self.pending_unserialize = None
        self.main_window = main_window
        self.create_page(profile)
        self.view_id = next(view_id)
        self.iconChanged.connect(self.on_icon_changed, type=Qt.QueuedConnection)
        self.set_editable_text_in_gui_thread.connect(self.set_editable_text, type=Qt.QueuedConnection)
        self.loadStarted.connect(self.load_started)
        self.loadFinished.connect(self.load_finished)
        self._page.linkHovered.connect(self.link_hovered.emit)
        self._page.windowCloseRequested.connect(lambda: self.window_close_requested.emit(self))
        self.popup = Popup(self)
        self._page.featurePermissionRequested.connect(self.feature_permission_requested)
        self._page.featurePermissionRequestCanceled.connect(self.feature_permission_request_canceled)
        self._page.fullScreenRequested.connect(self.full_screen_requested)
        self.feature_permission_map = {}
        self.text_input_focused = False
        self._force_passthrough = False
        self.titleChanged.connect(self.on_title_change)
        self.renderProcessTerminated.connect(self.render_process_terminated)

    def render_process_terminated(self, termination_type, exit_code):
        if termination_type == QWebEnginePage.CrashedTerminationStatus:
            from .message_box import error_dialog
            error_dialog(self.parent(), _('Render process crashed'), _(
                'The render process crashed while displaying the URL: {0} with exit code: {1}').format(
                    self.url().toString(), exit_code), show=True)
        elif termination_type == QWebEnginePage.AbnormalTerminationStatus:
            from .message_box import error_dialog
            error_dialog(self.parent(), _('Render process terminated'), _(
                'The render process exited abnormally while displaying the URL: {0} with exit code: {1}').format(
                    self.url().toString(), exit_code), show=True)

    def load_started(self):
        self.text_input_focused = False
        self.focus_changed.emit(False, self)
        self.loading_status_changed.emit(True)

    def load_finished(self):
        if self.pending_unserialize is not None:
            state, self.pending_unserialize = self.pending_unserialize, None
            self._page.runJavaScript('window.scrollTo(%d, %d)' % (state['x'], state['y']))
        self.loading_status_changed.emit(False)
        u, ru = self._page.url(), self._page.requestedUrl()
        if u != ru:
            if u.toString() == 'https' + ru.toString()[4:]:
                places.merge_https_places(ru)

    def on_title_change(self, title):
        from .settings import TITLE_TOKEN
        if title != TITLE_TOKEN:
            try:
                places.on_title_change(self.url(), title)
            except Exception:
                import traceback
                traceback.print_exc()
            self.title_changed.emit(title)
        self._page.poll_for_messages.emit()

    def on_icon_changed(self, icon):
        icurl = self.iconUrl()
        QApplication.instance().save_favicon_in_cache(icon, icurl)
        places.on_favicon_change(self.url(), icurl)
        self.icon_changed.emit(icon)

    def register_callback(self, name, func, *args, **kw):
        self._page.register_callback(name, func, *args, **kw)

    @property
    def force_passthrough(self):
        return self._force_passthrough

    @force_passthrough.setter
    def force_passthrough(self, val):
        self._force_passthrough = bool(val)
        self.passthrough_changed.emit(self._force_passthrough, self)

    @connect_signal('element_focused')
    def on_focus_change(self, is_text_input):
        self.text_input_focused = is_text_input
        self.focus_changed.emit(is_text_input, self)

    def exit_text_input(self):
        python_to_js(self, 'exit_text_input')
        self.text_input_focused = False
        self.focus_changed.emit(False, self)

    @connect_signal('copy_to_clipboard')
    def copy_to_clipboard(self, text):
        QApplication.clipboard().setText(text)

    def feature_permission_requested(self, qurl, feature):
        key = (qurl.toString(), feature)
        what = {QWebEnginePage.Geolocation: _('current location'), QWebEnginePage.MediaAudioCapture: _('microphone'),
                QWebEnginePage.MediaVideoCapture: _('webcam'), QWebEnginePage.MediaAudioVideoCapture: _('microphone and webcam')
                }[feature]
        self.feature_permission_map[key] = self.popup(
            _('Grant this site access to your <b>%s</b>?') % what,
            lambda ok, during_shutdown: self.page().setFeaturePermission(qurl, feature, (
                QWebEnginePage.PermissionGrantedByUser if ok else QWebEnginePage.PermissionDeniedByUser))
        )

    def feature_permission_request_canceled(self, qurl, feature):
        key = (qurl.toString(), feature)
        qid = self.feature_permission_map.pop(key, None)
        if qid is not None:
            self.popup.abort_question(qid)

    def exit_full_screen(self):
        self._page.triggerAction(self._page.ExitFullScreen)

    def full_screen_requested(self, req):
        if True or site_permissions.has_permission(req.origin(), 'full_screen'):
            # Asking the user is disabled because of: https://bugreports.qt.io/browse/QTBUG-55064
            # The next release of PyQt will allow cloning of the request
            # objects (SIP v 4.19)
            req.accept()
            self.toggle_full_screen.emit(req.toggleOn())
        else:
            callback = partial(self.on_full_screen_decision, req)
            q = _('Allow %s to switch to full screen?')
            if not req.toggleOn():
                q = _('Allow %s to switch out of full screen?')
            self.popup(q % ascii_lowercase(req.origin().host()),
                       callback, extra_buttons={_('Always'): 'permanent'})

    def on_full_screen_decision(self, req, ok, during_shutdown):
        if ok:
            site_permissions.add_permission(req.origin(), 'full_screen', permanent=ok == 'permanent')
            req.accept()
            if not during_shutdown:
                self.toggle_full_screen.emit(req.toggleOn())
        else:
            req.reject()

    def resizeEvent(self, ev):
        self.resized.emit()
        return QWebEngineView.resizeEvent(self, ev)

    def moveEvent(self, ev):
        self.moved.emit()
        return QWebEngineView.moveEvent(self, ev)

    def break_cycles(self):
        self.popup.break_cycles()
        self._page.break_cycles()
        for s in ('resized moved icon_changed loading_status_changed link_hovered urlChanged iconChanged renderProcessTerminated'
                  ' loadStarted loadFinished window_close_requested focus_changed passthrough_changed toggle_full_screen').split():
            safe_disconnect(getattr(self, s))

    def create_page(self, profile):
        self._page = WebPage(profile, self)
        self.setPage(self._page)

    def sizeHint(self):
        return QSize(800, 600)

    def raise_tab(self):
        self.main_window.raise_tab(self)

    @connect_signal('middle_click_soon')
    def expecting_middle_click(self):
        self.middle_click_soon = monotonic()

    def createWindow(self, window_type):
        site = '<b>%s</b>' % self.title() or self.url().host() or self.url().toString()
        now = monotonic()
        if window_type == QWebEnginePage.WebBrowserBackgroundTab or now - self.middle_click_soon < 2 or question_dialog(
                self, _('Allow new window?'), _('The site {0} wants to open a new tab, allow it?').format(site)):
            return self.main_window.get_child_tab_for_load()

    def runjs(self, src, callback=None, world_id=QWebEngineScript.ApplicationWorld):
        if callback is not None:
            self._page.runJavaScript(src, world_id, callback)
        else:
            self._page.runJavaScript(src, world_id)

    def js_func(self, name, *args, callback=None, world_id=QWebEngineScript.ApplicationWorld):
        func = '%s(%s)' % (name, ','.join(map(lambda x: json.dumps(x, ensure_ascii=False), args)))
        self.runjs(func, callback=callback, world_id=world_id)

    def save_page(self, path=None):
        from .downloads import save_page_path_map
        self._page.triggerAction(self._page.SavePage)
        save_page_path_map[self.url().toString()] = path

    def print_page(self, path=None):
        if not path:
            path = os.path.join(get_download_dir(), self.title())
        if not path.lower().endswith('.pdf'):
            path += '.pdf'
        size = QPageSize(getattr(QPageSize, misc_config('paper_size', 'A4')))
        layout = QPageLayout(size, QPageLayout.Portrait, QMarginsF(
            float(misc_config('margin_left', 36)), float(misc_config('margin_top', 36)),
            float(misc_config('margin_right', 36)), float(misc_config('margin_bottom', 36))))
        self._page.printToPdf(partial(self.print_done, path), layout)

    def print_done(self, path, data):
        with open(path, 'wb') as f:
            f.write(data.data())
        open_local_file(path)

    @connect_signal('login_form_submitted_in_page')
    def on_login_form_submit(self, url, username, password):
        if not username or not password:
            return
        key = key_from_url(url)
        if password_exclusions.get(key, False):
            return
        if not QApplication.instance().ask_for_master_password(self):
            return
        if key not in password_db:
            def store_passwd(ok, during_shutdown):
                if ok == 'never':
                    exclude = gprefs.get('never-store-password-for', {})
                    exclude[key] = True
                    password_exclusions.set(key, True)
                elif ok and not during_shutdown:
                    QApplication.instance().store_password(url, username, password)
            self.popup(_('Remember password for: {0}?').format(key),
                       store_passwd, {_('Never'): 'never'})
        else:
            QApplication.instance().store_password(url, username, password)

    @connect_signal()
    def login_form_found_in_page(self, url):
        self.on_login_form_found(url, False)

    @connect_signal()
    def url_for_current_login_form(self, url):
        self.on_login_form_found(url, True)

    def get_login_credentials(self, url):
        if not QApplication.instance().ask_for_master_password(self):
            return
        if password_db.join():
            key = key_from_url(url)
            accounts = password_db.get_accounts(key)
            if accounts:
                return accounts[0]

    def on_login_form_found(self, url, is_current_form):
        ac = self.get_login_credentials(url)
        if ac is not None:
            python_to_js(self, 'autofill_login_form', url, ac['username'], ac['password'], ac['autologin'], is_current_form)

    def find_text(self, text, callback=None, forward=True):
        flags = QWebEnginePage.FindFlags(0) if forward else QWebEnginePage.FindBackward
        self.find_text_data = [text, callback]
        if callback is None:
            self._page.findText(text, flags)
        else:
            self._page.findText(text, flags, self._find_text_intermediate)

    def _find_text_intermediate(self, found):
        text, callback = self.find_text_data
        self.find_text_data = [None, None]
        if callback is not None:
            callback(text, found)

    def serialize_state(self, include_favicon=False):
        pos = self._page.scrollPosition()
        sz = self._page.contentsSize()
        ans = {
            'x': pos.x(), 'y': pos.y(),
            'width': sz.width(), 'height': sz.height(),
            'zoom_factor': self.zoom_factor,
            'title': self.title(),
            'url': self._page.url().toString(),
            'audio_muted': self._page.isAudioMuted(),
            'view_id': self.view_id,
        }
        if include_favicon:
            ic = icon_to_data(self.icon())
            if ic:
                ans['favicon'] = 'data:image/png;base64,' + standard_b64encode(ic).decode('ascii')

        return ans

    def unserialize_state(self, state):
        self.load(QUrl(state['url']))
        self.setZoomFactor(state['zoom_factor'])
        self._page.setAudioMuted(state['audio_muted'])
        self.pending_unserialize = state

    @property
    def zoom_factor(self):
        return self.zoomFactor()

    @zoom_factor.setter
    def zoom_factor(self, val):
        self.setZoomFactor(max(0.25, min(val, 5.0)))

    def start_follow_link(self, action):
        self.follow_link_pending = action
        python_to_js(self, 'start_follow_link', action)

    def follow_link(self, key):
        jkey = FOLLOW_LINK_KEY_MAP.get(key)
        if jkey is not None:
            python_to_js(self, 'follow_link', jkey)
            return True

    @connect_signal()
    def link_followed(self, ok, text):
        if ok:
            self.follow_link_pending = None
        else:
            if text == '|escape':
                self.follow_link_pending = None
                return
            self.main_window.show_status_message(_('No match for %s!') % text, 5000, 'error')

    def set_editable_text(self, *args):
        python_to_js(self, 'set_editable_text', *args)

    @connect_signal()
    def edit_text(self, text, frame_id, eid):
        ref = weakref.ref(self)
        t = Thread(name='EditText', target=edit_text, args=(ref, text, frame_id, eid))
        t.daemon = True
        t.start()
