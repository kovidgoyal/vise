#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2015, Kovid Goyal <kovid at kovidgoyal.net>

from PyQt5.Qt import QWebEngineView, QWebEnginePage, QSize

view_id = 0


class WebPage(QWebEnginePage):

    def __init__(self, profile, parent):
        QWebEnginePage.__init__(self, profile, parent)


class WebView(QWebEngineView):

    def __init__(self, profile, parent):
        global view_id
        QWebEngineView.__init__(self, parent)
        self.create_page(profile)
        self.view_id = view_id
        view_id += 1

    def create_page(self, profile):
        self._page = WebPage(profile, self)
        self.setPage(self._page)

    def sizeHint(self):
        return QSize(800, 600)
