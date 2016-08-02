#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2015, Kovid Goyal <kovid at kovidgoyal.net>

import os
from functools import partial
from gettext import gettext as _

import sip
from PyQt5.Qt import (
    QMainWindow, Qt, QSplitter, QApplication, QStackedWidget, QUrl, QFrame,
    QKeySequence, pyqtSignal, QTimer
)

from .ask import Ask
from .cmd import run_command
from .config import color
from .constants import appname
from .downloads import Indicator
from .settings import gprefs, profile, create_profile, quickmarks
from .status_bar import Status, ModeLabel, PassthroughButton
from .tab_tree import TabTree
from .view import WebView


_window_id = 0


class StackedWidget(QStackedWidget):

    resized = pyqtSignal()

    def resizeEvent(self, ev):
        self.resized.emit()
        return QStackedWidget.resizeEvent(self, ev)


class MainWindow(QMainWindow):

    start_search_signal = pyqtSignal(bool)

    def __init__(self, is_private=False):
        global _window_id
        QMainWindow.__init__(self)
        self.current_tab = None
        self.quickmark_pending = self.choose_tab_pending = None
        _window_id += 1
        self.window_id = _window_id
        self.is_private = is_private
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.status_msg = Status(self)
        self.status_msg.hidden.connect(self.refocus)
        self.start_search_signal.connect(self.status_msg.show_search, type=Qt.QueuedConnection)
        self.start_search = lambda forward=True: self.start_search_signal.emit(forward)
        self.status_msg.search.edit.do_search.connect(self.do_search)
        self.statusBar().addWidget(self.status_msg)
        self.mode_label = ml = ModeLabel(self)
        self.passthrough_button = PassthroughButton(self)
        self.downloads_indicator = Indicator(self)

        def addsep():
            f = QFrame(self)
            f.setFrameShape(f.VLine)
            self.statusBar().addPermanentWidget(f)
        addsep()
        self.statusBar().addPermanentWidget(ml)
        addsep()
        self.statusBar().addPermanentWidget(self.downloads_indicator)
        addsep()
        self.statusBar().addPermanentWidget(self.passthrough_button)
        self.statusBar().setStyleSheet('''
        QStatusBar { color: FG; background: BG; }
        QStatusBar QLabel { color: FG; background: BG; }
        '''.replace(
            'FG', color('status bar foreground', 'palette(window-text)')).replace(
            'BG', color('status bar background', 'palette(window)'))
        )

        self.main_splitter = w = QSplitter(self)
        self.setCentralWidget(w)

        self.tabs = []
        self.tab_tree = tt = TabTree(self)
        tt.tab_activated.connect(self.show_tab)
        tt.tab_close_requested.connect(self.close_tab)
        tt.delete_tabs.connect(self.delete_removed_tabs)
        w.addWidget(tt)
        self.stack = s = StackedWidget(self)
        s.currentChanged.connect(self.current_tab_changed)
        w.addWidget(s), w.setCollapsible(1, False)
        self.ask = a = Ask(s)
        a.hidden.connect(self.refocus)
        a.setVisible(False), a.run_command.connect(self.run_command)
        self.profile = create_profile(private=True) if is_private else profile()

        self.open_url(QUrl('vise:welcome'))

        self.restore_state()
        self.current_tab_changed()

    def show_status_message(self, msg, timeout=1, message_type='info'):
        self.statusBar().showMessage(msg, int(timeout * 1000))

    def ask(self, prefix):
        self.ask(prefix)

    def run_command(self, text):
        run_command(self, text)

    def refocus(self):
        if self.current_tab is not None:
            self.current_tab.setFocus(Qt.TabFocusReason)
        else:
            self.stack.setFocus(Qt.TabFocusReason)

    def sizeHint(self):
        rect = QApplication.desktop().screenGeometry(self)
        return rect.size() * 0.9

    def save_state(self):
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
        QApplication.instance().remove_window_later.emit(self)
        ev.accept()

    def create_new_tab(self):
        ans = WebView(self.profile, self)
        self.stack.addWidget(ans)
        self.tabs.append(ans)
        ans.title_changed.connect(self.update_window_title)
        ans.open_in_new_tab.connect(self.open_in_new_tab)
        ans.urlChanged.connect(self.url_changed)
        ans.link_hovered.connect(partial(self.link_hovered, ans))
        ans.window_close_requested.connect(self.close_tab)
        ans.focus_changed.connect(self.mode_label.update_mode)
        ans.passthrough_changed.connect(self.mode_label.update_mode)
        ans.passthrough_changed.connect(self.passthrough_button.update_state)
        ans.toggle_full_screen.connect(self.toggle_full_screen)
        return ans

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

    def raise_tab(self, tab):
        self.stack.setCurrentWidget(tab)

    def delete_removed_tabs(self, tabs):
        # Delete tabs that have already been removed from the tab tree
        for tab in tabs:
            tab.break_cycles()
            try:
                self.tabs.remove(tab)
            except ValueError:
                pass
            self.stack.removeWidget(tab)

    def close_tab(self, tab=None):
        tab = tab or self.current_tab
        if tab is not None:
            self.delete_removed_tabs(self.tab_tree.remove_tab(tab))
        if not self.tabs:
            self.open_url(QUrl('vise:welcome'), switch_to_tab=True)
            QTimer.singleShot(0, self.current_tab_changed)

    def break_cycles(self):
        for tab in self.tabs:
            if not sip.isdeleted(tab):
                self.stack.removeWidget(tab)
                tab.break_cycles()
                tab.deleteLater()
        self.tabs = []

    def url_changed(self):
        if self.current_tab is None:
            self.status_msg('')
        else:
            qurl = self.current_tab.url()
            val = qurl.toDisplayString()
            self.status_msg(val)

    def link_hovered(self, tab, href):
        if tab is self.current_tab:
            self.show_status_message(href, 10)

    def get_tab_for_load(self, in_current_tab=True):
        in_current_tab = self.current_tab is not None and in_current_tab
        if in_current_tab:
            tab = self.current_tab
        else:
            tab = self.create_new_tab()
            self.tab_tree.add_tab(tab)
            if self.current_tab is None:
                self.current_tab = tab
        return tab

    def open_url(self, qurl, in_current_tab=True, switch_to_tab=False):
        tab = self.get_tab_for_load(in_current_tab=in_current_tab)
        tab.load(qurl)
        if switch_to_tab:
            self.show_tab(tab)
        return tab

    def show_html(self, html, in_current_tab=True):
        if isinstance(html, bytes):
            html = html.decode('utf-8')
        tab = self.get_tab_for_load(in_current_tab=in_current_tab)
        tab.setHtml(html, QUrl.fromLocalFile(os.path.expanduser('~')))

    def open_in_new_tab(self, qurl):
        if isinstance(qurl, str):
            qurl = QUrl(qurl)
        if self.current_tab is None:
            return self.open_url(qurl, in_current_tab=False)
        tab = self.create_new_tab()
        self.tab_tree.add_tab(tab, parent=self.current_tab)
        tab.load(qurl)

    def current_tab_changed(self):
        self.update_window_title()
        self.current_tab = self.stack.currentWidget()
        self.tab_tree.current_changed(self.current_tab)
        self.passthrough_button.update_state()
        self.url_changed()

    def show_tab(self, tab):
        if tab is not None:
            self.stack.setCurrentWidget(tab)

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
            if not key & Qt.Key_Escape:
                key = QKeySequence(key).toString()
                self.show_status_message(_('Quickmark %s is not defined!') % key, 5, 'error')
            return
        self.open_url(url, in_current_tab=in_current_tab, switch_to_tab=True)

    def choose_tab(self, key):
        self.choose_tab_pending = None
        if not self.tab_tree.activate_marked_tab(key):
            if not key & Qt.Key_Escape:
                key = QKeySequence(key).toString()
                self.show_status_message(_('No tab with mark: %s') % key, 5, 'error')
        self.tab_tree.mark_tabs(unmark=True)

    def do_search(self, text=None, forward=True):
        if self.current_tab is not None:
            text = self.status_msg.current_search_text if text is None else text
            self.current_tab.find_text(text, self.search_done)

    def search_done(self, text, found):
        if text:
            msg = _('%s found') % text if found else _('%s not found!') % text
            self.show_status_message(msg, 1 if found else 3, 'success' if found else 'error')

    def follow_next(self, forward=True):
        if self.current_tab is not None:
            self.current_tab.follow_next(forward)
