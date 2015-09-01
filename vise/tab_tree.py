#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2015, Kovid Goyal <kovid at kovidgoyal.net>

import weakref
from gettext import gettext as _
from functools import partial

from PyQt5.Qt import (
    QTreeWidget, QTreeWidgetItem, Qt, pyqtSignal, QSize, QFont, QPen, QRect,
    QApplication, QPainter, QPixmap, QIcon, QTimer, QStyledItemDelegate,
    QModelIndex
)

from .utils import elided_text, draw_snake_spinner

LOADING_ROLE = Qt.UserRole
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


class TabDelegate(QStyledItemDelegate):

    MARGIN = 2

    def __init__(self, parent):
        QStyledItemDelegate.__init__(self, parent)
        pal = parent.palette()
        self.dark = pal.color(pal.Text)
        self.light = pal.color(pal.Base)
        self.errored_out = False

    def sizeHint(self, option, index):
        return QSize(300, ICON_SIZE + 2 * self.MARGIN)

    def paint(self, painter, option, index):
        QStyledItemDelegate.paint(self, painter, option, QModelIndex())
        painter.save()
        rect = option.rect
        icon_rect = QRect(rect.left() + self.MARGIN, rect.top() + self.MARGIN, ICON_SIZE, ICON_SIZE)
        left = icon_rect.right() + 2 * self.MARGIN
        text_rect = QRect(left, icon_rect.top(), rect.width() - left, icon_rect.height())
        text = index.data(Qt.DisplayRole) or ''
        font = index.data(Qt.FontRole)
        if font:
            painter.setFont(font)
        text_flags = Qt.AlignVCenter | Qt.AlignLeft | Qt.TextSingleLine
        text = elided_text(text, font, text_rect.width(), 'right')
        painter.drawText(text_rect, text_flags, text)
        if index.data(LOADING_ROLE):
            if not self.errored_out:
                angle = index.data(ANGLE_ROLE)
                try:
                    draw_snake_spinner(painter, icon_rect, angle, self.light, self.dark)
                except Exception:
                    import traceback
                    traceback.print_exc()
                    self.errored_out = True
        else:
            icon = index.data(Qt.DecorationRole)
            icon.paint(painter, icon_rect)
        painter.restore()

tab_item_counter = 0


class TabItem(QTreeWidgetItem):

    def __init__(self, tab, loading_status_changed):
        global tab_item_counter
        QTreeWidgetItem.__init__(self)
        tab_item_counter += 1
        self.uid = tab_item_counter
        self.loading_status_changed = loading_status_changed
        self.setFlags(self.flags() | Qt.ItemIsDragEnabled | Qt.ItemIsDropEnabled)
        self.set_data(LOADING_ROLE, False)
        self.set_data(Qt.DisplayRole, tab.title() or _('Loading...'))
        self.set_data(Qt.DecorationRole, missing_icon())
        self.set_data(ANGLE_ROLE, 0)
        self.tabref = weakref.ref(tab)
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
        self.setIconSize(QSize(ICON_SIZE, ICON_SIZE))
        self.setAutoScrollMargin(ICON_SIZE * 2)
        self.setAnimated(True)
        self.setHeaderHidden(True)
        self.setSelectionMode(self.ExtendedSelection)
        self.setDragEnabled(True)
        self.viewport().setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setDragDropMode(self.InternalMove)
        self.setDefaultDropAction(Qt.MoveAction)
        self.invisibleRootItem().setFlags(Qt.ItemIsDragEnabled | Qt.ItemIsDropEnabled | self.invisibleRootItem().flags())
        self.itemClicked.connect(self.item_clicked)
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
