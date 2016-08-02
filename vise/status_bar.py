#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2016, Kovid Goyal <kovid at kovidgoyal.net>

from gettext import gettext as _

from PyQt5.Qt import (
    QLineEdit, pyqtSignal, Qt, QStackedWidget, QLabel, QWidget, QHBoxLayout,
    QToolButton)
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


class Status(QStackedWidget):

    def __init__(self, parent):
        QStackedWidget.__init__(self, parent)
        self.main_window = parent
        self.msg = QLabel('')
        self.msg.setFocusPolicy(Qt.NoFocus)
        self.addWidget(self.msg)
        self.setFocusPolicy(Qt.NoFocus)
        self.msg.setFocusPolicy(Qt.NoFocus)
        self.search = SearchPanel(self)
        self.search.edit.abort_search.connect(self.hide_search)
        self.search.edit.do_search.connect(self.hide_search)
        self.addWidget(self.search)

    def __call__(self, text=''):
        self.msg.setText('<b>' + text)

    def show_search(self, forward=True):
        self.setCurrentIndex(1)
        self.search.show_search(forward)

    def hide_search(self):
        self.setCurrentIndex(0)
        self.search.hide_search()
        self.main_window.refocus()

    @property
    def current_search_text(self):
        return self.search.edit.text()


class ModeLabel(QLabel):

    def __init__(self, main_window):
        QLabel.__init__(self, '')
        self.main_window = main_window
        self.setFocusPolicy(Qt.NoFocus)

    def update_mode(self):
        tab = self.main_window.current_tab
        text = ''
        if tab is not None:
            if tab.force_passthrough:
                text = '-- %s --' % _('PASSTHROUGH')
            elif tab.text_input_focused:
                text = '-- %s --' % _('INSERT')
        self.setText(text)


class PassthroughButton(QToolButton):

    def __init__(self, main_window):
        QToolButton.__init__(self, main_window)
        self.setFocusPolicy(Qt.NoFocus)
        self.setCursor(Qt.PointingHandCursor)
        self.main_window = main_window
        self.setCheckable(True)
        self.setIcon(get_icon('passthrough.png'))
        self.toggled.connect(self.change_passthrough)
        self.update_state()

    def update_state(self):
        self.blockSignals(True)
        tab = self.main_window.current_tab
        self.setChecked(getattr(tab, 'force_passthrough', False))
        self.setToolTip(_('Disable passthrough mode') if self.isChecked() else _(
            'Enable passthrough mode'))
        self.blockSignals(False)

    def change_passthrough(self):
        tab = self.main_window.current_tab
        if tab is not None:
            tab.force_passthrough = self.isChecked()
