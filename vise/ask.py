#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2015, Kovid Goyal <kovid at kovidgoyal.net>

import sys
from gettext import gettext as _
from queue import Queue
from threading import Thread

from PyQt6 import sip
from PyQt6.QtCore import QPoint, QSize, Qt, pyqtSignal
from PyQt6.QtGui import QColor, QKeySequence, QPainter
from PyQt6.QtWidgets import (QAbstractListModel, QApplication, QFrame,
                             QLineEdit, QListView, QModelIndex,
                             QStringListModel, QStyledItemDelegate,
                             QVBoxLayout, QWidget)

from .cmd import all_command_names, command_map
from .config import color
from .utils import make_highlighted_text

sorted_command_names = sorted(all_command_names)


class Completions(QAbstractListModel):

    def __init__(self, parent=None):
        QAbstractListModel.__init__(self, parent)
        self.items = []

    def rowCount(self, parent=QModelIndex()):
        return len(self.items)

    def set_items(self, items):
        self.beginResetModel()
        self.items = items
        self.endResetModel()

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.UserRole:
            try:
                return self.items[index.row()]
            except IndexError:
                pass
        elif role == Qt.ItemDataRole.DecorationRole:
            try:
                return self.items[index.row()].icon()
            except IndexError:
                pass


class Delegate(QStyledItemDelegate):

    def __init__(self, parent=None):
        QStyledItemDelegate.__init__(self, parent)
        self._m = QStringListModel(['sdfgkjsg sopgjs gsgs slgjslg sdklgsgl', ''])

    def sizeHint(self, option, index):
        ans = QStyledItemDelegate.sizeHint(self, option, self._m.index(0))
        index.data(Qt.ItemDataRole.UserRole).adjust_size_hint(option, ans)
        return ans

    def paint(self, painter, option, index):
        QStyledItemDelegate.paint(self, painter, option, self._m.index(1))
        painter.save()
        parent = self.parent() or QApplication.instance()
        style = parent.style()
        try:
            index.data(Qt.ItemDataRole.UserRole).draw_item(painter, style, option)
        finally:
            painter.restore()


class Candidate:

    def __init__(self, text, positions):
        self.value = text + ' '
        self.text = make_highlighted_text(text, positions)

    def __repr__(self):
        return self.value

    def draw_item(self, painter, style, option):
        text_rect = style.subElementRect(style.SE_ItemViewItemText, option, None)
        y = text_rect.y()
        y += (text_rect.height() - self.text.size().height()) // 2
        painter.drawStaticText(QPoint(text_rect.x(), y), self.text)

    def adjust_size_hint(self, option, sz):
        pass


class ListView(QListView):

    def __init__(self, parent=None):
        QListView.__init__(self, parent)
        self.setStyleSheet('''
        QListView { color: FG; background: BG }
        QListView::item:selected { border-radius: 8px; background: HB }
        '''.replace('HB', color('status bar highlight', 'palette(highlight)')).replace(
            'FG', color('tab tree foreground', 'palette(window-text)')).replace(
            'BG', color('tab tree background', 'palette(window)'))
        )
        self.setFrameStyle(QFrame.Shape.NoFrame)
        self.viewport().setAutoFillBackground(False)
        self.setIconSize(QSize(16, 16))
        self.setSpacing(2)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.delegate = d = Delegate(self)
        self.setItemDelegate(d)


class LineEdit(QLineEdit):

    passthrough_keys = True

    def __init__(self, parent=None):
        QLineEdit.__init__(self, parent)
        self.setAttribute(Qt.WidgetAttribute.WA_MacShowFocusRect, False)
        self.setStyleSheet('''
        QLineEdit {
            border-radius: 8px;
            padding: 1px 6px;
            background: BG;
            color: FG;
            selection-background-color: SEL;
        }
        '''.replace('BG', color('status bar background', 'palette(window)')).replace(
            'FG', color('status bar foreground', 'palette(window-text)')).replace(
            'SEL', color('status bar selection', 'palette(highlight)'))
        )
        self.setPlaceholderText(_('Enter command'))

    def keyPressEvent(self, ev):
        if ev.matches(QKeySequence.StandardKey.Copy):
            from .commands.open import Open
            cmd, rest = self.text().partition(' ')[::2]
            if cmd in Open.names and rest.strip():
                QApplication.clipboard().setText(rest)
                ev.accept()
                return
        k = ev.key()
        mods = ev.modifiers()
        if k in (Qt.Key.Key_V, Qt.Key.Key_S) and mods & Qt.Modifier.CTRL and mods & Qt.Modifier.SHIFT:
            text = QApplication.clipboard().text(k == Qt.Key.Key_S)
            if text:
                self.insert(text)
        return QLineEdit.keyPressEvent(self, ev)


