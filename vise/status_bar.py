#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2016, Kovid Goyal <kovid at kovidgoyal.net>

from collections import namedtuple
from gettext import gettext as _
from time import monotonic
from xml.sax.saxutils import escape

from PyQt6.QtCore import Qt, QTimer, QUrl, pyqtSignal, QPointF
from PyQt6.QtGui import (QBrush, QColor, QLinearGradient, QPainter, QPalette,
                         QStaticText, QTextOption)
from PyQt6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
                             QStackedWidget, QStatusBar, QWidget)

from .config import color
from .constants import STATUS_BAR_HEIGHT


class Search(QLineEdit):

    do_search = pyqtSignal(object, object)
    abort_search = pyqtSignal()
    passthrough_keys = True

    def __init__(self, parent=None):
        QLineEdit.__init__(self, parent)
        self.setAttribute(Qt.WidgetAttribute.WA_MacShowFocusRect, False)
        self.setStyleSheet('QLineEdit { background: transparent; color: %s; selection-background-color: %s }' % (
            color('status bar foreground', 'palette(window-text)'),
            color('status bar selection', 'palette(window-text)'),
        ))
        self.search_forward = True
        self.textEdited.connect(self.text_edited)

    def text_edited(self, text):
        self.do_search.emit(text, self.search_forward)

    def keyPressEvent(self, ev):
        k = ev.key()
        if k == Qt.Key.Key_Escape:
            self.abort_search.emit()
            ev.accept()
            return
        if k in (Qt.Key.Key_Enter, Qt.Key.Key_Return):
            text = self.text()
            self.editingFinished.emit()
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
        self.edit.setFocus(Qt.FocusReason.OtherFocusReason)
        self.edit.search_forward = forward
        self.la.setText(_('Search forward:') if forward else _('Search backward:'))

    def hide_search(self):
        pass


TemporaryMessage = namedtuple('TemporaryMessage', 'timeout text type start_time')


