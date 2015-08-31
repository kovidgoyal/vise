#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2015, Kovid Goyal <kovid at kovidgoyal.net>

import weakref
from gettext import gettext as _
from functools import partial

from PyQt5.Qt import (
    QTreeWidget, QTreeWidgetItem, Qt, pyqtSignal, QSize, QFont, QPen, QRect,
    QApplication, QPainter, QPixmap, QIcon, QTimer, QAbstractItemDelegate
)

from .utils import elided_text, draw_snake_spinner

TAB_ROLE = Qt.UserRole
LOADING_ROLE = TAB_ROLE + 1
ANGLE_ROLE = LOADING_ROLE + 1
ICON_SIZE = 24


_missing_icon = None


def missing_icon():
    global _missing_icon
    if _missing_icon is None:
        p = QPixmap(ICON_SIZE, ICON_SIZE)
        p.fill(Qt.transparent)
        painter = QPainter(p)
        pal = QApplication.instance().palette()
        painter.setPen(QPen(pal.color(pal.Text), 0, Qt.DashLine))
        margin = 3
        r = p.rect().adjusted(margin, margin, -margin, -margin)
        painter.drawRect(r)
        painter.end()
        _missing_icon = QIcon(p)
    return _missing_icon


class TabDelegate(QAbstractItemDelegate):

    MARGIN = 2

    def __init__(self, parent):
        QAbstractItemDelegate.__init__(self, parent)
        pal = parent.palette()
        self.dark = pal.color(pal.Text)
        self.light = pal.color(pal.Base)

    def sizeHint(self, option, index):
        return QSize(300, ICON_SIZE + 2 * self.MARGIN)

    def paint(self, painter, option, index):
        rect = option.rect
        icon_rect = QRect(rect.left() + self.MARGIN, rect.top() + self.MARGIN, ICON_SIZE, ICON_SIZE)
        left = icon_rect.right() + 2 * self.MARGIN
        text_rect = QRect(left, icon_rect.top(), rect.width() - left, icon_rect.height())
        font = index.data(Qt.FontRole)
        if font:
            painter.setFont(font)
        text_flags = Qt.AlignVCenter | Qt.AlignLeft | Qt.TextSingleLine
        text = elided_text(index.data(Qt.DisplayRole) or '', font, text_rect.width(), 'right')
        painter.drawText(text_rect, text_flags, text)
        if index.data(LOADING_ROLE):
            angle = index.data(ANGLE_ROLE)
            draw_snake_spinner(painter, icon_rect, angle, self.light, self.dark)
        else:
            icon = index.data(Qt.DecorationRole)
            icon.paint(painter, icon_rect)

tab_item_counter = 0


class TabItem(QTreeWidgetItem):

    def __init__(self, tab, loading_status_changed):
        global tab_item_counter
        QTreeWidgetItem.__init__(self)
        tab_item_counter += 1
        self.uid = tab_item_counter
        self.loading_status_changed = loading_status_changed
        self.set_data(LOADING_ROLE, False)
        self.set_data(Qt.DisplayRole, tab.title() or _('Loading...'))
        self.set_data(Qt.DecorationRole, missing_icon())
        self.set_data(ANGLE_ROLE, 0)

        self.tabref = weakref.ref(tab)
        self.set_data(TAB_ROLE, self.tabref)
        tab.titleChanged.connect(partial(self.set_data, Qt.DisplayRole))
        tab.icon_changed.connect(self.icon_changed)
        tab.loading_status_changed.connect(self._loading_status_changed)

    def _loading_status_changed(self, loading):
        self.set_data(ANGLE_ROLE, 0)
        self.set_data(LOADING_ROLE, loading)
        self.loading_status_changed(self, loading)

    def icon_changed(self, new_icon):
        if new_icon.isNull():
            new_icon = missing_icon()
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

    def __hash__(self):
        return self.uid


class TabTree(QTreeWidget):

    tab_activated = pyqtSignal(object)

    def __init__(self, parent):
        QTreeWidget.__init__(self, parent)
        self.setHeaderHidden(True)
        self.setSelectionMode(self.NoSelection)
        self.itemClicked.connect(self.item_clicked)
        self.setIconSize(QSize(ICON_SIZE, ICON_SIZE))
        self.current_item = None
        self.emphasis_font = QFont(self.font())
        self.emphasis_font.setBold(True)
        self.setFocusPolicy(Qt.NoFocus)
        self.animation_timer = t = QTimer(self)
        t.setInterval(10)
        t.timeout.connect(self.tick_loading_animation)
        self.loading_items = set()
        self.delegate = TabDelegate(self)
        self.setItemDelegate(self.delegate)

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
        i = TabItem(tab, self.loading_status_changed)
        if parent is None:
            self.addTopLevelItem(i)
        else:
            self.item_for_tab(parent).addChild(i)
            self.scrollToItem(i)

    def loading_status_changed(self, item, loading):
        if loading:
            self.loading_items.add(item)
            self.animation_timer.start()
        else:
            self.loading_items.discard(item)
            if not self.loading_items:
                self.animation_timer.stop()

    def tick_loading_animation(self):
        for item in self.loading_items:
            angle = item.data(0, ANGLE_ROLE)
            item.set_data(ANGLE_ROLE, angle - 4)

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
            item.set_data(Qt.FontRole, self.emphasis_font)
