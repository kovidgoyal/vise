#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2015, Kovid Goyal <kovid at kovidgoyal.net>

from gettext import gettext as _


from .commands import Command
from .commands.open import Open  # noqa
from .commands.tab import SwitchToTab, CloseOtherTabs # noqa


class Close(Command):

    names = {'close', 'wclose', 'winclose'}

    def __call__(self, cmd, rest, window):
        if cmd == 'close':
            window.close_tab()
        else:
            window.close()


class PasswordManager(Command):

    names = {'password-manager'}

    def __call__(self, cmd, rest, window):
        from PyQt5.Qt import QApplication
        from .passwd.db import password_db
        from .passwd.gui import PasswordManager
        app = QApplication.instance()
        if app.ask_for_master_password(window):
            d = PasswordManager(password_db, parent=window)
            d.exec_()


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
        common = [name for name in command_map if name.startswith(cmd)]
        if len(common) == 1:
            obj = command_map[common[0]]
        else:
            window.statusBar().showMessage(_('Unknown command: ') + cmd, 5000)
            return
    obj(cmd, rest, window)
