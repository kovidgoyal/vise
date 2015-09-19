#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2015, Kovid Goyal <kovid at kovidgoyal.net>

from gettext import gettext as _


from .commands import Command
from .commands.open import Open  # noqa


class Close(Command):

    names = {'close', 'wclose', 'winclose'}


class SwitchToTab(Command):

    names = {'tab'}

all_commands = {x() for x in locals().values() if x is not Command and type(x) is type and issubclass(x, Command)}
command_map = {}
all_command_names = set()
for cmd in all_commands:
    all_command_names |= cmd.names
    for name in cmd.names:
        if name in command_map:
            raise ValueError('The command name %r is used twice' % name)
        command_map[name] = cmd
del cmd, name


def run_command(window, text):
    cmd, rest = text.partition(' ')[::2]
    obj = command_map.get(cmd)
    if obj is None:
        window.statusBar().showMessage(_('Unknown command: ') + cmd, 5000)
        return
    obj(cmd, rest, window)
