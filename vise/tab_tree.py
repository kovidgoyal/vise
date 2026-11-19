#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2015, Kovid Goyal <kovid at kovidgoyal.net>

# The tab tree is a pure data model, it holds the hierarchical relationship
# between tabs. Tabs are displayed to the user via the tab overlay (see
# tab_overlay.py) organized into groups, where each group is a top level node
# of the tree with all its descendants.

import string
import weakref
from contextlib import closing
from gettext import gettext as _

from PyQt6.QtCore import QObject, Qt, QUrl, pyqtSignal
from PyQt6.QtGui import QIcon, QPainter, QPalette, QPen, QPixmap
from PyQt6.QtWidgets import QApplication

from .downloads import DOWNLOAD_ICON_NAME, DOWNLOADS_URL
from .resources import get_icon
from .welcome import WELCOME_URL, welcome_icon

ICON_SIZE = 24


_missing_icon = None
mark_map = {}
for x in string.digits + string.ascii_uppercase:
    mark_map[x] = getattr(Qt.Key, 'Key_' + x)
for x in string.ascii_uppercase:
    mark_map[x] = getattr(Qt.Key, 'Key_' + x) | Qt.KeyboardModifier.ShiftModifier
mark_rmap = {v.toCombined() if hasattr(v, 'toCombined') else v.value: k for k, v in mark_map.items()}


def missing_icon():
    global _missing_icon
    if _missing_icon is None:
        p = QPixmap(ICON_SIZE, ICON_SIZE)
        p.fill(Qt.GlobalColor.transparent)
        painter = QPainter(p)
        pal = QApplication.instance().palette()
        painter.setPen(QPen(pal.color(QPalette.ColorRole.Text), 0, Qt.PenStyle.DashLine))
        margin = 3
        r = p.rect().adjusted(margin, margin, -margin, -margin)
        painter.drawRect(r)
        painter.end()
        _missing_icon = QIcon(p)
    return _missing_icon


tab_item_counter = 0


class TabItem:

    def __init__(self, tab, tree):
        global tab_item_counter
        tab_item_counter += 1
        self.uid = tab_item_counter
        self._parent = None
        self.children = []
        self.treeref = weakref.ref(tree)
        self.tabref = lambda: None
        self.mark = None
        self.set_view(tab)

    def set_view(self, tab):
        self.loading = False
        self.title = tab.title() or _('Loading...')
        self.icon = missing_icon()
        self.qurl = QUrl()
        self.muted = False
        self.tabref = weakref.ref(tab)
        tab.title_changed.connect(self.set_title)
        tab.icon_changed.connect(self.icon_changed)
        tab.loading_status_changed.connect(self._loading_status_changed)
        tab.audio_muted_changed.connect(self.audio_muted_changed)
        tab.urlChanged.connect(self.set_url)
        self.url_for_last_non_null_icon = None
        self.url_when_current_icon_was_set = None

    def notify(self):
        tree = self.treeref()
        if tree is not None:
            tree.item_changed(self)

    def set_title(self, text):
        self.title = text or ''
        self.notify()

    def set_url(self, url):
        self.qurl = QUrl(url)
        if url != self.url_when_current_icon_was_set:
            self.icon_changed(QIcon())
        self.notify()

    def icon_url_changed(self, url):
        dc = QApplication.instance().disk_cache.data(url)
        if dc is not None:
            with closing(dc):
                raw = dc.readAll()
                p = QPixmap()
                p.loadFromData(raw)
                if not p.isNull():
                    ic = QIcon()
                    ic.addPixmap(p)
                    self.icon = ic
                    self.notify()

    def _loading_status_changed(self, loading):
        self.loading = bool(loading)
        tree = self.treeref()
        if tree is not None:
            tree.loading_status_changed(self, self.loading)
        self.notify()

    def audio_muted_changed(self, muted):
        self.muted = bool(muted)
        self.notify()

    def icon_changed(self, new_icon):
        url = None
        if new_icon.isNull():
            tab = self.tab
            if tab is not None:
                url = tab.url()
                if self.url_for_last_non_null_icon is not None and url == self.url_for_last_non_null_icon:
                    return
            new_icon = missing_icon()
            self.url_for_last_non_null_icon = None
        else:
            self.url_for_last_non_null_icon = self.qurl
        self.icon = new_icon
        self.url_when_current_icon_was_set = url
        self.notify()

    @property
    def display_icon(self):
        if self.qurl == WELCOME_URL:
            return welcome_icon()
        if self.qurl == DOWNLOADS_URL:
            return get_icon(DOWNLOAD_ICON_NAME)
        return self.icon

    @property
    def url(self):
        return self.qurl.toDisplayString()

    @property
    def host(self):
        if self.qurl == WELCOME_URL or self.qurl == DOWNLOADS_URL:
            return self.qurl.toDisplayString()
        host = self.qurl.host()
        if not host:
            return self.qurl.toDisplayString()
        port = self.qurl.port()
        return host if port < 0 else f'{host}:{port}'

    @property
    def tab(self):
        return self.tabref()

    @property
    def view_id(self):
        return getattr(self.tab, 'view_id', -1)

    @property
    def current_title(self):
        return self.title

    @property
    def current_icon(self):
        return self.display_icon

    # Tree API {{{
    def parent(self):
        return self._parent

    def childCount(self):
        return len(self.children)

    def child(self, i):
        return self.children[i]

    def indexOfChild(self, child):
        try:
            return self.children.index(child)
        except ValueError:
            return -1

    def addChild(self, child):
        self.insertChild(len(self.children), child)

    def insertChild(self, idx, child):
        child._parent = self if isinstance(self, TabItem) else None
        self.children.insert(idx, child)

    def removeChild(self, child):
        try:
            self.children.remove(child)
        except ValueError:
            pass
        child._parent = None

    def takeChildren(self):
        ans, self.children = self.children, []
        for c in ans:
            c._parent = None
        return ans

    def __iter__(self):
        for child in self.children:
            yield child
            yield from child
    # }}}

    def __hash__(self):
        return self.uid

    def __repr__(self):
        return f'TabItem({self.title!r})'

    def has_ancestor(self, a):
        p = self.parent()
        while p:
            if p is a:
                return True
            p = p.parent()
        return False


