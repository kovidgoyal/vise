#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2015, Kovid Goyal <kovid at kovidgoyal.net>

import os
import re
import sys
import math
from functools import lru_cache

from PyQt5.Qt import (
    QUrl, QFontMetrics, QApplication, QConicalGradient, QPen, QBrush, QPainter,
    QRect, Qt, QDialog, QDialogButtonBox)

from .constants import cache_dir, str_version
from .settings import gprefs


def parse_url(url_or_path):
    return QUrl.fromUserInput(url_or_path, os.getcwd())


def safe_disconnect(signal):
    try:
        signal.disconnect()
    except TypeError:
        pass  # signal was not connected


@lru_cache(maxsize=500)
def elided_text(text, font=None, width=300, pos='middle'):
    ''' Return a version of text that is no wider than width pixels when
    rendered, replacing characters from the left, middle or right (as per pos)
    of the string with an ellipsis. Results in a string much closer to the
    limit than Qt's elidedText() '''
    fm = QApplication.fontMetrics() if font is None else (font if isinstance(font, QFontMetrics) else QFontMetrics(font))
    delta = 4
    ellipsis = u'\u2026'

    def remove_middle(x):
        mid = len(x) // 2
        return x[:max(0, mid - (delta // 2))] + ellipsis + x[mid + (delta // 2):]

    chomp = {'middle': remove_middle, 'left': lambda x: (ellipsis + x[delta:]), 'right': lambda x: (x[:-delta] + ellipsis)}[pos]
    while len(text) > delta and fm.width(text) > width:
        text = chomp(text)
    return text


def draw_snake_spinner(painter, rect, angle, light, dark):
    ' Draw a snake spinner on the specified painter '
    painter.setRenderHint(QPainter.Antialiasing)

    if rect.width() > rect.height():
        delta = (rect.width() - rect.height()) // 2
        rect = rect.adjusted(delta, 0, -delta, 0)
    elif rect.height() > rect.width():
        delta = (rect.height() - rect.width()) // 2
        rect = rect.adjusted(0, delta, 0, -delta)
    disc_width = max(4, rect.width() // 10)

    drawing_rect = QRect(rect.x() + disc_width, rect.y() + disc_width, rect.width() - 2 * disc_width, rect.height() - 2 * disc_width)
    try:
        angle_for_width = math.degrees(math.atan2(2.5 * disc_width, drawing_rect.width()))
    except ZeroDivisionError:
        angle_for_width = 5

    gradient = QConicalGradient(drawing_rect.center(), angle - angle_for_width)
    gradient.setColorAt(1, light)
    gradient.setColorAt(0, dark)

    painter.setPen(QPen(light, disc_width))
    painter.drawArc(drawing_rect, 0, 360 * 16)
    pen = QPen(QBrush(gradient), disc_width)
    pen.setCapStyle(Qt.RoundCap)
    painter.setPen(pen)
    painter.drawArc(drawing_rect, angle * 16, (360 - 2 * angle_for_width) * 16)


class Dialog(QDialog):

    '''
    An improved version of Qt's QDialog class. This automatically remembers the
    last used size, automatically connects the signals for QDialogButtonBox,
    automatically sets the window title and if the dialog has an object named
    splitter, automatically saves the splitter state.

    In order to use it, simply subclass an implement setup_ui(). You can also
    implement sizeHint() to give the dialog a different default size when shown
    for the first time.
    '''

    def __init__(self, title, name, parent=None, prefs=gprefs):
        QDialog.__init__(self, parent)
        self.prefs_for_persistence = prefs
        self.setWindowTitle(title)
        self.name = name
        self.bb = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.bb.accepted.connect(self.accept)
        self.bb.rejected.connect(self.reject)

        self.setup_ui()

        self.resize(self.sizeHint())
        geom = self.prefs_for_persistence.get(name + '-geometry', None)
        if geom is not None:
            self.restoreGeometry(geom)
        if hasattr(self, 'splitter'):
            state = self.prefs_for_persistence.get(name + '-splitter-state', None)
            if state is not None:
                self.splitter.restoreState(state)

    def accept(self):
        self.prefs_for_persistence.set(self.name + '-geometry', bytearray(self.saveGeometry()))
        if hasattr(self, 'splitter'):
            self.prefs_for_persistence.set(self.name + '-splitter-state', bytearray(self.splitter.saveState()))
        QDialog.accept(self)

    def reject(self):
        self.prefs_for_persistence.set(self.name + '-geometry', bytearray(self.saveGeometry()))
        if hasattr(self, 'splitter'):
            self.prefs_for_persistence.set(self.name + '-splitter-state', bytearray(self.splitter.saveState()))
        QDialog.reject(self)

    def setup_ui(self):
        raise NotImplementedError('You must implement this method in Dialog subclasses')


def ipython(user_ns=None):
    import IPython
    from traitlets.config import Config
    ipydir = os.path.join(cache_dir, 'ipython')
    defns = {'os': os, 're': re, 'sys': sys}
    BANNER = ('Welcome to the interactive vise shell!\n')
    if not user_ns:
        user_ns = defns
    else:
        defns.update(user_ns)
        user_ns = defns

    c = Config()
    c.TerminalInteractiveShell.confirm_exit = False
    c.PromptManager.in_template = (r'{color.LightGreen}vise '
                                   '{color.LightBlue}[{color.LightCyan}%s{color.LightBlue}]'
                                   r'{color.Green}|\#> ' % str_version)
    c.PromptManager.in2_template = r'{color.Green}|{color.LightGreen}\D{color.Green}> '
    c.PromptManager.out_template = r'<\#> '
    c.TerminalInteractiveShell.banner1 = BANNER
    c.PromptManager.justify = True
    c.TerminalIPythonApp.ipython_dir = ipydir
    os.environ['IPYTHONDIR'] = ipydir

    c.InteractiveShell.separate_in = ''
    c.InteractiveShell.separate_out = ''
    c.InteractiveShell.separate_out2 = ''

    c.PrefilterManager.multi_line_specials = True

    IPython.embed(config=c, user_ns=user_ns)
