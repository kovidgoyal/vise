#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2015, Kovid Goyal <kovid at kovidgoyal.net>

from PyQt5.Qt import (
    Qt, QObject, QEvent, QApplication, QMainWindow, QKeySequence, QOpenGLWidget, QLineEdit
)

from . import actions
from .ask import Ask

modifiers_mask = int(Qt.ShiftModifier | Qt.ControlModifier | Qt.AltModifier | Qt.MetaModifier)

all_keys = {int(v): k for k, v in vars(Qt).items() if k.startswith('Key_') and k not in {'Key_Alt', 'Key_Meta', 'Key_Control', 'Key_Shift'}}


def only_modifiers(key):
    return (key & ~modifiers_mask) not in all_keys


def key_from_event(ev):
    modifiers = int(ev.modifiers()) & modifiers_mask
    return ev.key() | modifiers


def key_to_string(key):
    return QKeySequence(key).toString().encode('utf-8', 'ignore').decode('utf-8')

normal_key_map, input_key_map = {}, {}


def read_key_map(which, raw):
    for line in raw.splitlines():
        line = line.strip()
        if line:
            key, action = (x.strip() for x in line.partition(' ')[::2])
            key = QKeySequence.fromString(key)[0]
            action = getattr(actions, action)
            which[key] = action


read_key_map(normal_key_map, '''\
Alt+Right                   forward
Alt+Left                    back
Shift+Right                 next_tab
Shift+Left                  prev_tab
D                           close_tab
/                           search_forward
?                           search_back
Shift+?                     search_back
N                           next_match
Shift+N                     prev_match
Ctrl+Z                      set_passthrough_mode
G                           quickmark
Shift+G                     quickmark_newtab
J                           scroll_line_down
K                           scroll_line_up
H                           scroll_line_left
L                           scroll_line_right
Y                           copy_url
P                           paste_and_go
Shift+P                     paste_and_go_newtab
;                           ask
:                           ask
Shift+;                     ask
Shift+:                     ask
O                           ask_open
Shift+O                     ask_tabopen
''')


read_key_map(input_key_map, '''\
Escape                     exit_text_input
Ctrl+I                     edit_text
''')


class KeyFilter(QObject):

    def __init__(self, parent=None):
        QObject.__init__(self, parent)
        self.disabled = False

    @property
    def disable_filtering(self):
        return self

    def __enter__(self):
        self.disabled = True

    def __exit__(self, *args):
        self.disabled = False

    def eventFilter(self, watched, event):
        if self.disabled:
            return False
        etype = event.type()
        if etype == QEvent.KeyPress:
            app = QApplication.instance()
            window, fw = app.activeWindow(), app.focusWidget()

            if isinstance(fw, QLineEdit) and isinstance(fw.parent(), Ask):
                # Prevent tabbing out of line edit
                key = key_from_event(event)
                if key in (Qt.Key_Tab, Qt.Key_Backtab):
                    fw.parent().keyPressEvent(event)
                    return True

            if isinstance(window, QMainWindow) and (fw is None or isinstance(fw, QOpenGLWidget)):
                key = key_from_event(event)

                if window.quickmark_pending:
                    if only_modifiers(key):
                        return True
                    window.quickmark(key)
                    return True

                if window.current_tab is not None:

                    if window.current_tab.force_passthrough:
                        return False

                    if window.current_tab.text_input_focused:
                        action = input_key_map.get(key)
                        if action is not None:
                            swallow = action(window, fw, self)
                            if swallow is True:
                                return True
                        return False

                action = normal_key_map.get(key)
                if action is not None:
                    swallow = action(window, fw, self)
                    if swallow is True:
                        return True
        return False
