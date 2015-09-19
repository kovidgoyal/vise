#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2015, Kovid Goyal <kovid at kovidgoyal.net>

from gettext import gettext as _

from PyQt5.Qt import (
    QWidget, QVBoxLayout, QLineEdit, QListView, QAbstractListModel,
    QModelIndex, Qt, QStyledItemDelegate, QStringListModel, QApplication,
    QPoint, QColor
)

from .cmd import all_commands
from .resources import get_icon
from .utils import make_highlighted_text

command_map = {}
all_command_names = set()
for cmd in all_commands:
    all_command_names |= cmd.names
    for name in cmd.names:
        if name in command_map:
            raise ValueError('The command name %r is used twice' % name)
        command_map[name] = cmd
del cmd, name


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

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.UserRole:
            try:
                return self.items[index.row()]
            except IndexError:
                pass
        elif role == Qt.DecorationRole:
            try:
                return self.items[index.row()].icon()
            except IndexError:
                pass


class Delegate(QStyledItemDelegate):

    MARGIN = 6

    def __init__(self, parent=None):
        QStyledItemDelegate.__init__(self, parent)
        self._m = m = QStringListModel(['sdfgkjsg sopgjs gsgs slgjslg sdklgsgl', ''])
        m.setData(m.index(0), get_icon('blank.png'), Qt.DecorationRole)
        m.setData(m.index(1), get_icon('blank.png'), Qt.DecorationRole)

    def sizeHint(self, option, index):
        ans = QStyledItemDelegate.sizeHint(self, option, self._m.index(0))
        ans.setHeight(ans.height() + self.MARGIN)
        return ans

    def paint(self, painter, option, index):
        QStyledItemDelegate.paint(self, painter, option, self._m.index(1))
        painter.save()
        parent = self.parent() or QApplication.instance()
        style = parent.style()
        try:
            icon_rect = style.subElementRect(style.SE_ItemViewItemDecoration, option, self.parent())
            text_rect = style.subElementRect(style.SE_ItemViewItemText, option, self.parent())
            index.data(Qt.UserRole).draw_item(painter, icon_rect, text_rect, self.MARGIN // 4)
        finally:
            painter.restore()


class Candidate:

    def __init__(self, text, positions):
        self.value = text + ' '
        self.text = make_highlighted_text(text, positions)

    def __repr__(self):
        return self.value

    def draw_item(self, painter, icon_rect, text_rect, margin):
        painter.drawStaticText(QPoint(text_rect.x(), text_rect.y() + margin), self.text)


class Ask(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        if hasattr(parent, 'resized'):
            parent.resized.connect(self.re_layout)
        self.l = l = QVBoxLayout(self)
        self.edit = e = QLineEdit(self)
        e.textEdited.connect(self.update_completions)
        e.setPlaceholderText(_('Enter command'))
        self.candidates = c = QListView(self)
        c.currentChanged = self.current_changed
        c.setFocusPolicy(Qt.NoFocus)
        pal = c.palette()
        pal.setColor(pal.HighlightedText, pal.color(pal.Text))
        pal.setColor(pal.Highlight, QColor('#ffffaa'))
        c.setPalette(pal)
        self.model = m = Completions(self)
        self.delegate = d = Delegate(c)
        c.setItemDelegate(d)
        c.setModel(m)
        l.addWidget(e), l.addWidget(c)
        self.complete_pos = 0

    def re_layout(self):
        w = self.parent().width()
        h = self.parent().height() // 2
        self.resize(w, h)
        self.move(0, h)

    def __call__(self, prefix=''):
        self.edit.blockSignals(True)
        self.edit.setText(prefix)
        self.edit.blockSignals(False)
        self.update_completions()
        self.edit.setFocus(Qt.OtherFocusReason)

    def update_completions(self):
        text = self.edit.text()
        parts = text.strip().split(' ')
        completions = []
        self.complete_pos = 0
        if len(parts) == 1:
            completions = self.command_completions(parts[0])
        else:
            idx = self.complete_pos = text.find(parts[0]) + len(parts[0]) + 1
            cmd, rest = parts[0], text[idx:]
            obj = command_map.get(cmd)
            if obj is not None:
                completions = obj.completions(cmd, rest)
        self.model.set_items(completions)
        self.candidates.setCurrentIndex(QModelIndex())

    def command_completions(self, prefix):
        return [
            Candidate(cmd, [i for i in range(len(prefix))])
            for cmd in all_command_names if cmd.startswith(prefix)
        ]

    def keyPressEvent(self, ev):
        k = ev.key()
        if k == Qt.Key_Escape:
            self.close() if self.parent() is None else self.hide()
            ev.accept()
            return
        if k == Qt.Key_Tab:
            self.next_completion()
            ev.accept()
            return
        if k == Qt.Key_Backtab:
            self.next_completion(forward=False)
            ev.accept()
            return
        return QWidget.keyPressEvent(self, ev)

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
        item = self.candidates.currentIndex().data(Qt.UserRole)
        text = self.edit.text()[:self.complete_pos] + item.value
        self.edit.setText(text)


def develop():
    app = QApplication([])
    w = Ask()
    w()
    w.show()
    app.exec_()
