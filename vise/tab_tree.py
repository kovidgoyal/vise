#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2015, Kovid Goyal <kovid at kovidgoyal.net>

import string
import weakref
from collections import OrderedDict
from functools import partial
from gettext import gettext as _

from PyQt5.Qt import (QApplication, QBrush, QColor, QEvent, QFont, QIcon,
                      QMenu, QPainter, QPainterPath, QPen, QPixmap, QRect,
                      QRectF, QSize, QStyle, QStyledItemDelegate, Qt, QTimer,
                      QTreeWidget, QTreeWidgetItem, pyqtSignal)

from .config import color
from .downloads import DOWNLOAD_ICON_NAME, DOWNLOADS_URL
from .resources import get_data_as_path, get_icon
from .utils import RotatingIcon, elided_text
from .welcome import WELCOME_URL, welcome_icon

LOADING_ROLE = Qt.ItemDataRole.UserRole
HOVER_ROLE = LOADING_ROLE + 1
CLOSE_HOVER_ROLE = HOVER_ROLE + 1
MARK_ROLE = CLOSE_HOVER_ROLE + 1
DISPLAY_ROLE = MARK_ROLE + 1
DECORATION_ROLE = DISPLAY_ROLE + 1
URL_ROLE = DECORATION_ROLE + 1
MUTED_ROLE = URL_ROLE + 1
ICON_SIZE = 24
NUM_FRAMES = 120


_missing_icon = None

mark_map = OrderedDict()
for x in string.digits + string.ascii_uppercase:
    mark_map[x] = getattr(Qt, 'Key_' + x)
for x in string.ascii_uppercase:
    mark_map[x] = getattr(Qt, 'Key_' + x) | Qt.KeyboardModifier.ShiftModifier
mark_rmap = {int(v): k for k, v in mark_map.items()}


def missing_icon():
    global _missing_icon
    if _missing_icon is None:
        p = QPixmap(ICON_SIZE, ICON_SIZE)
        p.fill(Qt.GlobalColor.transparent)
        painter = QPainter(p)
        pal = QApplication.instance().palette()
        painter.setPen(QPen(pal.color(pal.Text), 0, Qt.PenStyle.DashLine))
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
        self.frames = RotatingIcon(frames=NUM_FRAMES, icon_size=ICON_SIZE).frames
        self.frame_number = 0
        self.dark = pal.color(pal.Text)
        self.light = pal.color(pal.Base)
        self.highlighted_text = pal.color(pal.HighlightedText)
        self.current_background = QBrush(QColor(color('tab tree current background', Qt.GlobalColor.lightGray)))

    def sizeHint(self, option, index):
        return QSize(300, ICON_SIZE + 2 * self.MARGIN)

    def paint(self, painter, option, index):
        QStyledItemDelegate.paint(self, painter, option, index)
        hovering = index.data(HOVER_ROLE) is True
        painter.save()
        painter.setRenderHint(painter.Antialiasing)
        painter.setRenderHint(painter.SmoothPixmapTransform)
        rect = option.rect
        is_current = index.data(Qt.ItemDataRole.FontRole) is not None
        if not hovering and is_current:
            qpp = QPainterPath()
            qpp.addRoundedRect(QRectF(rect), 6, 6)
            painter.fillPath(qpp, self.current_background)
        icon_rect = QRect(rect.left() + self.MARGIN, rect.top() + self.MARGIN, ICON_SIZE, ICON_SIZE)
        left = icon_rect.right() + 2 * self.MARGIN
        text_rect = QRect(left, icon_rect.top(), rect.width() - left + rect.left(), icon_rect.height())
        mark = index.data(MARK_ROLE)
        if hovering or mark:
            text_rect.adjust(0, 0, -text_rect.height(), 0)
        text = index.data(DISPLAY_ROLE) or ''
        muted = index.data(MUTED_ROLE)
        if muted:
            mc = get_icon('volume-off.svg').pixmap(ICON_SIZE, ICON_SIZE)
            painter.drawPixmap(QRect(text_rect.left(), text_rect.top(), ICON_SIZE, text_rect.height()), mc, mc.rect())
            text_rect.adjust(ICON_SIZE, 0, 0, 0)
        font = index.data(Qt.ItemDataRole.FontRole)
        if font:
            painter.setFont(font)
        text_flags = Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft | Qt.TextFlag.TextSingleLine
        text = elided_text(text, font, text_rect.width(), 'right')
        if option.state & QStyle.StateFlag.State_Selected:
            painter.setPen(QPen(self.highlighted_text))
        painter.drawText(text_rect, text_flags, text)
        if mark:
            hrect = QRect(text_rect.right(), text_rect.top(), text_rect.height(), text_rect.height())
            painter.fillRect(hrect, QColor('#ffffaa'))
            painter.drawText(hrect, Qt.AlignmentFlag.AlignCenter, mark)
        elif hovering:
            hrect = QRect(text_rect.right(), text_rect.top(), text_rect.height(), text_rect.height())
            close_hover = index.data(CLOSE_HOVER_ROLE) is True
            if close_hover:
                pen = painter.pen()
                pen.setColor(QColor('red'))
                painter.setPen(pen)
            painter.drawText(hrect, Qt.AlignmentFlag.AlignCenter, '✖ ')
        if index.data(LOADING_ROLE):
            lc = self.frames[self.frame_number]
            painter.drawPixmap(icon_rect.topLeft(), lc)
        else:
            icurl = index.data(URL_ROLE)
            if icurl == WELCOME_URL:
                icon = welcome_icon()
            elif icurl == DOWNLOADS_URL:
                icon = get_icon(DOWNLOAD_ICON_NAME)
            else:
                icon = index.data(DECORATION_ROLE)
            icon.paint(painter, icon_rect)
        painter.restore()

    def next_loading_frame(self):
        self.frame_number = (self.frame_number + 1) % NUM_FRAMES


