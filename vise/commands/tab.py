#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2015, Kovid Goyal <kovid at kovidgoyal.net>

import weakref
from gettext import gettext as _

from PyQt5.Qt import QApplication, Qt, QIcon, QPoint

from . import Command
from ..utils import make_highlighted_text


class CompletionCandidate:

    def __init__(self, tab_item, substrings):
        self.tabref = weakref.ref(tab_item)

        def get_positions(text):
            ans = set()
            text = text.lower()
            for ss in substrings:
                idx = text.find(ss.lower())
                if idx > -1:
                    ans |= set(range(idx, idx + len(ss)))
            return sorted(ans)

        text = tab_item.text(0)
        self.text = make_highlighted_text(text, get_positions(text))

    @property
    def value(self):
        t = self.tabref()
        if t is None:
            return ''
        return t.text(0)

    @property
    def icon(self):
        t = self.tabref()
        if t is None:
            return QIcon()
        return t.data(0, Qt.DecorationRole)

    def adjust_size_hint(self, option, ans):
        ans.setHeight(max(option.decorationSize.height() + 6, ans.height()))

    def draw_item(self, painter, style, option):
        option.features |= option.HasDecoration
        option.icon = self.icon
        text_rect = style.subElementRect(style.SE_ItemViewItemText, option, None)
        if not option.icon.isNull():
            icon_rect = style.subElementRect(style.SE_ItemViewItemDecoration, option, None)
            option.icon.paint(painter, icon_rect, alignment=Qt.AlignBottom | Qt.AlignHCenter)
        option.icon = QIcon()
        x, y = text_rect.x(), text_rect.y()
        y += (text_rect.height() - self.text.size().height()) // 2
        painter.drawStaticText(QPoint(x, y), self.text)


def tab_matches(item, substrings):
    text = item.text(0).lower()
    for ss in substrings:
        if ss.lower() not in text:
            return False
    return True


class SwitchToTab(Command):

    names = {'tab'}

    def completions(self, cmd, prefix):
        tt = QApplication.instance().activeWindow().tab_tree
        substrings = prefix.split(' ')
        items = [CompletionCandidate(item, substrings) for item in tt if tab_matches(item, substrings)]
        return items

    def __call__(self, cmd, rest, window):
        if not rest.strip():
            return
        tt = window.tab_tree
        if not tt.activate_tab(rest.strip()):
            window.statusBar().showMessage(_('No tab matching: ') + rest.strip(), 5000)


class CloseOtherTabs(SwitchToTab):

    names = {'tabonly'}

    def __call__(self, cmd, rest, window):
        if not rest.strip():
            ct = window.current_tab
            if ct:
                window.tab_tree.close_other_tabs(ct)
            return
        tt = window.tab_tree
        item = tt.item_for_text(rest.strip())
        if item is None:
            window.statusBar().showMessage(_('No tab matching: ') + rest.strip(), 5000)
        else:
            tt.close_other_tabs(item)


class CloseToBottom(CloseOtherTabs):

    names = {'closetobottom'}

    def __call__(self, cmd, rest, window):
        if not rest.strip():
            ct = window.current_tab
            if ct:
                window.tab_tree.close_tabs_to_bottom(ct)
            return
        tt = window.tab_tree
        item = tt.item_for_text(rest.strip())
        if item is None:
            window.statusBar().showMessage(_('No tab matching: ') + rest.strip(), 5000)
        else:
            tt.close_tabs_to_bottom(item)
