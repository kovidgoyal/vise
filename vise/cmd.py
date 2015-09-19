#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2015, Kovid Goyal <kovid at kovidgoyal.net>

from PyQt5.Qt import QPoint

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

        def __init__(self, url, title, substrings):
            self.value = url

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

        def __repr__(self):
            return self.value

        def draw_item(self, painter, icon_rect, text_rect, margin):
            x, y = text_rect.x(), text_rect.y() + margin
            width = (text_rect.width() // 2) - 10
            painter.setClipRect(x, text_rect.y(), width, text_rect.height())
            painter.drawStaticText(QPoint(x, y), self.left)
            painter.setClipRect(text_rect)
            x += width + 20
            painter.drawStaticText(QPoint(x, y), self.right)

    def completions(self, cmd, prefix):
        substrings = prefix.split(' ')
        items = [Open.Candidate(url, title, substrings) for url, title in places.substring_matches(substrings)]
        return items


class Close(Command):

    names = {'close', 'wclose', 'winclose'}


class SwitchToTab(Command):

    names = {'tab'}

all_commands = {x() for x in locals().values() if x is not Command and type(x) is type and issubclass(x, Command)}
