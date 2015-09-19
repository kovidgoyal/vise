#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2015, Kovid Goyal <kovid at kovidgoyal.net>

from contextlib import closing
from gettext import gettext as _

from PyQt5.Qt import QPoint, QApplication, QIcon, QPixmap, QUrl, Qt

from .places import places
from .utils import make_highlighted_text


class Command:

    names = set()

    def __call__(self, cmd, rest, window):
        raise NotImplementedError()

    def __repr__(self):
        return 'Command(%s)' % self.__class__.__name__

    def completions(self, cmd, prefix):
        return ()


class Open(Command):

    names = {'open', 'tabopen', 'topen', 'wopen', 'winopen', 'popen', 'privateopen'}

    class Candidate:

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
                    f = QApplication.instance().disk_cache.data(QUrl(str(url)))  # Bug in PyQt neccessitates call to str()
                    if f is not None:
                        with closing(f):
                            raw = bytes(f.readAll())
                            p = QPixmap()
                            p.loadFromData(raw)
                            if not p.isNull():
                                self._icon.addPixmap(p)
            return self._icon

        def __repr__(self):
            return self.value

        def draw_item(self, painter, style, option):
            option.features |= option.HasDecoration
            option.icon = self.icon
            text_rect = style.subElementRect(style.SE_ItemViewItemText, option)
            if not option.icon.isNull():
                icon_rect = style.subElementRect(style.SE_ItemViewItemDecoration, option)
                option.icon.paint(painter, icon_rect, alignment=Qt.AlignBottom | Qt.AlignHCenter)
            option.icon = QIcon()
            x, y = text_rect.x(), text_rect.y()
            y += (text_rect.height() - self.left.size().height()) // 2
            width = (text_rect.width() // 2) - 10
            painter.setClipRect(x, text_rect.y(), width, text_rect.height())
            painter.drawStaticText(QPoint(x, y), self.left)
            painter.setClipRect(text_rect)
            x += width + 20
            painter.drawStaticText(QPoint(x, y), self.right)

    def completions(self, cmd, prefix):
        substrings = prefix.split(' ')
        items = [Open.Candidate(place_id, url, title, substrings) for place_id, url, title in places.substring_matches(substrings)]
        return items


class Close(Command):

    names = {'close', 'wclose', 'winclose'}


class SwitchToTab(Command):

    names = {'tab'}

all_commands = {x() for x in locals().values() if x is not Command and type(x) is type and issubclass(x, Command)}


def run_command(window, text):
    cmd, rest = text.partition(' ')[::2]
    obj = all_commands.get(cmd)
    if obj is None:
        window.statusBar().showMessage(_('Unknown command: ') + cmd, 5000)
        return
    obj(cmd, rest, window)
