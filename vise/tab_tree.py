#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2015, Kovid Goyal <kovid at kovidgoyal.net>

import weakref
import string
from gettext import gettext as _
from functools import partial
from collections import OrderedDict

from PyQt5.Qt import (
    QTreeWidget, QTreeWidgetItem, Qt, pyqtSignal, QSize, QFont, QPen, QRect,
    QApplication, QPainter, QPixmap, QIcon, QTimer, QStyledItemDelegate,
    QStyle, QEvent, QColor
)

from .utils import elided_text, draw_snake_spinner

LOADING_ROLE = Qt.UserRole
ANGLE_ROLE = LOADING_ROLE + 1
HOVER_ROLE = ANGLE_ROLE + 1
CLOSE_HOVER_ROLE = HOVER_ROLE + 1
MARK_ROLE = CLOSE_HOVER_ROLE + 1
DISPLAY_ROLE = MARK_ROLE + 1
DECORATION_ROLE = DISPLAY_ROLE + 1
ICON_SIZE = 24


_missing_icon = None

mark_map = OrderedDict()
for x in string.digits + string.ascii_uppercase:
    mark_map[x] = getattr(Qt, 'Key_' + x)
for x in string.ascii_uppercase:
    mark_map[x] = getattr(Qt, 'Key_' + x) | Qt.ShiftModifier
