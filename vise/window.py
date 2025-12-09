#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2015, Kovid Goyal <kovid at kovidgoyal.net>

import os
from collections import deque
from gettext import gettext as _
from itertools import count

from PyQt6 import sip
from PyQt6.QtCore import QEventLoop, Qt, QTimer, QUrl, pyqtSignal, QSize
from PyQt6.QtGui import QKeySequence
from PyQt6.QtWebEngineCore import QWebEnginePage
from PyQt6.QtWidgets import (QApplication, QMainWindow, QSplitter,
                             QStackedWidget)

from .ask import Ask
from .cmd import run_command
from .constants import appname
from .dev_tools import DevToolsContainer
from .downloads import Indicator
from .places import places
from .resources import get_icon
from .settings import create_profile, gprefs, profile, quickmarks
from .status_bar import StatusBar
from .tab_tree import TabTree
from .view import WebView
from .welcome import WELCOME_URL

window_id = count()


class StackedWidget(QStackedWidget):

    resized = pyqtSignal()

    def resizeEvent(self, ev):
        self.resized.emit()
        return QStackedWidget.resizeEvent(self, ev)


class MainWindow(QMainWindow):

    start_search_signal = pyqtSignal(bool)
    window_closed = pyqtSignal(object)

    def __init__(self, is_private=False, restart_state=None):
        QMainWindow.__init__(self)
        self.saved_scroll = None
        self.setWindowIcon(get_icon('vise.svg'))
        self.setWindowRole('browser')
        self.current_tab = None
        self.quickmark_pending = self.choose_tab_pending = None
        self.window_id = next(window_id)
        self.is_private = is_private
        self.deleted_tabs_cache = deque(maxlen=200)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)

        self.downloads_indicator = Indicator(self)
        self.status_bar = StatusBar(self.downloads_indicator, self)
        self.start_search_signal.connect(self.show_search, type=Qt.ConnectionType.QueuedConnection)
        self.start_search = lambda forward=True: self.start_search_signal.emit(forward)
        self.status_bar.do_search.connect(self.do_search)
        self.status_bar.change_passthrough.connect(self.change_passthrough)
        self.status_bar.search_bar_hidden.connect(self.restore_state_after_popup)
        self.setStatusBar(self.status_bar)

        self.main_splitter = w = QSplitter(self)
        self.setCentralWidget(w)

        self.tabs = []
        self.tab_tree = tt = TabTree(self)
        tt.tab_loading_status_changed.connect(self.status_bar.loading_status_changed)
        tt.delete_tabs.connect(self.update_status_bar_state, type=Qt.ConnectionType.QueuedConnection)
        tt.tab_activated.connect(self.show_tab)
        tt.tab_close_requested.connect(self.close_tab)
        tt.delete_tabs.connect(self.delete_removed_tabs)
        w.addWidget(tt)
        self.stack = s = StackedWidget(self)
        s.currentChanged.connect(self.current_tab_changed)
        w.addWidget(s)
        self.dev_tools_container = d = DevToolsContainer(self)
        self.before_devtools_splitter_state = None
        self.prev_devtools_splitter_state = None
        w.addWidget(d)
        d.setVisible(False)
        w.setCollapsible(0, True), w.setCollapsible(1, False), w.setCollapsible(2, True)
        self._ask = a = Ask(s)
        a.setVisible(False), a.run_command.connect(self.run_command)
        a.hidden.connect(self.restore_state_after_popup)
        self.profile = create_profile(private=True) if is_private else profile()
        if is_private:
            # TODO: delete this profile on window close rather than application
            # close
            self.profile.setParent(None)

        if restart_state is None:
            self.open_url(WELCOME_URL)
        else:
            self.unserialize_state(restart_state)

        self.restore_state()
        self.current_tab_changed()

    def save_scroll(self):
        if self.current_tab is not None:
            self.saved_scroll = self.current_tab, self.current_tab.scroll_position

    def restore_state_after_popup(self):
        ss, self.saved_scroll = self.saved_scroll, None
        if ss is not None:
            tab, pos = ss
            if tab is self.current_tab:
                tab.scroll_position = pos
                tab.exit_text_input()

    def ask(self, *a, **k):
        self.save_scroll()
        self._ask(*a, **k)

    def show_search(self, *a, **k):
        self.save_scroll()
        self.status_bar.show_search(*a, **k)

    def show_status_message(self, msg, timeout=1, message_type='info'):
        self.status_bar.show_message(msg, timeout, message_type)

    def run_command(self, text):
        run_command(self, text)

    def sizeHint(self):
        return QSize(800, 600)

    def save_state(self):
        self.set_devtools_visibility(False)
        with gprefs:
            gprefs['main-window-geometry'] = bytearray(self.saveGeometry())
            gprefs['main-splitter-state'] = bytearray(self.main_splitter.saveState())

    def restore_state(self):
        geom = gprefs.get('main-window-geometry')
        if geom is not None:
            self.restoreGeometry(geom)
        ms = gprefs.get('main-splitter-state')
        if ms is not None:
            self.main_splitter.restoreState(ms)
        else:
            self.main_splitter.setSizes([300, 700])

    def closeEvent(self, ev):
        self.save_state()
        ev.accept()
        self.window_closed.emit(self)

    def create_new_tab(self):
        ans = WebView(self.profile, self)
        self.stack.addWidget(ans)
        self.tabs.append(ans)
        ans.title_changed.connect(self.update_window_title)
        ans.urlChanged.connect(self.url_changed)
        ans.link_hovered.connect(self.link_hovered)
        ans.window_close_requested.connect(self.close_tab, type=Qt.ConnectionType.QueuedConnection)
        ans.focus_changed.connect(self.update_mode)
        ans.passthrough_changed.connect(self.update_status_bar_state)
        ans.toggle_full_screen.connect(self.toggle_full_screen)
        ans.dev_tools_requested.connect(self.dev_tools_requested)
        if self.current_tab:
            # As of Qt 5.11 adding the widget to the stack does not
            # set its geometry correctly until it is shown
            ans.setGeometry(self.current_tab.geometry())
        return ans

    def update_mode(self):
        tab = self.current_tab
        text = ''
        if tab is not None:
            if tab.force_passthrough:
                text = '-- %s --' % _('PASSTHROUGH')
            elif tab.text_input_focused:
                text = '-- %s --' % _('INSERT')
        self.status_bar.update_mode(text)

    def update_passthrough_state(self):
        tab = self.current_tab
        passthrough = getattr(tab, 'force_passthrough', False)
        self.status_bar.update_passthrough_state(passthrough)

    def update_status_bar_state(self):
        self.update_mode()
        self.update_passthrough_state()
        self.tab_tree.emit_tab_loading_status_changed()

    def change_passthrough(self, passthrough):
        tab = self.current_tab
        if tab is not None:
            tab.force_passthrough = passthrough

    def toggle_full_screen(self, on):
        if self.isFullScreen() == on:
            return
        if on:
            self.tab_tree.setVisible(False)
            self.statusBar().setVisible(False)
            self.showFullScreen()
        else:
            self.tab_tree.setVisible(True)
            self.statusBar().setVisible(True)
            self.showNormal()
            for tab in self.tabs:
                tab.exit_full_screen()

    def delete_removed_tabs(self, tabs):
        # Delete tabs that have already been removed from the tab tree
        for tab in tabs:
            self.deleted_tabs_cache.append(tab.serialize_state())
            tab.break_cycles()
            try:
                self.tabs.remove(tab)
            except ValueError:
                pass
            self.stack.removeWidget(tab)
            tab.close()
            # As of Qt 5.11 closing many tabs without processing events between
            # closes causes Qt to crash
            num = 10
            app = QApplication.instance()
            while app.processEvents(QEventLoop.ProcessEventsFlag.ExcludeUserInputEvents, 100) and num > 0:
                num -= 1

    def undelete_tab(self):
        if self.deleted_tabs_cache:
            stab = self.deleted_tabs_cache.pop()
            tab = self.get_tab_for_load(in_current_tab=False)
            self.tab_tree.undelete_tab(tab, stab)
            tab.unserialize_state(stab)
            self.show_tab(tab)
            return True
        return False

    def close_tab(self, tab=None):
        tab = tab or self.current_tab
        if tab is not None:
            self.delete_removed_tabs(self.tab_tree.remove_tab(tab))
        if not self.tabs:
            self.open_url(WELCOME_URL, switch_to_tab=True)
            QTimer.singleShot(0, self.current_tab_changed)
        QTimer.singleShot(0, self.update_status_bar_state)

    def close_all_tabs(self):
        if self.current_tab is not None:
            self.tab_tree.close_other_tabs(self.current_tab)
            self.close_tab(self.current_tab)

    def break_cycles(self):
        self.dev_tools_container.change_widget()
        for tab in self.tabs:
            if not sip.isdeleted(tab):
                self.stack.removeWidget(tab)
                tab.break_cycles()
                tab.deleteLater()
        self.tabs = []

    def url_changed(self):
        if self.current_tab is None:
            self.status_bar.set_permanent_message('')
        else:
            qurl = self.current_tab.url()
            val = qurl.toDisplayString()
            self.status_bar.set_permanent_message(val)

    def link_hovered(self, tab, href):
        if tab is self.current_tab:
            self.show_status_message(href, 10)

    def get_tab_for_load(self, in_current_tab=True, parent=None):
        in_current_tab = self.current_tab is not None and in_current_tab
        if in_current_tab:
            tab = self.current_tab
            # This is needed in Qt 5.10 as otherwise if the tab already has
            # focus, some input element on the new page is given focus on page
            # load
            tab.clearFocus()
        else:
            tab = self.create_new_tab()
            self.tab_tree.add_tab(tab, parent=parent)
            if self.current_tab is None:
                self.current_tab = tab
                tab.setFocus(Qt.FocusReason.ActiveWindowFocusReason)
        return tab

    def get_child_tab_for_load(self):
        return self.get_tab_for_load(in_current_tab=False, parent=self.current_tab)

    def open_url(self, qurl, in_current_tab=True, switch_to_tab=False):
        tab = self.get_tab_for_load(in_current_tab=in_current_tab)
        tab.load(qurl)
        if switch_to_tab:
            self.show_tab(tab)
        return tab

    def save_url_in_places(self, qurl):
        places.on_visit(qurl, QWebEnginePage.NavigationType.NavigationTypeTyped, True)

    def show_html(self, html, in_current_tab=True):
        if isinstance(html, bytes):
            html = html.decode('utf-8')
        tab = self.get_tab_for_load(in_current_tab=in_current_tab)
        tab.setHtml(html, QUrl.fromLocalFile(os.path.expanduser('~')))

    def current_tab_changed(self):
        self.update_window_title()
        self.current_tab = self.stack.currentWidget()
        self.tab_tree.current_changed(self.current_tab)
        self.update_status_bar_state()
        self.url_changed()
        if self.current_tab is not None:
            self.current_tab.on_display_in_stack()
            if self.current_tab.dev_tools_enabled:
                self.dev_tools_container.change_widget(self.current_tab.dev_tools)
                self.set_devtools_visibility(True)
            else:
                self.dev_tools_container.change_widget()
                self.set_devtools_visibility(False)

    def show_tab(self, tab):
        if tab is not None and self.current_tab is not tab:
            self.stack.setCurrentWidget(tab)
            if not tab.hasFocus():
                tab.setFocus(Qt.FocusReason.ActiveWindowFocusReason)

    def update_window_title(self):
        title = at = appname.capitalize()
        if self.current_tab is not None:
            x = self.current_tab.title()
            if x:
                title = '%s - %s' % (x, at)
        self.setWindowTitle(title)

    def quickmark(self, key):
        in_current_tab = self.quickmark_pending == 'sametab'
        self.quickmark_pending = None
        url = quickmarks().get(key)
        if url is None:
            if key.key() is not Qt.Key.Key_Escape:
                key = QKeySequence(key).toString()
                self.show_status_message(_('Quickmark %s is not defined!') % key, 5, 'error')
            return
        self.open_url(url, in_current_tab=in_current_tab, switch_to_tab=True)

    def choose_tab(self, key):
        self.choose_tab_pending = None
        if not self.tab_tree.activate_marked_tab(key):
            if key != Qt.Key.Key_Escape:
                key = QKeySequence(key).toString()
                self.show_status_message(_('No tab with mark: %s') % key, 5, 'error')
        self.tab_tree.mark_tabs(unmark=True)

    def start_follow_link(self, action):
        if self.current_tab is not None:
            self.current_tab.start_follow_link(action)

    def do_search(self, text=None, forward=True):
        if self.current_tab is not None:
            text = self.status_bar.current_search_text if text is None else text
            self.current_tab.find_text(text, self.search_done)

    def search_done(self, text, found):
        if text:
            msg = _('%s found') % text if found else _('%s not found!') % text
            self.show_status_message(msg, 1 if found else 3, 'success' if found else 'error')

    def serialize_state(self, include_favicons=False):
        ans = {'window_id': self.window_id, 'is_private': self.is_private}
        tab_map = ans['tab_map'] = {}
        for tab in self.tabs:
            s = tab.serialize_state(include_favicon=include_favicons)
            tab_map[s['view_id']] = s
        if self.current_tab is not None:
            ans['current_tab'] = self.current_tab.view_id
        ans['tab_tree'] = self.tab_tree.serialize_state()
        return ans

    def unserialize_state(self, state):
        tab_map = state['tab_map']
        current_tab_id = state.get('current_tab')
        current_tab = None

        def process_node(node, parent=None):
            nonlocal current_tab
            for child in node['children']:
                tab = self.get_tab_for_load(in_current_tab=False, parent=parent)
                tab.unserialize_state(tab_map[child['view_id']])
                if child['view_id'] == current_tab_id:
                    current_tab = tab
                process_node(child, tab)
                self.tab_tree.unserialize_state(child, tab)

        process_node(state['tab_tree'])
        if current_tab is not None:
            self.show_tab(current_tab)

    def set_devtools_visibility(self, visible):
        if self.dev_tools_container.isVisible() == visible:
            return
        if not self.dev_tools_container.isVisible():
            self.before_devtools_splitter_state = self.main_splitter.saveState()
            self.dev_tools_container.setVisible(True)
            if self.prev_devtools_splitter_state is not None:
                self.main_splitter.restoreState(self.prev_devtools_splitter_state)
            else:
                w = self.main_splitter.width()
                self.main_splitter.setSizes([int(w * 0.2), int(w * 0.45), int(w * 0.35)])
        else:
            self.prev_devtools_splitter_state = self.main_splitter.saveState()
            self.dev_tools_container.setVisible(False)
            if self.before_devtools_splitter_state is not None:
                self.main_splitter.restoreState(self.before_devtools_splitter_state)

    def toggle_devtools(self):
        if self.dev_tools_container.isVisible():
            self.set_devtools_visibility(False)
            if self.current_tab is not None:
                self.dev_tools_container.change_widget()
                self.current_tab.close_dev_tools()
        else:
            self.set_devtools_visibility(True)
            if self.current_tab is not None:
                self.dev_tools_container.change_widget(self.current_tab.dev_tools)

    def dev_tools_requested(self):
        if not self.dev_tools_container.isVisible():
            self.toggle_devtools()