class Message(QWidget):

    def __init__(self, parent, sb_background):
        QWidget.__init__(self, parent)
        self.is_permanent = False
        self.is_address = False
        self.is_secure = False
        self.static_text = None
        self.current_key = None
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.sb_background = QColor(color(sb_background, self.palette().color(QPalette.ColorRole.Window)))

    def focusInEvent(self, ev):
        # Needed because in Qt 5.11 the no focus focus policy is broken
        app = QApplication.instance()
        window = app.activeWindow()
        if hasattr(window, 'current_tab'):
            ct = window.current_tab
            if ct is not None:
                ct.setFocus(Qt.FocusReason.OtherFocusReason)

    def set_message(self, text, color_, bold=False, is_permanent=False):
        from vise.view import certificate_error_domains
        key = (text, color_.name(), bold, is_permanent)
        if key == self.current_key:
            return
        self.current_key = key
        self.is_permanent = is_permanent
        prefix = text.partition(':')[0]
        self.is_address = self.is_permanent and prefix.lower() in {'http', 'https', 'vise', 'file'}
        self.is_secure = prefix.lower() in {'https', 'vise', 'file'}
        color_ = color_ or self.palette().color(self.palette().WindowText)
        if self.is_address:
            qurl = QUrl(text)
            if self.is_secure and qurl.host() in certificate_error_domains:
                self.is_secure = False
            if qurl.scheme() in {'vise', 'file'}:
                host = qurl.path()
                rest = ''
                sep = ':'
            else:
                host = qurl.host()
                rest = qurl.toDisplayString(QUrl.UrlFormattingOption.RemoveScheme | QUrl.UrlFormattingOption.RemoveAuthority)
                sep = '://'
            self.static_text = QStaticText(
                '<span style="white-space:nowrap; color: {fg}">'
                '<span style="color:{emph}; font-weight:bold">{scheme}</span><span style="color:{dull}">{sep}</span>'
                '<span style="color:{fg}">{host}</span>'
                '<span style="color:{dull}">{rest}</span>'.format(
                    fg=color_.name(), emph='green' if self.is_secure else 'red', scheme=escape(qurl.scheme()),
                    host=escape(host), dull=color('status bar dull foreground', 'gray'), sep=sep,
                    rest=escape(rest)
                ))
        else:
            self.static_text = QStaticText('<span style="color:{}; font-weight: {}; white-space:nowrap">{}</span>'.format(
                color_.name(), ('bold' if bold else 'normal'), escape(text)))
        to = QTextOption(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        to.setWrapMode(QTextOption.WrapMode.NoWrap)
        self.static_text.setTextOption(to)
        self.static_text.prepare(font=self.font())
        self.update()

    def paintEvent(self, ev):
        if not self.static_text or not self.static_text.text():
            return
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        # If text is too long too fit, fade it out at the end
        self.static_text.setTextWidth(self.rect().width())
        sz = self.static_text.size()
        r = self.rect()
        p.drawStaticText(0, int(r.height() - sz.height()) // 2, self.static_text)
        if sz.width() > r.width():
            g = QLinearGradient(QPointF(self.rect().topLeft()), QPointF(self.rect().topRight()))
            c = QColor(self.sb_background)
            c.setAlpha(0)
            g.setColorAt(0, c)
            g.setColorAt(0.8, c)
            g.setColorAt(1.0, self.sb_background)
            p.fillRect(self.rect(), QBrush(g))
        p.end()


class Status(QStackedWidget):

    hidden = pyqtSignal()

    def __init__(self, parent):
        QStackedWidget.__init__(self, parent)
        self.permanent_message = ''
        self.temporary_message = TemporaryMessage(1, '', 'info', monotonic())
        self.msg = Message(self, parent.sb_background)
        self.addWidget(self.msg)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.msg.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.search = SearchPanel(self)
        self.search.edit.abort_search.connect(self.hide_search)
        self.search.edit.editingFinished.connect(self.hide_search)
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
        is_permanent = True
        if tm.text and (tm.timeout == 0 or monotonic() - tm.start_time < tm.timeout):
            text = tm.text
            if tm.type == 'error':
                col, bold = QColor('red'), True
            elif tm.type == 'success':
                col, bold = QColor('green'), True
            self.update_timer.start()
            is_permanent = False
        else:
            text = self.permanent_message
            self.update_timer.stop()
        self.msg.set_message(text, col, bold, is_permanent)

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
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    def update_mode(self, text):
        self.setText(text)


class PassthroughButton(QWidget):

    toggled = pyqtSignal(bool)

    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.is_enabled = False
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.update_state(False)
        self.setMinimumWidth(STATUS_BAR_HEIGHT - 4)
        self.setMinimumHeight(STATUS_BAR_HEIGHT - 4)

    def update_state(self, passthrough):
        self.is_enabled = bool(passthrough)
        self.setToolTip(_('Disable passthrough mode') if self.is_enabled else _('Enable passthrough mode'))
        self.update()

    def mousePressEvent(self, ev):
        if ev.button() == Qt.MouseButton.LeftButton:
            self.is_enabled ^= True
            self.toggled.emit(self.is_enabled)
            ev.accept()

    def paintEvent(self, ev):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        f = painter.font()
        f.setBold(True)
        f.setPixelSize(max(2, self.height() - 1))
        painter.setFont(f)
        painter.setPen(QColor('red' if self.is_enabled else 'green'))
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, 'Z')
        painter.end()


class StatusBar(QStatusBar):

    search_bar_hidden = pyqtSignal()
    do_search = pyqtSignal(object, object)
    change_passthrough = pyqtSignal(bool)

    def __init__(self, downloads_indicator, parent=None):
        QStatusBar.__init__(self, parent)
        self.setMaximumHeight(STATUS_BAR_HEIGHT)
        self.setMinimumHeight(STATUS_BAR_HEIGHT)
        self.sb_background = 'status bar private background' if getattr(parent, 'is_private', False) else 'status bar background'
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

        self.addPermanentWidget(self.mode_label)
        self.addPermanentWidget(downloads_indicator)
        self.addPermanentWidget(self.passthrough_button)
        self.setStyleSheet('''
        QStatusBar { color: FG; background: BG; }
        QStatusBar QLabel { color: FG; background: BG; }
        '''.replace(
            'FG', color('status bar foreground', 'palette(window-text)')).replace(
            'BG', color(self.sb_background, 'palette(window)'))
        )

    @property
    def current_search_text(self):
        return self.status_msg.current_search_text