mark_rmap = {int(v): k for k, v in mark_map.items()}


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
        self.highlighted_text = pal.color(pal.HighlightedText)
        self.errored_out = False

    def sizeHint(self, option, index):
        return QSize(300, ICON_SIZE + 2 * self.MARGIN)

    def paint(self, painter, option, index):
        QStyledItemDelegate.paint(self, painter, option, index)
        hovering = index.data(HOVER_ROLE) is True
        painter.save()
        rect = option.rect
        icon_rect = QRect(rect.left() + self.MARGIN, rect.top() + self.MARGIN, ICON_SIZE, ICON_SIZE)
        left = icon_rect.right() + 2 * self.MARGIN
        text_rect = QRect(left, icon_rect.top(), rect.width() - left + rect.left(), icon_rect.height())
        mark = index.data(MARK_ROLE)
        if hovering or mark:
            text_rect.adjust(0, 0, -text_rect.height(), 0)
        text = index.data(DISPLAY_ROLE) or ''
        font = index.data(Qt.FontRole)
        if font:
            painter.setFont(font)
        text_flags = Qt.AlignVCenter | Qt.AlignLeft | Qt.TextSingleLine
        text = elided_text(text, font, text_rect.width(), 'right')
        if option.state & QStyle.State_Selected:
            painter.setPen(QPen(self.highlighted_text))
        painter.drawText(text_rect, text_flags, text)
        if mark:
            hrect = QRect(text_rect.right(), text_rect.top(), text_rect.height(), text_rect.height())
            painter.fillRect(hrect, QColor('#ffffaa'))
            painter.drawText(hrect, Qt.AlignCenter, mark)
        elif hovering:
            hrect = QRect(text_rect.right(), text_rect.top(), text_rect.height(), text_rect.height())
            close_hover = index.data(CLOSE_HOVER_ROLE) is True
            if close_hover:
                pen = painter.pen()
                pen.setColor(QColor('red'))
                painter.setPen(pen)
            painter.drawText(hrect, Qt.AlignCenter, '✖ ')
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
            icon = index.data(DECORATION_ROLE)
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
        self.set_data(DISPLAY_ROLE, tab.title() or _('Loading...'))
        self.set_data(DECORATION_ROLE, missing_icon())
        self.set_data(ANGLE_ROLE, 0)
        self.set_data(HOVER_ROLE, False)
        self.tabref = weakref.ref(tab)
        tab.title_changed.connect(partial(self.set_data, DISPLAY_ROLE))
        tab.icon_changed.connect(self.icon_changed)
        tab.loading_status_changed.connect(self._loading_status_changed)

    def _loading_status_changed(self, loading):
        self.set_data(ANGLE_ROLE, 0)
        self.set_data(LOADING_ROLE, loading)
        self.loading_status_changed(self, loading)

    def icon_changed(self, new_icon):
        if new_icon.isNull():
            new_icon = missing_icon()
        self.set_data(DECORATION_ROLE, new_icon)

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
    tab_close_requested = pyqtSignal(object)

    def __init__(self, parent):
        QTreeWidget.__init__(self, parent)
        pal = self.palette()
        pal.setColor(pal.Highlight, pal.color(pal.Base))
        pal.setColor(pal.HighlightedText, pal.color(pal.Text))
        self.setPalette(pal)
        self.setIconSize(QSize(ICON_SIZE, ICON_SIZE))
        self.setAutoScrollMargin(ICON_SIZE * 2)
        self.setAnimated(True)
        self.setHeaderHidden(True)
        self.setSelectionMode(self.SingleSelection)
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
        self.setMouseTracking(True)
        self._last_item = lambda: None
        self.itemEntered.connect(lambda item, col: item.set_data(HOVER_ROLE, True))
        self.setCursor(Qt.PointingHandCursor)
        self.viewport().installEventFilter(self)

    def eventFilter(self, widget, event):
        if widget is self.viewport():
            etype = event.type()
            item = last_item = self._last_item()
            if etype == QEvent.MouseMove:
                pos = event.pos()
                item = self.itemAt(pos)
                if item is not None:
                    item.set_data(CLOSE_HOVER_ROLE, self.over_close(item, pos))
            elif etype == QEvent.Leave:
                item = None
            if item is not last_item:
                if last_item is not None:
                    last_item.set_data(HOVER_ROLE, False)
                    last_item.set_data(CLOSE_HOVER_ROLE, False)
                self._last_item = (lambda: None) if item is None else weakref.ref(item)
        return QTreeWidget.eventFilter(self, widget, event)

    def over_close(self, item, pos):
        rect = self.visualItemRect(item)
        rect.setLeft(rect.right() - rect.height())
        return rect.contains(pos)

    def mouseReleaseEvent(self, ev):
        if ev.button() == Qt.LeftButton:
            item = self.itemAt(ev.pos())
            if item is not None:
                if self.over_close(item, ev.pos()):
                    tab = item.tabref()
                    if tab is not None:
                        self.tab_close_requested.emit(tab)
                        ev.accept()
                        return
        return QTreeWidget.mouseReleaseEvent(self, ev)

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

    def remove_tab(self, tab):
        item = self.item_for_tab(tab)
        if item is not None:
            p = item.parent() or self.invisibleRootItem()
            p.removeChild(item)

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

    def _activate_item(self, item, tab, expand=True):
        self.scrollToItem(item)
        self.tab_activated.emit(item.tab)
        if expand and not item.isExpanded():
            item.setExpanded(True)

    def activate_tab(self, text):
        text = text.strip()
        for item in self:
            tab = item.tab
            if tab is not None and item.text(0).strip() == text:
                self._activate_item(item, tab)
                return True

    def next_tab(self, forward=True):
        tabs = self if forward else reversed(tuple(self))
        found = self.current_item is None
        item = None
        for item in tabs:
            tab = item.tab
            if found and tab is not None:
                self._activate_item(item, tab)
                return True
            if self.current_item == item:
                found = True
        tabs = self if forward else reversed(tuple(self))
        for item in tabs:
            tab = item.tab
            if tab is not None:
                self._activate_item(item, tab)
                return True
        return False

    def current_changed(self, tab):
        if self.current_item is not None:
            self.current_item.set_data(Qt.FontRole, None)
            self.current_item = None
        item = self.item_for_tab(tab)
        if item is not None:
            self.current_item = item
            item.set_data(Qt.FontRole, self.emphasis_font)

    def mark_tabs(self, unmark=False):
        for item in self:
            item.set_data(MARK_ROLE, None)
        if not unmark:
            names = iter(mark_map)
            item = self.topLevelItem(0)
            while item is not None:
                item.set_data(MARK_ROLE, next(names))
                item = self.itemBelow(item)

    def activate_marked_tab(self, key):
        m = mark_rmap.get(key)
        if m is None:
            return False
        for item in self:
            if item.data(0, MARK_ROLE) == m:
                tab = item.tab
                if tab is not None:
                    self._activate_item(item, tab)
                    return True
        return False
