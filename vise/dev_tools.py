#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2018, Kovid Goyal <kovid at kovidgoyal.net>

from PyQt6.QtWidgets import QHBoxLayout, QWidget
from PyQt6.QtWebEngineWidgets import QWebEngineView


def default_size_hint(ans):
    ans.setWidth(400), ans.setHeight(600)
    return ans


class DevTools(QWebEngineView):

    def __init__(self, parent=None):
        QWebEngineView.__init__(self, parent)

    def set_inspected_view(self, view=None):
        self.page().setInspectedPage(view.page() if view else None)

    def sizeHint(self):
        return default_size_hint(QWebEngineView.sizeHint(self))


class DevToolsContainer(QWidget):

    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.ly = ly = QHBoxLayout(self)
        ly.setContentsMargins(0, 0, 0, 0)
        self.has_widget = False

    def change_widget(self, dev_tools=None):
        item = self.ly.itemAt(0)
        if item:
            self.ly.removeItem(item)
            w = item.widget()
            if w:
                w.setParent(None)
        self.has_widget = False
        if dev_tools:
            self.ly.addWidget(dev_tools)
            self.has_widget = True

    def sizeHint(self):
        ans = QWidget.sizeHint(self)
        if not self.has_widget:
            ans = default_size_hint(ans)
        return ans