class Ask(QWidget):

    run_command = pyqtSignal(object)
    hidden = pyqtSignal()
    completions_done = pyqtSignal(object)

    def __init__(self, parent=None):
        self.complete_pos = 0
        self.callback = None
        QWidget.__init__(self, parent)
        self.queue = Queue()
        self.completions_done.connect(self.on_completions_done)
        self.completions_thread = t = Thread(name='Completions', target=self.completions_thread, daemon=True)
        t.start()
        self.l = l = QVBoxLayout(self)
        self.edit = e = LineEdit(self)
        e.textEdited.connect(self.update_completions)
        self.candidates = c = ListView(self)
        c.currentChanged = self.current_changed
        self.model = m = Completions(self)
        c.setModel(m)
        l.addWidget(e), l.addWidget(c)
        if hasattr(parent, 'resized'):
            parent.resized.connect(self.re_layout)
            self.re_layout()

    def completions_thread(self):
        while True:
            obj, cmd, rest = self.queue.get()
            completions = obj.completions(cmd, rest)
            if not sip.isdeleted(self):
                self.completions_done.emit(completions)

    def re_layout(self):
        w = self.parent().width()
        h = self.parent().height() // 2
        self.resize(w, h)
        self.move(0, h)

    def __call__(self, prefix='', callback=None):
        self.callback = callback
        self.setVisible(True), self.raise_()
        self.edit.blockSignals(True)
        self.edit.setText(prefix)
        self.edit.blockSignals(False)
        self.update_completions()
        self.edit.setFocus(Qt.FocusReason.OtherFocusReason)

    def update_completions(self):
        text = self.edit.text()
        parts = text.strip().split(' ')
        self.complete_pos = 0
        if len(parts) == 1:
            self.completions_done.emit(self.command_completions(parts[0]))
        else:
            idx = self.complete_pos = text.find(parts[0]) + len(parts[0]) + 1
            cmd, rest = parts[0], text[idx:]
            obj = command_map.get(cmd)
            if obj is not None:
                self.queue.put((obj, cmd, rest))

    def on_completions_done(self, completions):
        self.model.set_items(completions)
        self.candidates.setCurrentIndex(QModelIndex())

    def command_completions(self, prefix):
        return [
            Candidate(cmd, [i for i in range(len(prefix))])
            for cmd in sorted_command_names if cmd.startswith(prefix)
        ]

    def keyPressEvent(self, ev):
        k = ev.key()
        if k == Qt.Key.Key_Escape:
            c = self.callback
            if c is not None:
                c(None)
            self.close() if self.parent() is None else self.hide()
            ev.accept()
            return
        if k == Qt.Key.Key_Tab:
            self.next_completion()
            ev.accept()
            return
        if k == Qt.Key.Key_Backtab:
            self.next_completion(forward=False)
            ev.accept()
            return
        if k in (Qt.Key.Key_Enter, Qt.Key.Key_Return):
            c = self.callback
            self.close() if self.parent() is None else self.hide()
            if c is not None:
                c(self.edit.text())
            else:
                self.run_command.emit(self.edit.text())
        return QWidget.keyPressEvent(self, ev)

    def hide(self):
        QWidget.hide(self)
        self.callback = None
        self.hidden.emit()

    def next_completion(self, forward=True):
        if self.model.rowCount() == 0:
            return
        v = self.candidates
        ci = v.currentIndex()
        row = ci.row() if ci.isValid() else -1
        row = (row + (1 if forward else -1)) % self.model.rowCount()
        v.setCurrentIndex(self.model.index(row))
        v.scrollTo(v.currentIndex())

    def current_changed(self, old_index, new_index):
        item = self.candidates.currentIndex().data(Qt.ItemDataRole.UserRole)
        if item is not None:
            text = self.edit.text()[:self.complete_pos] + item.value
            self.edit.setText(text)

    def paintEvent(self, ev):
        p = QPainter(self)
        c = color('tab tree background', None)
        if c:
            p.fillRect(ev.rect(), QColor(c))
        p.end()
        QWidget.paintEvent(self, ev)


def develop():
    from .main import Application
    app = Application(no_session=True, run_local_server=False)
    w = Ask()
    w()
    w.show()
    app.exec()
    del w
    del app


def standalone():
    from vise.utils import parse_url

    from .main import Application
    from .places import places
    app = Application(no_session=True, run_local_server=False)
    w = Ask()
    ret = 0

    def output(text):
        nonlocal ret
        if text is None:
            ret = 1
        else:
            text = text.partition(' ')[-1].strip()
            qurl = parse_url(text)
            places.on_visit(qurl, 1, True)
            sys.stdout.buffer.write(text.encode('utf-8'))
            sys.stdout.flush()

    w('copyurl ', output)
    w.show()
    app.exec()
    del w
    del app
    raise SystemExit(ret)
