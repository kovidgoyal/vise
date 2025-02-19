#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2015, Kovid Goyal <kovid at kovidgoyal.net>

import json
import os
import shlex
import subprocess
import weakref
from base64 import standard_b64encode
from functools import partial
from gettext import gettext as _
from itertools import count
from tempfile import NamedTemporaryFile
from threading import Thread
from time import monotonic

from PyQt6 import sip
from PyQt6.QtCore import QMarginsF, QSize, Qt, QUrl, pyqtSignal, QEvent
from PyQt6.QtGui import QKeyEvent, QPageLayout, QPageSize
from PyQt6.QtWebEngineCore import QWebEnginePage, QWebEngineScript
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QApplication, QCheckBox, QGridLayout, QLabel, QDialogButtonBox

from .auth import get_http_auth_credentials, get_proxy_auth_credentials
from .certs import cert_exceptions
from .communicate import connect_signal, js_to_python, python_to_js
from .config import misc_config
from .constants import FOLLOW_LINK_KEY_MAP
from .dev_tools import DevTools
from .downloads import get_download_dir
from .message_box import question_dialog
from .passwd.db import key_from_url, password_db, password_exclusions
from .places import places
from .popup import Popup
from .settings import gprefs
from .site_permissions import site_permissions
from .utils import (Dialog, ascii_lowercase, icon_to_data, open_local_file,
                    safe_disconnect)

view_id = count()
certificate_error_domains = set()


class Alert(Dialog):  # {{{

    suppressed_alerts: set[str] = set()

    def __init__(self, title, qurl, msg, parent):
        title = title or qurl.host() or qurl.toString()
        self.msg = msg
        self.key = qurl.toString()
        Dialog.__init__(self, _('Alert from') + ': ' + title, 'alert', parent)

    def setup_ui(self):
        self.lay = lay = QGridLayout(self)
        self.la = la = QLabel(self.msg)
        la.setWordWrap(True)
        lay.addWidget(la, 0, 0, 1, -1)
        self.setMaximumWidth(self.parent().width())
        self.setMaximumHeight(self.parent().height())
        self.cb = cb = QCheckBox(_('&Suppress future alerts from this site'), self)
        cb.toggled.connect(self.suppress_toggled)
        lay.addWidget(cb, 1, 0)
        lay.addWidget(self.bb, 1, 1), self.bb.setStandardButtons(QDialogButtonBox.StandardButton.Close)

    def suppress_toggled(self):
        if self.cb.isChecked():
            Alert.suppressed_alerts.add(self.key)

    def sizeHint(self):
        ans = Dialog.sizeHint(self)
        ans.setWidth(min(self.maximumWidth(), ans.width() + 150))
        return ans
# }}}


def edit_text(viewref, text, frame_id, eid):  # {{{
    defedit = os.environ.get('VISUAL', os.environ.get('EDITOR', 'vim'))
    defedit = 'kitty ' + defedit
    editor = shlex.split(misc_config('editor', default=defedit))
    with NamedTemporaryFile(prefix='vise-edit-file-', suffix='.txt', delete=False) as f:
        f.write(text.encode('utf-8'))
    try:
        ret = subprocess.Popen(editor + [f.name]).wait()
        if ret == 0:
            with open(f.name, 'rb') as f:
                new_text = f.read().decode('utf-8')
            if new_text != text:
                view = viewref()
                if view is not None:
                    view.set_editable_text_in_gui_thread.emit(new_text, frame_id, eid)
    finally:
        os.remove(f.name)
# }}}