class Root(TabItem):

    def __init__(self):
        self.uid = 0
        self._parent = None
        self.children = []


class TabTree(QObject):

    tab_activated = pyqtSignal(object)
    tab_close_requested = pyqtSignal(object)
    delete_tabs = pyqtSignal(object)
    tab_loading_status_changed = pyqtSignal(int, int, bool)
    # Emitted whenever anything about the tree or the items in it changes
    changed = pyqtSignal()

    def __init__(self, parent):
        QObject.__init__(self, parent)
        self.root = Root()
        self.deleted_parent_map = {}
        self.current_item = None
        self.loading_items = set()

    def invisibleRootItem(self):
        return self.root

    def item_changed(self, item):
        self.changed.emit()

    def _parent_of(self, item):
        return item.parent() or self.root

    def _remove_item(self, item):
        p = self._parent_of(item)
        self.deleted_parent_map[item.view_id] = (p.view_id if p is not self.root else -1, p.indexOfChild(item))
        p.removeChild(item)
        self.loading_items.discard(item)
        if item is self.current_item:
            self.current_item = None

    def groups(self):
        ''' Yield (root_item, [root_item, *descendants]) for every top level item '''
        for item in self.root.children:
            yield item, [item] + list(item)

    def close_tabs_to_bottom(self, item_or_tab):
        item = item_or_tab if isinstance(item_or_tab, TabItem) else self.item_for_tab(item_or_tab)
        if item:
            tabs_to_delete = []
            found_self = False
            for i in tuple(self):
                found_self = found_self or i is item
                if found_self:
                    self._remove_item(i)
                    tabs_to_delete.append(i.tab)
            self.changed.emit()
            self.delete_tabs.emit(tuple(filter(None, tabs_to_delete)))

    def close_other_tabs(self, item_or_tab):
        item = item_or_tab if isinstance(item_or_tab, TabItem) else self.item_for_tab(item_or_tab)
        if item:
            tabs_to_delete = []
            for i in tuple(self):
                if i is not item:
                    self._remove_item(i)
                    tabs_to_delete.append(i.tab)
            self._parent_of(item).removeChild(item)
            item.takeChildren()
            self.root.addChild(item)
            self.changed.emit()
            self.delete_tabs.emit(tuple(filter(None, tabs_to_delete)))

    def close_tree(self, item_or_tab):
        item = item_or_tab if isinstance(item_or_tab, TabItem) else self.item_for_tab(item_or_tab)
        if item:
            tabs_to_delete = [item.tab]
            descendants = tuple(item)
            self._remove_item(item)
            for i in descendants:
                self._remove_item(i)
                tabs_to_delete.append(i.tab)
            self.changed.emit()
            self.delete_tabs.emit(tuple(filter(None, tabs_to_delete)))

    def __iter__(self):
        yield from self.root

    def __len__(self):
        return sum(1 for x in self)

    def item_for_tab(self, tab):
        for q in self:
            if q.tab is tab:
                return q

    def add_tab(self, tab, parent=None):
        i = TabItem(tab, self)
        p = None if parent is None else self.item_for_tab(parent)
        (p or self.root).addChild(i)
        self.changed.emit()
        return i

    def undelete_tab(self, tab, stab):
        old_tab_id = stab['view_id']
        parent_id, pos = self.deleted_parent_map.pop(old_tab_id, (None, None))
        parent = self.root
        item = self.item_for_tab(tab)
        if parent_id is not None and parent_id >= 0:
            for q in self:
                if q.view_id == parent_id:
                    parent = q
                    break
        self._parent_of(item).removeChild(item)
        if pos is not None and pos > -1 and pos < parent.childCount():
            parent.insertChild(pos, item)
        else:
            parent.addChild(item)
        self.changed.emit()

    def replace_view_in_tab(self, tab, replacement):
        item = self.item_for_tab(tab)
        if item is not None:
            item.set_view(replacement)
            self.changed.emit()

    def remove_tab(self, tab):
        ' Remove the tab, its children are preserved, with the first child taking its place '
        item = self.item_for_tab(tab)
        if item is not None:
            if item is self.current_item:
                self.next_tab(wrap=False)
            p = self._parent_of(item)
            surviving_children = item.takeChildren()
            if surviving_children:
                p.insertChild(p.indexOfChild(item), surviving_children[0])
                for c in surviving_children[1:]:
                    surviving_children[0].addChild(c)
            self._remove_item(item)
            self.changed.emit()
        return (tab,)

    def loading_status_changed(self, item, loading):
        if loading:
            self.loading_items.add(item)
        else:
            self.loading_items.discard(item)
        self.emit_tab_loading_status_changed()

    def emit_tab_loading_status_changed(self):
        current_loaded = False
        if (i := self.current_item) is not None:
            if (tab := i.tabref()) is not None:
                current_loaded = not tab.loading_in_progress
        self.tab_loading_status_changed.emit(len(self.loading_items), len(self), current_loaded)

    def activate_item(self, item):
        if item is not None and (tab := item.tab) is not None:
            self.tab_activated.emit(tab)
            return True
        return False

    def item_for_text(self, text):
        text = text.strip()
        for item in self:
            tab = item.tab
            if tab is not None and item.title.strip() == text:
                return item

    def activate_tab(self, text):
        item = self.item_for_text(text)
        if item is not None:
            return self.activate_item(item)

    def next_tab(self, forward=True, wrap=True):
        tabs = self if forward else reversed(tuple(self))
        found = self.current_item is None
        item = None
        for item in tabs:
            tab = item.tab
            if found and tab is not None:
                self.activate_item(item)
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
                self.activate_item(item)
                return True
        return False

    def current_changed(self, tab):
        self.current_item = self.item_for_tab(tab)
        self.emit_tab_loading_status_changed()
        self.changed.emit()

    def mark_tabs(self, unmark=False):
        names = iter(mark_map)
        for item in self:
            item.mark = None if unmark else next(names, None)
        self.changed.emit()

    def activate_marked_tab(self, key):
        m = mark_rmap.get(key.toCombined())
        if m is None:
            return False
        for item in self:
            if item.mark == m:
                return self.activate_item(item)
        return False

    def serialize_state(self):
        ans = {'children': []}

        def process_node(node, sparent=ans):
            for child in node.children:
                view_id = child.view_id
                if view_id > -1:
                    sparent['children'].append({'view_id': view_id, 'is_expanded': True, 'children': []})
                    process_node(child, sparent['children'][-1])
        process_node(self.root)
        return ans

    def unserialize_state(self, state, tab):
        pass
