#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2015, Kovid Goyal <kovid at kovidgoyal.net>

import os
from functools import partial

from PyQt5.Qt import (
    QMainWindow, Qt, QSplitter, QApplication, QStackedWidget, QUrl, QLabel
)

from .constants import appname
from .resources import get_data_as_file
from .settings import gprefs, profile, create_profile
from .tab_tree import TabTree
from .view import WebView


class MainWindow(QMainWindow):

    def __init__(self, is_private=False):
        QMainWindow.__init__(self)
        self.is_private = is_private
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.url_label = QLabel('')
        self.statusBar().addWidget(self.url_label)

        self.main_splitter = w = QSplitter(self)
        self.setCentralWidget(w)

        self.tabs = []
        self.current_tab = None
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
        return ans

    def url_changed(self):
        if self.current_tab is None:
            self.url_label.setText('')
        else:
            self.url_label.setText('<b>' + self.current_tab.url().toDisplayString())

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
