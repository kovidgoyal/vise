#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2015, Kovid Goyal <kovid at kovidgoyal.net>


class Command:

    names = set()

    def __call__(self, cmd, rest, window):
        raise NotImplementedError()

    def __repr__(self):
        return 'Command(%s)' % self.__class__.__name__


class Open(Command):

    names = {'open', 'tabopen', 'topen', 'wopen', 'winopen'}


class Close(Command):

    names = {'close', 'wclose', 'winclose'}

all_commands = {x() for x in locals().values() if x is not Command and type(x) is type and issubclass(x, Command)}
