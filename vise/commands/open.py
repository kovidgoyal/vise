#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2015, Kovid Goyal <kovid at kovidgoyal.net>

from contextlib import closing

from PyQt6.QtCore import QPoint, QUrl, QUrlQuery
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QApplication, QStyleOptionViewItem, QStyle

from ..places import places
from ..utils import make_highlighted_text, parse_url
from . import Command


def search_engine(q):
    ans = QUrl('https://google.com/search')
    # ans = QUrl('https://duckduckgo.com/lite')
    # ans = QUrl('https://duckduckgo.com')
    qq = QUrlQuery()
    qq.addQueryItem('q', q)
    ans.setQuery(qq)
    return ans


class CompletionCandidate:

    def __init__(self, place_id, url, title, substrings):
        self.value = url
        self.place_id = place_id

        def get_positions(text):
            ans = set()
            text = text.lower()
            for ss in substrings:
                idx = text.find(ss.lower())
                if idx > -1:
                    ans |= set(range(idx, idx + len(ss)))
            return sorted(ans)

        self.left = make_highlighted_text(url, get_positions(url))
        self.right = make_highlighted_text(title, get_positions(title))
        self._icon = None

    def adjust_size_hint(self, option, ans):
        ans.setHeight(max(option.decorationSize.height() + 6, ans.height()))

    @property
    def icon(self):
        if self._icon is None:
            self._icon = QIcon()
            url = places.favicon_url(self.place_id)
            if url is not None:
                f = QApplication.instance().disk_cache.data(QUrl(url))
                if f is not None:
                    with closing(f):
                        raw = f.readAll()
                    p = QPixmap()
                    p.loadFromData(raw)
                    if not p.isNull():
                        self._icon.addPixmap(p)
        return self._icon

    def __repr__(self):
        return self.value

    def draw_item(self, painter, style, option):
        option.features |= QStyleOptionViewItem.ViewItemFeature.HasDecoration
        option.icon = self.icon
        text_rect = style.subElementRect(QStyle.SubElement.SE_ItemViewItemText, option, None)
        x, y = text_rect.x(), text_rect.y()
        y += int(text_rect.height() - self.left.size().height()) // 2
        if not option.icon.isNull():
            icon_rect = style.subElementRect(QStyle.SubElement.SE_ItemViewItemDecoration, option, None)
            icon_rect.setTop(y), icon_rect.setBottom(int(text_rect.bottom()))
            option.icon.paint(painter, icon_rect)
        option.icon = QIcon()
        width = (text_rect.width() // 2) - 10
        painter.setClipRect(x, int(text_rect.y()), int(width), int(text_rect.height()))
        painter.drawStaticText(QPoint(int(x), int(y)), self.left)
        painter.setClipRect(text_rect)
        x += width + 20
        painter.drawStaticText(QPoint(int(x), int(y)), self.right)


class Open(Command):

    names = {'open', 'tabopen', 'topen', 'wopen', 'winopen', 'popen', 'privateopen', 'copyurl'}

    def completions(self, cmd, prefix):
        substrings = prefix.split(' ')
        items = [CompletionCandidate(place_id, url, title, substrings) for place_id, url, title in places.substring_matches(substrings)]
        return items

    def __call__(self, cmd, rest, window):
        if cmd == 'copyurl':
            QApplication.clipboard().setText(rest)
            window.save_url_in_places(parse_url(rest))
            return
        rest = rest.strip()
        if rest.startswith('http://') or rest.startswith('https://') or rest.startswith('vise:') or rest.startswith('chrome://'):
            is_search = False
        else:
            is_search = rest.strip() and (' ' in rest or '.' not in rest.strip('.'))
        url = search_engine(rest) if is_search else parse_url(rest)
        if cmd in {'open', 'topen', 'tabopen'}:
            window.open_url(url, in_current_tab=cmd == 'open', switch_to_tab=True)
        else:
            window = QApplication.instance().new_window(is_private=cmd.startswith('p'))
            window.show()
            window.open_url(url, in_current_tab=True)
