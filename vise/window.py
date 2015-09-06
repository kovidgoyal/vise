#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2015, Kovid Goyal <kovid at kovidgoyal.net>

import os
from functools import partial
from gettext import gettext as _

from PyQt5.Qt import (
    QMainWindow, Qt, QSplitter, QApplication, QStackedWidget, QUrl, QLabel,
    QToolButton, QFrame
)

from .constants import appname
from .resources import get_data_as_file, get_icon
from .settings import gprefs, profile, create_profile
from .tab_tree import TabTree
from .view import WebView


class Status(QStackedWidget):

    def __init__(self, parent):
        QStackedWidget.__init__(self, parent)
        self.msg = QLabel('')
        self.msg.setFocusPolicy(Qt.NoFocus)
        self.addWidget(self.msg)

    def __call__(self, text=''):
        self.msg.setText('<b>' + text)


class ModeLabel(QLabel):

    def __init__(self, main_window):
        QLabel.__init__(self, '')
        self.main_window = main_window

    def update_mode(self):
        tab = self.main_window.current_tab
        text = ''
        if tab is not None:
            if tab.force_passthrough:
                text = '-- %s --' % _('PASSTHROUGH')
            elif tab.text_input_focused:
                text = '-- %s --' % _('INSERT')
        self.setText(text)


class PassthroughButton(QToolButton):

    def __init__(self, main_window):
        QToolButton.__init__(self, main_window)
        self.setCursor(Qt.PointingHandCursor)
        self.main_window = main_window
        self.setCheckable(True)
        self.setIcon(get_icon('images/passthrough.png'))
        self.toggled.connect(self.change_passthrough)
        self.update_state()

    def update_state(self):
        self.blockSignals(True)
        tab = self.main_window.current_tab
        self.setChecked(getattr(tab, 'force_passthrough', False))
        self.setToolTip(_('Disable passthrough mode') if self.isChecked() else _(
            'Enable passthrough mode'))
        self.blockSignals(False)

    def change_passthrough(self):
        tab = self.main_window.current_tab
        if tab is not None:
            tab.force_passthrough = self.isChecked()


_window_id = 0


class MainWindow(QMainWindow):

    def __init__(self, is_private=False):
        global _window_id
        QMainWindow.__init__(self)
        self.current_tab = None
        _window_id += 1
        self.window_id = _window_id
        self.is_private = is_private
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.status_msg = Status(self)
        self.statusBar().addWidget(self.status_msg)
        self.mode_label = ml = ModeLabel(self)
        self.passthrough_button = b = PassthroughButton(self)

        def addsep():
            f = QFrame(self)
            f.setFrameShape(f.VLine)
            self.statusBar().addPermanentWidget(f)
        addsep()
        self.statusBar().addPermanentWidget(ml)
        addsep()
        self.statusBar().addPermanentWidget(b)

        self.main_splitter = w = QSplitter(self)
        self.setCentralWidget(w)

        self.tabs = []
        self.tab_tree = tt = TabTree(self)
        tt.tab_activated.connect(self.show_tab)
        w.addWidget(tt)
        self.stack = s = QStackedWidget(self)
        s.currentChanged.connect(self.current_tab_changed)
        w.addWidget(s), w.setCollapsible(1, False)
        self.profile = create_profile(private=True) if is_private else profile()

        self.show_html(get_data_as_file('welcome.html').read())

        self.restore_state()
        self.current_tab_changed()

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
        ev.accept()
        QApplication.instance().remove_window(self)

    def create_new_tab(self):
        ans = WebView(self.profile, self)
        self.stack.addWidget(ans)
        self.tabs.append(ans)
        ans.titleChanged.connect(self.update_window_title)
        ans.open_in_new_tab.connect(self.open_in_new_tab)
        ans.urlChanged.connect(self.url_changed)
        ans.link_hovered.connect(partial(self.link_hovered, ans))
        ans.window_close_requested.connect(self.close_tab)
        ans.focus_changed.connect(self.mode_label.update_mode)
        ans.passthrough_changed.connect(self.mode_label.update_mode)
        ans.passthrough_changed.connect(self.passthrough_button.update_state)
        return ans

    def raise_tab(self, tab):
        self.stack.setCurrentWidget(tab)

    def close_tab(self, tab):
        self.tab_tree.remove_tab(tab)
        tab.break_cycles()
        self.tabs.remove(tab)
        self.stack.removeWidget(tab)

    def break_cycles(self):
        for tab in self.tabs:
            self.stack.removeWidget(tab)
            tab.break_cycles()
        self.tabs = []

    def url_changed(self):
        if self.current_tab is None:
            self.status_msg('')
        else:
            self.status_msg(self.current_tab.url().toDisplayString())

    def link_hovered(self, tab, href):
        if tab is self.current_tab:
            self.statusBar().showMessage(href, 10000)

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

    def open_url(self, qurl, in_current_tab=True):
        tab = self.get_tab_for_load(in_current_tab=in_current_tab)
        tab.load(qurl)

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