tab_item_counter = 0


class TabItem(QTreeWidgetItem):

    def __init__(self, tab, loading_status_changed):
        global tab_item_counter
        QTreeWidgetItem.__init__(self)
        tab_item_counter += 1
        self.uid = tab_item_counter
        self.loading_status_changed = loading_status_changed
        self.setFlags(self.flags() | Qt.ItemFlag.ItemIsDragEnabled | Qt.ItemFlag.ItemIsDropEnabled)
        self.tabref = lambda: None
        self.set_view(tab)

    def set_view(self, tab):
        self.set_data(LOADING_ROLE, False)
        self.set_data(DISPLAY_ROLE, tab.title() or _('Loading...'))
        self.set_data(DECORATION_ROLE, missing_icon())
        self.set_data(HOVER_ROLE, False)
        self.set_data(URL_ROLE, '')
        self.set_data(MUTED_ROLE, False)
        self.tabref = weakref.ref(tab)
        tab.title_changed.connect(self.set_display_role)
        tab.icon_changed.connect(self.icon_changed)
        tab.loading_status_changed.connect(self._loading_status_changed)
        tab.audio_muted_changed.connect(self.audio_muted_changed)
        tab.urlChanged.connect(self.set_url_role)

    def set_display_role(self, text):
        self.set_data(DISPLAY_ROLE, text)

    def set_url_role(self, url):
        self.set_data(URL_ROLE, url)

    def _loading_status_changed(self, loading):
        self.set_data(LOADING_ROLE, loading)
        self.loading_status_changed(self, loading)

    def audio_muted_changed(self, muted):
        self.set_data(MUTED_ROLE, muted)

    def icon_changed(self, new_icon):
        if new_icon.isNull():
            new_icon = missing_icon()
        self.set_data(DECORATION_ROLE, new_icon)

    @property
    def tab(self):
        return self.tabref()

    @property
    def view_id(self):
        return getattr(self.tab, 'view_id', -1)

    @property
    def current_title(self):
        return self.data(0, DISPLAY_ROLE)

    @property
    def current_icon(self):
        return self.data(0, DECORATION_ROLE)

    def __iter__(self):
        for i in range(self.childCount()):
            child = self.child(i)
            yield child
            yield from child

    def set_data(self, role, data):
        try:
            self.setData(0, role, data)
        except RuntimeError:
            pass

    def __hash__(self):
        return self.uid

    def has_ancestor(self, a):
        p = self.parent()
        while p:
            if p is a:
                return True
            p = p.parent()
        return False


