#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2015, Kovid Goyal <kovid at kovidgoyal.net>

import weakref
from gettext import gettext as _
from functools import partial

from PyQt5.Qt import (
    QTreeWidget, QTreeWidgetItem, Qt, pyqtSignal, QSize, QFont, QPen,
    QApplication, QPainter, QPixmap, QIcon
)


TAB_ROLE = Qt.UserRole
ICON_SIZE = 24


def missing_icon():
    p = QPixmap(ICON_SIZE, ICON_SIZE)
    p.fill(Qt.transparent)
    painter = QPainter(p)
    pal = QApplication.instance().palette()
    painter.setPen(QPen(pal.color(pal.Text), 0, Qt.DashLine))
    margin = 3
    r = p.rect().adjusted(margin, margin, -margin, -margin)
    painter.drawRect(r)
    painter.end()
    return QIcon(p)


class TabItem(QTreeWidgetItem):

    def __init__(self, tab):
        QTreeWidgetItem.__init__(self)
        self.set_data(Qt.DisplayRole, tab.title() or _('Loading...'))
        self.tabref = weakref.ref(tab)
        self.set_data(TAB_ROLE, self.tabref)
        self.missing_icon = missing_icon()
        tab.titleChanged.connect(partial(self.set_data, Qt.DisplayRole))
        tab.icon_changed.connect(self.icon_changed)

    def icon_changed(self, new_icon):
        if new_icon.isNull():
            new_icon = self.missing_icon
        self.set_data(Qt.DecorationRole, new_icon)

    @property
    def tab(self):
        return self.tabref()

    def __iter__(self):
        for i in range(self.childCount()):
            child = self.child(i)
            yield child
            yield from child

    def set_data(self, role, data):
        self.setData(0, role, data)


class TabTree(QTreeWidget):

    tab_activated = pyqtSignal(object)

    def __init__(self, parent):
        QTreeWidget.__init__(self, parent)
        self.setHeaderHidden(True)
        self.setSelectionMode(self.NoSelection)
        self.itemClicked.connect(self.item_clicked)
        self.setIconSize(QSize(ICON_SIZE, ICON_SIZE))
        self.current_item = None
        self.bold_font = QFont(self.font())
        self.bold_font.setBold(True)

    def __iter__(self):
        for i in range(self.topLevelItemCount()):
            item = self.topLevelItem(i)
            yield item
            yield from item

    def item_for_tab(self, tab):
        for q in self:
            if q.tab is tab:
                return q

    def add_tab(self, tab, parent=None):
        i = TabItem(tab)
        if parent is None:
            self.addTopLevelItem(i)
        else:
            self.item_for_tab(parent).addChild(i)
            self.scrollToItem(i)

    def item_clicked(self, item, column):
        if item is not None:
            tab = item.tab
            if tab is not None:
                self.tab_activated.emit(item.tab)

    def current_changed(self, tab):
        if self.current_item is not None:
            self.current_item.set_data(Qt.FontRole, None)
            self.current_item = None
        item = self.item_for_tab(tab)
        if item is not None:
            self.current_item = item
            item.set_data(Qt.FontRole, self.bold_font)
