#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2015, Kovid Goyal <kovid at kovidgoyal.net>

from PyQt6.QtCore import QEvent, QObject, Qt
from PyQt6.QtGui import QKeySequence
from PyQt6.QtWidgets import QApplication, QDialog, QLineEdit, QMainWindow

from . import actions
from .ask import Ask
from .config import load_config

modifiers_mask = (Qt.KeyboardModifier.ShiftModifier | Qt.KeyboardModifier.ControlModifier | Qt.KeyboardModifier.AltModifier | Qt.KeyboardModifier.MetaModifier).value

all_keys = {int(v): k for k, v in vars(Qt).items() if k.startswith('Key_') and k not in {'Key_Alt', 'Key_Meta', 'Key_Control', 'Key_Shift'}}


def only_modifiers(key):
    return (key & ~modifiers_mask) not in all_keys


def key_from_event(ev):
    modifiers = int(ev.modifiers()) & modifiers_mask
    return ev.key() | modifiers


def key_to_string(key):
    return QKeySequence(key).toString().encode('utf-8', 'ignore').decode('utf-8')


normal_key_map, input_key_map = {}, {}


def read_key_map(mode='normal'):
    km = mode + ' mode keys'
    dkm, ukm = load_config(user=False)[km], load_config(user=True).get(km) or {}

    def get_keys(x):
        if isinstance(x, str):
            x = [x]
        for k in x:
            if isinstance(k, str):
                yield QKeySequence.fromString(k)[0]

    key_map = {}
    for action, x in ukm.items():
        if isinstance(action, str):
            try:
                action = getattr(actions, action)
            except AttributeError:
                continue
            key_map.update(dict.fromkeys(get_keys(x), action))
    for action, x in dkm.items():
        if isinstance(action, str):
            action = getattr(actions, action)
            for k in get_keys(x):
                if k not in key_map:
                    key_map[k] = action
    return key_map


normal_key_map = read_key_map()
input_key_map = read_key_map('insert')


def passthrough_keys(widget):
    if widget is None:
        return True
    if getattr(widget, 'passthrough_keys', False):
        return True
    p = widget.parent()
    while p:
        if isinstance(p, QDialog):
            return True
        p = p.parent()
    return False


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
        if etype == QEvent.Type.KeyPress:
            app = QApplication.instance()
            window, fw = app.activeWindow(), app.focusWidget()

            if isinstance(fw, QLineEdit) and isinstance(fw.parent(), Ask):
                # Prevent tabbing out of line edit
                key = key_from_event(event)
                if key in (Qt.Key.Key_Tab, Qt.Key.Key_Backtab, Qt.KeyboardModifier.ShiftModifier | Qt.Key.Key_Backtab):
                    fw.parent().keyPressEvent(event)
                    return True

            if fw is None and hasattr(window, 'current_tab'):
                ct = window.current_tab
                if ct is not None:
                    ct.setFocus(Qt.FocusReason.OtherFocusReason)
                    fw = QApplication.instance().focusWidget()

            if isinstance(window, QMainWindow) and not passthrough_keys(fw):
                key = key_from_event(event)

                if window.quickmark_pending:
                    if only_modifiers(key):
                        return True
                    window.quickmark(key)
                    return True

                if window.choose_tab_pending:
                    if only_modifiers(key):
                        return True
                    window.choose_tab(key)
                    return True

                ct = window.current_tab
                if ct is not None:

                    if ct.force_passthrough:
                        return False

                    if ct.follow_link_pending:
                        if only_modifiers(key):
                            return True
                        if ct.follow_link(key):
                            return True

                    if ct.text_input_focused:
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