class TabTree(QTreeWidget):

    tab_activated = pyqtSignal(object)
    tab_close_requested = pyqtSignal(object)
    delete_tabs = pyqtSignal(object)

    def __init__(self, parent):
        QTreeWidget.__init__(self, parent)
        self.deleted_parent_map = {}
        pal = self.palette()
        pal.setColor(pal.Highlight, pal.color(pal.Base))
        pal.setColor(pal.HighlightedText, pal.color(pal.Text))
        self.setPalette(pal)
        self.setStyleSheet('''
                QTreeView {
                    background: BG;
                    color: FG;
                    border: none;
                }

                QTreeView::item {
                    border: 1px solid transparent;
                    padding-top:0.5ex;
                    padding-bottom:0.5ex;
                }

                QTreeView::item:hover {
                    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 GS, stop: 1 GE);
                    border: 1px solid BC;
                    border-radius: 6px;
                }

                QTreeView::branch {
                    background: darkGray;
                }

                QTreeView::branch:has-children:!has-siblings:closed, QTreeView::branch:closed:has-children:has-siblings {
                    image: url(CLOSED);
                }

                QTreeView::branch:open:has-children:!has-siblings, QTreeView::branch:open:has-children:has-siblings  {
                    image: url(OPEN);
                }
        '''.replace(
            'CLOSED', get_data_as_path('images/tree-closed.svg')).replace(
            'OPEN', get_data_as_path('images/tree-open.svg')).replace(
            'BG', color('tab tree background', 'palette(window)')).replace(
            'FG', color('tab tree foreground', 'palette(window-text)')).replace(
            'GS', color('tab tree hover gradient start', '#e7effd')).replace(
            'GE', color('tab tree hover gradient end', '#cbdaf1')).replace(
            'BC', color('tab tree hover border', '#bfcde4'))
        )
        self.setIconSize(QSize(ICON_SIZE, ICON_SIZE))
        self.setAutoScrollMargin(ICON_SIZE * 2)
        self.setAnimated(True)
        self.setHeaderHidden(True)
        self.setSelectionMode(self.SingleSelection)
        self.setDragEnabled(True)
        self.viewport().setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setDragDropMode(self.InternalMove)
        self.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.invisibleRootItem().setFlags(Qt.ItemFlag.ItemIsDragEnabled | Qt.ItemFlag.ItemIsDropEnabled | self.invisibleRootItem().flags())
        self.itemClicked.connect(self.item_clicked)
        self.current_item = None
        self.emphasis_font = QFont(self.font())
        self.emphasis_font.setBold(True)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.loading_items = set()
        self.delegate = TabDelegate(self)
        self.setItemDelegate(self.delegate)
        self.loading_animation_timer = t = QTimer(self)
        t.setInterval(1000 // 60)
        t.timeout.connect(self.repaint_loading_items)
        self.setMouseTracking(True)
        self._last_item = lambda: None
        self.itemEntered.connect(self.item_entered)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.viewport().installEventFilter(self)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def item_entered(self, item, col):
        item.set_data(HOVER_ROLE, True)

    def show_context_menu(self, pos):
        item = self.itemAt(pos)
        if not item:
            return
        m = QMenu(self)
        m.addAction(_('Close tabs to the bottom'), partial(self.close_tabs_to_bottom, item))
        m.addAction(_('Close other tabs'), partial(self.close_other_tabs, item))
        m.addAction(_('Close this tree'), partial(self.close_tree, item))
        m.exec_(self.mapToGlobal(pos))

    def close_tabs_to_bottom(self, item_or_tab):
        item = item_or_tab if isinstance(item_or_tab, TabItem) else self.item_for_tab(item_or_tab)
        if item:
            tabs_to_delete = []
            found_self = False
            for i in tuple(self):
                found_self = found_self or i is item
                if found_self:
                    parent = i.parent() or self.invisibleRootItem()
                    self.deleted_parent_map[i.view_id] = (getattr(parent, 'view_id', -1), parent.indexOfChild(i))
                    parent.removeChild(i)
                    tabs_to_delete.append(i.tab)
            self.delete_tabs.emit(tuple(filter(None, tabs_to_delete)))

    def close_other_tabs(self, item_or_tab):
        item = item_or_tab if isinstance(item_or_tab, TabItem) else self.item_for_tab(item_or_tab)
        if item:
            tabs_to_delete = []
            keep_children = not item.isExpanded()
            for i in tuple(self):
                if i is not item and (not keep_children or not i.has_ancestor(item)):
                    p = i.parent() or self.invisibleRootItem()
                    self.deleted_parent_map[i.view_id] = (getattr(p, 'view_id', -1), p.indexOfChild(i))
                    p.removeChild(i)
                    tabs_to_delete.append(i.tab)
            p = (item.parent() or self.invisibleRootItem())
            self.deleted_parent_map[item.view_id] = (getattr(p, 'view_id', -1), p.indexOfChild(item))
            p.removeChild(item)
            self.addTopLevelItem(item)
            self.delete_tabs.emit(tuple(filter(None, tabs_to_delete)))

    def close_tree(self, item_or_tab):
        item = item_or_tab if isinstance(item_or_tab, TabItem) else self.item_for_tab(item_or_tab)
        if item:
            p = (item.parent() or self.invisibleRootItem())
            self.deleted_parent_map[item.view_id] = (getattr(p, 'view_id', -1), p.indexOfChild(item))
            p.removeChild(item)
            tabs_to_delete = [item.tab]
            for i in tuple(item):
                p = i.parent()
                self.deleted_parent_map[i.view_id] = (getattr(p, 'view_id', -1), p.indexOfChild(i))
                p.removeChild(i)
                tabs_to_delete.append(i.tab)
            self.delete_tabs.emit(tuple(filter(None, tabs_to_delete)))

    def eventFilter(self, widget, event):
        if widget is self.viewport():
            etype = event.type()
            item = last_item = self._last_item()
            if etype == QEvent.Type.MouseMove:
                pos = event.pos()
                item = self.itemAt(pos)
                if item is not None:
                    item.set_data(CLOSE_HOVER_ROLE, self.over_close(item, pos))
            elif etype == QEvent.Type.Leave:
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
        if ev.button() == Qt.MouseButton.LeftButton:
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
            if isinstance(item, TabItem):
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

    def undelete_tab(self, tab, stab):
        old_tab_id = stab['view_id']
        parent_id, pos = self.deleted_parent_map.pop(old_tab_id, (None, None))
        parent = self.invisibleRootItem()
        item = self.item_for_tab(tab)
        if parent_id is not None and parent_id >= 0:
            for q in self:
                if q.view_id == parent_id:
                    parent = q
                    break
        (item.parent() or self.invisibleRootItem()).removeChild(item)
        if pos > -1 and pos < parent.childCount():
            parent.insertChild(pos, item)
        else:
            parent.addChild(item)
        self.scrollToItem(item)

    def replace_view_in_tab(self, tab, replacement):
        item = self.item_for_tab(tab)
        if item is not None:
            item.set_view(replacement)

    def remove_tab(self, tab):
        item = self.item_for_tab(tab)
        closing_current_tab = item is self.current_item
        children_to_close = ()
        if item is not None:
            p = item.parent() or self.invisibleRootItem()
            if item.isExpanded():
                if closing_current_tab:
                    self.next_tab(wrap=False)
                surviving_children = tuple(item.takeChildren())
                if surviving_children:
                    p.insertChild(p.indexOfChild(item), surviving_children[0])
                    tuple(map(surviving_children[0].addChild, surviving_children[1:]))
                    surviving_children[0].setExpanded(True)
            else:
                children_to_close = tuple(i.tab for i in item.takeChildren())
                if closing_current_tab:
                    self.next_tab(wrap=False)
            self.deleted_parent_map[item.view_id] = (getattr(p, 'view_id', -1), p.indexOfChild(item))
            p.removeChild(item)
        return children_to_close + (tab,)

    def loading_status_changed(self, item, loading):
        if loading:
            self.loading_items.add(item)
            # this is disabled as it causes loading to become very slow
            # when many tabs are loading, probably need to move the delegate
            # implementation into native code
            # self.loading_animation_timer.start()
        else:
            self.loading_items.discard(item)
            if not self.loading_items:
                self.loading_animation_timer.stop()

    def repaint_loading_items(self):
        self.delegate.next_loading_frame()
        self.viewport().update()

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

    def item_for_text(self, text):
        text = text.strip()
        for item in self:
            tab = item.tab
            if tab is not None and item.data(0, DISPLAY_ROLE).strip() == text:
                return item

    def activate_tab(self, text):
        item = self.item_for_text(text)
        if item is not None:
            self._activate_item(item, item.tab)
            return True

    def next_tab(self, forward=True, wrap=True):
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
        if wrap:
            tabs = self if forward else reversed(tuple(self))
        else:
            tabs = reversed(tuple(self)) if forward else self
        for item in tabs:
            tab = item.tab
            if tab is not None and item is not self.current_item:
                self._activate_item(item, tab)
                return True
        return False

    def current_changed(self, tab):
        if self.current_item is not None:
            self.current_item.set_data(Qt.ItemDataRole.FontRole, None)
            self.current_item = None
        item = self.item_for_tab(tab)
        if item is not None:
            self.current_item = item
            item.set_data(Qt.ItemDataRole.FontRole, self.emphasis_font)

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

    def serialize_state(self):
        ans = {'children': []}

        def process_node(node, sparent=ans):
            for child in (node.child(i) for i in range(node.childCount())):
                view_id = child.view_id
                if view_id > -1:
                    sparent['children'].append({'view_id': view_id, 'is_expanded': child.isExpanded(), 'children': []})
                    process_node(child, sparent['children'][-1])
        process_node(self.invisibleRootItem())
        return ans

    def unserialize_state(self, state, tab):
        self.item_for_tab(tab).setExpanded(state['is_expanded'])