class WebPage(QWebEnginePage):

    poll_for_messages = pyqtSignal()

    def __init__(self, profile, parent):
        QWebEnginePage.__init__(self, profile, parent)
        self.authenticationRequired.connect(self.authentication_required)
        self.proxyAuthenticationRequired.connect(self.proxy_authentication_required)
        self.callbacks = {'vise_downloads_page': (self.downloads_callback, (), {})}
        self.poll_for_messages.connect(self.check_for_messages_from_js, type=Qt.ConnectionType.QueuedConnection)
        self.certificateError.connect(self.on_certificate_error)

    def register_callback(self, name, func, *args, **kw):
        self.callbacks[name] = (func, args, kw)

    def downloads_callback(self, *args, **kw):
        return QApplication.instance().downloads.callback(*args, **kw)

    def check_for_messages_from_js(self):
        self.runJavaScript('try { window.get_messages_from_javascript() } catch(TypeError) {}',
                           QWebEngineScript.ScriptWorldId.ApplicationWorld, self.messages_received_from_js)

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
            return func(self.parent(), data, *args, **kw)
        raise KeyError('No callback named %r is registered' % name)

    def javaScriptConsoleMessage(self, level, msg, linenumber, source_id):
        try:
            print('%s:%s: %s' % (source_id, linenumber, msg))
        except OSError:
            pass

    def on_certificate_error(self, err):
        code = err.type()
        qurl = err.url()
        domain = qurl.host()
        if cert_exceptions.has_exception(domain, code):
            certificate_error_domains.add(domain)
            err.acceptCertificate()
            return
        if not err.isOverridable():
            cert_exceptions.show_error(domain, err.description(), self.parent())
            err.rejectCertificate()
            return
        err.defer()
        allow = cert_exceptions.ask(domain, code, err.description(), self.parent())
        if allow:
            certificate_error_domains.add(domain)
            err.acceptCertificate()
        else:
            err.rejectCertificate()

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
        Alert(self.title(), qurl, msg, self.parent()).exec()

    def break_cycles(self):
        self.callbacks.clear()
        for s in ('authenticationRequired proxyAuthenticationRequired linkHovered featurePermissionRequested'
                  ' featurePermissionRequestCanceled fullScreenRequested windowCloseRequested quotaRequested'
                  ' poll_for_messages audioMutedChanged certificateError').split():
            safe_disconnect(getattr(self, s))
        # Without the next two lines we get a crash on exit with Qt 5.8.0
        self.setParent(None)
        self.deleteLater()

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
    link_hovered = pyqtSignal(object, object)
    window_close_requested = pyqtSignal(object)
    resized = pyqtSignal()
    moved = pyqtSignal()
    passthrough_changed = pyqtSignal(object, object)
    title_changed = pyqtSignal(object)
    toggle_full_screen = pyqtSignal(object)
    set_editable_text_in_gui_thread = pyqtSignal(str, int, str)
    dev_tools_requested = pyqtSignal()
    audio_muted_changed = pyqtSignal(bool)

    def __init__(self, profile, main_window):
        QWebEngineView.__init__(self, main_window)
        self.host_widget = None
        self.middle_click_soon = 0
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)  # needed otherwise object is not deleted on close which means, it keeps running
        self.setMinimumWidth(300)
        self.follow_link_pending = None
        self.setFocusPolicy(Qt.FocusPolicy(Qt.FocusPolicy.ClickFocus.value | Qt.FocusPolicy.WheelFocus.value))
        self.pending_unserialize = None
        self.main_window = main_window
        self.create_page(profile)
        self.view_id = next(view_id)
        self.iconChanged.connect(self.on_icon_changed, type=Qt.ConnectionType.QueuedConnection)
        self.set_editable_text_in_gui_thread.connect(self.set_editable_text, type=Qt.ConnectionType.QueuedConnection)
        self.loadStarted.connect(self.load_started)
        self.loadProgress.connect(self.load_progress)
        self.loadFinished.connect(self.load_finished)
        self._page.linkHovered.connect(self.on_link_hovered)
        self._page.windowCloseRequested.connect(self.on_window_close_requested)
        self.popup = Popup(self)
        self._page.featurePermissionRequested.connect(self.feature_permission_requested)
        self._page.featurePermissionRequestCanceled.connect(self.feature_permission_request_canceled)
        self._page.quotaRequested.connect(self.quota_requested)
        self._page.fullScreenRequested.connect(self.full_screen_requested)
        self.feature_permission_map = {}
        self.text_input_focused = False
        self.loading_in_progress = False
        self._force_passthrough = False
        self.titleChanged.connect(self.on_title_change)
        self.renderProcessTerminated.connect(self.render_process_terminated)
        self.callback_on_save_edit_text_node = None
        self._dev_tools = None
        self._pending_anchor = False

    @property
    def muted(self):
        return self._page.isAudioMuted()

    @muted.setter
    def muted(self, val):
        val = bool(val)
        if val != self.muted:
            self._page.setAudioMuted(bool(val))
            self.audio_muted_changed.emit(val)

    def on_link_hovered(self, href):
        self.link_hovered.emit(self, href)

    def on_window_close_requested(self):
        self.window_close_requested.emit(self)

    def on_display_in_stack(self):
        # Workaround for https://bugreports.qt.io/browse/QTBUG-69838
        if self._pending_anchor:
            self._pending_anchor = False
            self.runjs('''
            (function() {
                var h = location.hash;
                location.hash = '';
                location.hash = h;
            }());''')

    def render_process_terminated(self, termination_type, exit_code):
        if termination_type == QWebEnginePage.RenderProcessTerminationStatus.CrashedTerminationStatus:
            from .message_box import error_dialog
            error_dialog(self.parent(), _('Render process crashed'), _(
                'The render process crashed while displaying the URL: {0} with exit code: {1}').format(
                    self.url().toString(), exit_code), show=True)
        elif termination_type == QWebEnginePage.RenderProcessTerminationStatus.AbnormalTerminationStatus:
            from .message_box import error_dialog
            error_dialog(self.parent(), _('Render process terminated'), _(
                'The render process exited abnormally while displaying the URL: {0} with exit code: {1}').format(
                    self.url().toString(), exit_code), show=True)

    @property
    def dev_tools(self):
        if self._dev_tools is None:
            self._dev_tools = DevTools(self)
            self._dev_tools.set_inspected_view(self)
        return self._dev_tools

    @property
    def dev_tools_enabled(self):
        return self._dev_tools is not None

    def close_dev_tools(self):
        if self._dev_tools is not None:
            self._dev_tools.set_inspected_view()
            self._dev_tools.setParent(None)
            self._dev_tools.deleteLater()
            self._dev_tools = None

    @property
    def is_showing_internal_content(self):
        return self._page.url().scheme() == 'vise'

    def load_started(self):
        self.loading_in_progress = True
        self.loading_status_changed.emit(True)

    def load_progress(self, val):
        if val == 100 and self.loading_in_progress:
            # This hack is needed because of as of Qt 5.10 loadFinished() is
            # not reliable, it is not called for some page loads
            self.load_finished(True)

    def load_finished(self, ok):
        if not self.loading_in_progress:
            return
        self.loading_in_progress = False
        if self.pending_unserialize is not None:
            state, self.pending_unserialize = self.pending_unserialize, None
            self.scroll_position = (state['x'], state['y'])
        else:
            if not self.isVisible() and self._page.url().hasFragment():
                self._pending_anchor = True
        self.loading_status_changed.emit(False)
        u, ru = self._page.url(), self._page.requestedUrl()
        if u != ru:
            if u.toString() == 'https' + ru.toString()[4:]:
                places.merge_https_places(ru)

    @property
    def scroll_position(self):
        pos = self._page.scrollPosition()
        return pos.x(), pos.y()

    @scroll_position.setter
    def scroll_position(self, val):
        x, y = val
        factor = self.devicePixelRatioF()
        x, y = int(x / factor), int(y / factor)
        self.runjs(f'window.scrollTo({x}, {y})')

    def on_title_change(self, title):
        from .settings import TITLE_TOKEN
        if title != TITLE_TOKEN:
            try:
                places.on_title_change(self.url(), title)
            except Exception:
                import traceback
                traceback.print_exc()
            self.title_changed.emit(title)
        try:
            self._page.poll_for_messages.emit()
        except RuntimeError:
            pass  # happens if page is deleted

    def on_icon_changed(self, icon):
        icurl = self.iconUrl()
        if not icon.isNull():
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
        if not feature:
            return
        key = (qurl.toString(), feature)
        what = {
            QWebEnginePage.Feature.Notifications: _('notifications'),
            QWebEnginePage.Feature.Geolocation: _('current location'),
            QWebEnginePage.Feature.MediaAudioCapture: _('microphone'),
            QWebEnginePage.Feature.MediaVideoCapture: _('webcam'),
            QWebEnginePage.Feature.MediaAudioVideoCapture: _('microphone and webcam'),
            QWebEnginePage.Feature.MouseLock: _('mouse lock'),
            QWebEnginePage.Feature.DesktopVideoCapture: _('desktop video capture'),
            QWebEnginePage.Feature.DesktopAudioVideoCapture: _('desktop audio/video capture'),
            QWebEnginePage.Feature.ClipboardReadWrite: _('clipboard read/write'),
        }[feature]
        self.feature_permission_map[key] = self.popup(
            _('Grant this site access to your <b>%s</b>?') % what,
            lambda ok, during_shutdown: self.page().setFeaturePermission(qurl, feature, (
                QWebEnginePage.PermissionPolicy.PermissionGrantedByUser if ok else QWebEnginePage.PermissionPolicy.PermissionDeniedByUser))
        )

    def feature_permission_request_canceled(self, qurl, feature):
        key = (qurl.toString(), feature)
        qid = self.feature_permission_map.pop(key, None)
        if qid is not None:
            self.popup.abort_question(qid)

    def quota_requested(self, request):
        self.popup(
            _('Grant this site access to <b>persistent storage</b> of {}?'),
            lambda ok, during_shutdown: request.accept() if ok else request.reject()
        )

    def exit_full_screen(self):
        self._page.triggerAction(QWebEnginePage.WebAction.ExitFullScreen)

    def full_screen_requested(self, req):
        # Cannot accept this asynchronously in python, see
        # https://bugreports.qt.io/browse/QTBUG-55064
        req.accept()
        if site_permissions.has_permission(req.origin(), 'full_screen'):
            self.toggle_full_screen.emit(req.toggleOn())
        else:
            callback = partial(self.on_full_screen_decision, req.origin(), req.toggleOn())
            q = _('Allow %s to switch to full screen?')
            if not req.toggleOn():
                q = _('Allow %s to switch out of full screen?')
            self.popup(q % ascii_lowercase(req.origin().host()),
                       callback, extra_buttons={_('Always'): 'permanent'})

    def on_full_screen_decision(self, origin, toggle_on, ok, during_shutdown):
        if ok:
            site_permissions.add_permission(origin, 'full_screen', permanent=ok == 'permanent')
            if not during_shutdown:
                self.toggle_full_screen.emit(toggle_on)

    def resizeEvent(self, ev):
        self.resized.emit()
        return QWebEngineView.resizeEvent(self, ev)

    def moveEvent(self, ev):
        self.moved.emit()
        return QWebEngineView.moveEvent(self, ev)

    def break_cycles(self):
        self.close_dev_tools()
        self.host_widget = None
        self.callback_on_save_edit_text_node = None
        self.popup.break_cycles()
        self._page.break_cycles()
        for s in ('resized moved icon_changed loading_status_changed link_hovered urlChanged iconChanged iconUrlChanged renderProcessTerminated'
                  ' loadStarted loadFinished window_close_requested focus_changed passthrough_changed toggle_full_screen dev_tools_requested').split():
            safe_disconnect(getattr(self, s))

    def create_page(self, profile):
        self._page = WebPage(profile, self)
        self.setPage(self._page)

    def sizeHint(self):
        return QSize(800, 600)

    def raise_tab(self):
        self.main_window.show_tab(self)

    @connect_signal('middle_click_soon')
    def expecting_middle_click(self):
        self.middle_click_soon = monotonic()

    def createWindow(self, window_type):
        site = '<b>%s</b>' % self.title() or self.url().host() or self.url().toString()
        now = monotonic()
        if window_type == QWebEnginePage.WebWindowType.WebBrowserBackgroundTab or now - self.middle_click_soon < 2 or question_dialog(
                self, _('Allow new window?'), _('The site {0} wants to open a new tab, allow it?').format(site)):
            return self.main_window.get_child_tab_for_load()

    def runjs(self, src, callback=None, world_id=QWebEngineScript.ScriptWorldId.ApplicationWorld):
        if callback is not None:
            self._page.runJavaScript(src, world_id, callback)
        else:
            self._page.runJavaScript(src, world_id)

    def js_func(self, name, *args, callback=None, world_id=QWebEngineScript.ScriptWorldId.ApplicationWorld):
        func = '%s(%s)' % (name, ','.join(map(lambda x: json.dumps(x, ensure_ascii=False), args)))
        self.runjs(func, callback=callback, world_id=world_id)

    def save_page(self, path=None):
        from .downloads import save_page_path_map
        self._page.triggerAction(QWebEnginePage.WebAction.SavePage)
        save_page_path_map[self.url().toString()] = path

    def print_page(self, path=None):
        if not path:
            path = os.path.join(get_download_dir(), self.title())
        if not path.lower().endswith('.pdf'):
            path += '.pdf'
        size = QPageSize(getattr(QPageSize, misc_config('paper_size', 'A4')))
        layout = QPageLayout(size, QPageLayout.Orientation.Portrait, QMarginsF(
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
        self.on_login_form_found(url, True)

    @connect_signal()
    def url_for_current_login_form(self, url):
        self.on_login_form_found(url, True)

    def get_login_credentials(self, url):
        # return {'password': 'testpw', 'autologin': False, 'username': 'testuser', 'notes': None}
        if not QApplication.instance().ask_for_master_password(self):
            return
        if password_db.join():
            key = key_from_url(url)
            accounts = password_db.get_accounts(key)
            if accounts:
                return accounts[0]

    def event(self, event):
        if event.type() == QEvent.Type.ChildPolished:
            child = event.child()
            if 'QQuickWidget' in child.metaObject().className():
                self.host_widget = child
        return QWebEngineView.event(self, event)

    def send_text_using_keys(self, text):
        if self.host_widget is not None and not sip.isdeleted(self.host_widget):
            self.host_widget.setFocus(Qt.FocusReason.OtherFocusReason)
            with QApplication.instance().key_filter.disable_filtering:
                for ch in text:
                    key = getattr(Qt, f'Key_{ch.upper()}', Qt.Key.Key_A)
                    QApplication.sendEvent(self.host_widget, QKeyEvent(QEvent.Type.KeyPress, key, Qt.KeyboardModifier(0), ch))
                # Ensure key events are delivered before any other processing
                while QApplication.instance().processEvents():
                    pass
                return True
        return False

    @connect_signal()
    def fill_form_field_for(self, url, which, left, top, right, bottom):
        ac = self.get_login_credentials(url)
        if ac is not None:
            if self.send_text_using_keys(ac[which]):
                python_to_js(self, 'form_field_filled', url, which)

    def on_login_form_found(self, url, is_current_form):
        ac = self.get_login_credentials(url)
        if ac is not None:
            python_to_js(self, 'autofill_login_form', url, ac['autologin'], is_current_form)

    def find_text(self, text, callback=None, forward=True):
        flags = QWebEnginePage.FindFlag(0) if forward else QWebEnginePage.FindFlag.FindBackward
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
        x, y = self.scroll_position
        sz = self._page.contentsSize()
        ans = {
            'x': x, 'y': y,
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
        self.muted = state['audio_muted']
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
        jkey = FOLLOW_LINK_KEY_MAP.get(key.key())
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

    @connect_signal()
    def save_text_edit_node(self, selection_start, selection_end, source_frame_id, node_id):
        if self.callback_on_save_edit_text_node is not None:
            self.callback_on_save_edit_text_node(selection_start, selection_end, source_frame_id, node_id)

    def trigger_inspect(self):
        if not self.dev_tools_enabled:
            self.dev_tools_requested.emit()
        self._page.triggerAction(QWebEnginePage.WebAction.InspectElement)

    def contextMenuEvent(self, ev):
        self.middle_click_soon = monotonic() + 2  # so that voew page source does not popup a confirmation
        menu = self.createStandardContextMenu()
        menu.addSeparator()
        menu.addAction(_('Inspect element'), self.trigger_inspect)
        menu.exec(ev.globalPos())
