#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2015, Kovid Goyal <kovid at kovidgoyal.net>

import os
import tempfile
import pickle
from gettext import gettext as _


from .commands import Command
import vise.commands.open as open_commands
import vise.commands.tab as tab_commands


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


class ClearSearchHighlighting(Command):

    names = {'nohlsearch', 'nohl'}

    def __call__(self, cmd, rest, window):
        from .actions import clear_search_highlighting
        clear_search_highlighting(window)


class Restart(Command):

    names = {'restart'}

    def __call__(self, cmd, rest, window):
        from .actions import restart
        restart(window)


class Clear(Command):

    names = {'clear', 'closeall'}

    def __call__(self, cmd, rest, window):
        window.close_all_tabs()


class Quit(Command):

    names = {'quit'}

    def __call__(self, cmd, rest, window):
        from .actions import quit
        quit(window)


class Save(Command):

    names = {'save'}

    def __call__(self, cmd, rest, window):
        if window.current_tab:
            window.current_tab.save_page(rest.strip() or None)


class Export(Command):

    names = {'export'}

    def __call__(self, cmd, rest, window):
        from PyQt5.Qt import QApplication
        if not rest.strip():
            rest = os.path.join(tempfile.gettempdir(), 'unnamed.vise-session')
        with open(rest, 'wb') as f:
            session_data = QApplication.instance().serialize_state()
            f.write(pickle.dumps(session_data, pickle.HIGHEST_PROTOCOL))
        window.show_status_message(_('Exported session to: %s') % rest, 5, 'success')


class Print(Command):

    names = {'print'}

    def __call__(self, cmd, rest, window):
        if window.current_tab:
            window.current_tab.print_page(rest.strip() or None)


class Inspect(Command):

    names = {'inspect', 'dev'}

    def __call__(self, cmd, rest, window):
        window.toggle_devtools()


def init_commands():
    all_commands = set()

    def process_dict(d):
        for name, val in d.items():
            if type(val) is type and issubclass(val, Command) and val is not Command:
                all_commands.add(val)

    for group in (open_commands, tab_commands):
        process_dict(vars(group))
    process_dict(globals())
    return {c() for c in all_commands}


def read_command_names():
    command_map = {}
    all_command_names = set()
    for cmd in all_commands:
        all_command_names |= cmd.names
        for name in cmd.names:
            if name in command_map:
                raise ValueError('The command name %r is used twice' % name)
            command_map[name] = cmd
    return all_command_names, command_map


all_commands = init_commands()
all_command_names, command_map = read_command_names()


def run_command(window, text):
    cmd, rest = text.partition(' ')[::2]
    obj = command_map.get(cmd)
    if obj is None:
        common = [name for name in command_map if name.startswith(cmd)]
        if len(common) == 1:
            obj = command_map[common[0]]
        else:
            window.show_status_message(_('Unknown command: ') + cmd, 5, 'error')
            return
    obj(cmd, rest, window)
