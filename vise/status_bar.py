#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2016, Kovid Goyal <kovid at kovidgoyal.net>

from collections import namedtuple
from time import monotonic
from gettext import gettext as _

from PyQt5.Qt import (
    QLineEdit, pyqtSignal, Qt, QStackedWidget, QLabel, QWidget, QHBoxLayout,
    QToolButton, QTimer, QStatusBar, QFrame, QPainter, QColor)

from .config import color
from .resources import get_icon


class Search(QLineEdit):

    do_search = pyqtSignal(object, object)
    abort_search = pyqtSignal()

    def __init__(self, parent=None):
        QLineEdit.__init__(self, parent)
        self.search_forward = True

    def keyPressEvent(self, ev):
        k = ev.key()
        if k == Qt.Key_Escape:
            self.abort_search.emit()
            ev.accept()
            return
        if k in (Qt.Key_Enter, Qt.Key_Return):
            text = self.text()
            self.do_search.emit(text, self.search_forward)
            return
        return QLineEdit.keyPressEvent(self, ev)


class SearchPanel(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.l = l = QHBoxLayout(self)
        l.setContentsMargins(0, 0, 0, 0)
        self.la = la = QLabel(self)
        l.addWidget(la)
        self.edit = Search(self)
        la.setBuddy(self.edit)
        l.addWidget(self.edit)

    def sizeHint(self):
        ans = QWidget.sizeHint(self)
        ans.setWidth(100000)
        return ans

    def show_search(self, forward=True):
        self.edit.selectAll()
        self.edit.setFocus(Qt.OtherFocusReason)
        self.edit.search_forward = forward
        self.la.setText(_('&Search forward:') if forward else _('&Search backward:'))

    def hide_search(self):
        pass

TemporaryMessage = namedtuple('TemporaryMessage', 'timeout text type start_time')


class Message(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.text = ''
        self.bold = False
        self.setFocusPolicy(Qt.NoFocus)

    def set_message(self, text, color, bold=False):
        self.text, self.color, self.bold = text, color, bold
        self.update()

    def paintEvent(self, ev):
        if not self.text:
            return
        p = QPainter(self)
        if self.bold:
            f = self.font()
            f.setBold(True)
            p.setFont(f)
        if self.color:
            p.setPen(self.color)
        p.setRenderHint(p.TextAntialiasing)
        p.drawText(self.rect(), Qt.AlignLeft | Qt.AlignVCenter | Qt.TextSingleLine, self.text)
        p.end()


class Status(QStackedWidget):

    hidden = pyqtSignal()

    def __init__(self, parent):
        QStackedWidget.__init__(self, parent)
        self.permanent_message = ''
        self.temporary_message = TemporaryMessage(1, '', 'info', monotonic())
        self.msg = Message(self)
        self.addWidget(self.msg)
        self.setFocusPolicy(Qt.NoFocus)
        self.msg.setFocusPolicy(Qt.NoFocus)
        self.search = SearchPanel(self)
        self.search.edit.abort_search.connect(self.hide_search)
        self.search.edit.do_search.connect(self.hide_search)
        self.addWidget(self.search)
        self.update_timer = t = QTimer(self)
        self.fg_color = color('status bar foreground', None)
        if self.fg_color:
            self.fg_color = QColor(self.fg_color)
        t.setSingleShot(True), t.setInterval(100), t.timeout.connect(self.update_message)

    def __call__(self, text=''):
        self.permanent_message = text
        self.update_message()

    def update_message(self):
        tm = self.temporary_message
        col = self.fg_color
        bold = False
        if tm.text and (tm.timeout == 0 or monotonic() - tm.start_time < tm.timeout):
            text = tm.text
            if tm.type == 'error':
                col, bold = QColor('red'), True
            elif tm.type == 'success':
                col, bold = QColor('green'), True
            self.update_timer.start()
        else:
            text = self.permanent_message
            self.update_timer.stop()
        self.msg.set_message(text, col, bold)

    def show_message(self, msg, timeout=1, message_type='info'):
        self.temporary_message = TemporaryMessage(timeout, msg, message_type, monotonic())
        self.update_message()

    def show_search(self, forward=True):
        self.setCurrentIndex(1)
        self.search.show_search(forward)

    def hide_search(self):
        self.setCurrentIndex(0)
        self.search.hide_search()
        self.hidden.emit()

    @property
    def current_search_text(self):
        return self.search.edit.text()


class ModeLabel(QLabel):

    def __init__(self):
        QLabel.__init__(self, '')
        self.setFocusPolicy(Qt.NoFocus)

    def update_mode(self, text):
        self.setText(text)


class PassthroughButton(QToolButton):

    def __init__(self, parent):
        QToolButton.__init__(self, parent)
        self.setFocusPolicy(Qt.NoFocus)
        self.setCursor(Qt.PointingHandCursor)
        self.setCheckable(True)
        self.setIcon(get_icon('passthrough.png'))
        self.update_state(False)

    def update_state(self, passthrough):
        self.blockSignals(True)
        self.setChecked(passthrough)
        self.setToolTip(_('Disable passthrough mode') if self.isChecked() else _(
            'Enable passthrough mode'))
        self.blockSignals(False)


class StatusBar(QStatusBar):

    search_bar_hidden = pyqtSignal()
    do_search = pyqtSignal(object, object)
    change_passthrough = pyqtSignal(bool)

    def __init__(self, downloads_indicator, parent=None):
        QStatusBar.__init__(self, parent)
        if parent:
            f = parent.font()
            f.setPixelSize(int(f.pixelSize() * 0.8))
            self.setFont(f)
        self.status_msg = Status(self)
        self.status_msg.hidden.connect(self.search_bar_hidden)
        self.status_msg.search.edit.do_search.connect(self.do_search)
        self.show_search = self.status_msg.show_search
        self.show_message = self.status_msg.show_message
        self.set_permanent_message = self.status_msg
        self.addWidget(self.status_msg)

        self.mode_label = ModeLabel()
        self.update_mode = self.mode_label.update_mode

        self.passthrough_button = PassthroughButton(self)
        self.passthrough_button.toggled.connect(self.change_passthrough)
        self.update_passthrough_state = self.passthrough_button.update_state

        def addsep():
            f = QFrame(self)
            f.setFrameShape(f.VLine)
            self.addPermanentWidget(f)
        addsep()
        self.addPermanentWidget(self.mode_label)
        addsep()
        self.addPermanentWidget(downloads_indicator)
        addsep()
        self.addPermanentWidget(self.passthrough_button)
        self.setStyleSheet('''
        QStatusBar { color: FG; background: BG; }
        QStatusBar QLabel { color: FG; background: BG; }
        '''.replace(
            'FG', color('status bar foreground', 'palette(window-text)')).replace(
            'BG', color('status bar background', 'palette(window)'))
        )

    @property
    def current_search_text(self):
        return self.status_msg.current_search_text
