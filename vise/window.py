#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2015, Kovid Goyal <kovid at kovidgoyal.net>

import os

from PyQt5.Qt import (
    QMainWindow, Qt, QSplitter, QApplication, QStackedWidget, QUrl)

from .constants import appname
from .resources import get_data_as_file
from .settings import gprefs, profile, create_profile
from .tab_tree import TabTree
from .view import WebView


class Tabs:

    def __init__(self, view=None):
        self._tabs = set()
        self.view = view
        self.is_root = view is None

    def add(self, tab):
        self._tabs.add(Tabs(tab))

    def __iter__(self):
        return iter(self._tabs)

    def __len__(self):
        return len(self._tabs)


class MainWindow(QMainWindow):

    def __init__(self, is_private=False):
        QMainWindow.__init__(self)
        self.is_private = is_private
        self.setAttribute(Qt.WA_DeleteOnClose, True)

        self.main_splitter = w = QSplitter(self)
        self.setCentralWidget(w)

        self.tabs = Tabs()
        self.tab_tree = tt = TabTree(self)
        self.current_tab = None
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
        geom = gprefs['main-window-geometry']
        if geom is not None:
            self.restoreGeometry(geom)
        ms = gprefs['main-splitter-state']
        if ms is not None:
            self.main_splitter.restoreState(ms)
        else:
            self.main_splitter.setSizes([300, 700])

    def closeEvent(self, ev):
        self.save_state()
        ev.accept()
        QApplication.instance().remove_window(self)

    def create_new_tab(self):
        ans = WebView(self.profile, self.stack)
        self.stack.addWidget(ans)
        self.tabs.add(ans)
        ans.titleChanged.connect(self.update_window_title)
        return ans

    def open_url(self, qurl, in_current_tab=True):
        in_current_tab = self.current_tab is not None and in_current_tab
        tab = self.current_tab if in_current_tab else self.create_new_tab()
        tab.load(qurl)
        if self.current_tab is None:
            self.current_tab = tab

    def show_html(self, html, in_current_tab=True):
        if isinstance(html, bytes):
            html = html.decode('utf-8')
        in_current_tab = self.current_tab is not None and in_current_tab
        tab = self.current_tab if in_current_tab else self.create_new_tab()
        tab.setHtml(html, QUrl.fromLocalFile(os.path.expanduser('~')))
        if self.current_tab is None:
            self.current_tab = tab

    def current_tab_changed(self):
        self.update_window_title()

    def update_window_title(self):
        title = at = appname.capitalize()
        if self.current_tab is not None:
            x = self.current_tab.title()
            if x:
                title = '%s - %s' % (x, at)
        self.setWindowTitle(title)
