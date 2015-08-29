#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2015, Kovid Goyal <kovid at kovidgoyal.net>

import weakref
from gettext import gettext as _
from functools import partial

from PyQt5.Qt import (
    QTreeWidget, QTreeWidgetItem, Qt, pyqtSignal
)


TAB_ROLE = Qt.UserRole


class TabItem(QTreeWidgetItem):

    def __init__(self, tab):
        QTreeWidgetItem.__init__(self)
        self.set_data(Qt.DisplayRole, tab.title() or _('Loading...'))
        self.tabref = weakref.ref(tab)
        self.set_data(TAB_ROLE, self.tabref)
        tab.titleChanged.connect(partial(self.set_data, Qt.DisplayRole))
        tab.icon_changed.connect(partial(self.set_data, Qt.DecorationRole))

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

    def __iter__(self):
        for i in range(self.topLevelItemCount()):
            item = self.topLevelItem(i)
            yield item
            yield from item

    def item_for_tab(self, tab):
        for q in self:
            if q.tab is tab:
                return tab

    def add_tab(self, tab, parent=None):
        i = TabItem(tab)
        if parent is None:
            self.addTopLevelItem(i)
        else:
            self.item_for_tab(parent).addChild(tab)

    def item_clicked(self, item, column):
        if item is not None:
            tab = item.tab
            if tab is not None:
                self.tab_activated.emit(item.tab)
