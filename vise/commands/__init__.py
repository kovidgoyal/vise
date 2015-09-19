#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2015, Kovid Goyal <kovid at kovidgoyal.net>


class Command:

    names = set()

    def __call__(self, cmd, rest, window):
        raise NotImplementedError('This command is not implemented')

    def __repr__(self):
        return 'Command(%s)' % self.__class__.__name__

    def completions(self, cmd, prefix):
        return ()
