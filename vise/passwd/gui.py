#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2016, Kovid Goyal <kovid at kovidgoyal.net>

from gettext import gettext as _

import sip
from PyQt5.Qt import (
    QSize, QAbstractListModel, Qt, QSortFilterProxyModel, QListView, QVBoxLayout, QLineEdit
)

from ..message_box import error_dialog, question_dialog
from ..utils import Dialog
from .db import PasswordDB


class KeysModel(QAbstractListModel):

    def __init__(self, db, parent=None):
        self.keys = sorted(db, key=lambda x: x.lower())
        QAbstractListModel.__init__(self, parent)

    def rowCount(self, parent=None):
        return len(self.keys)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            try:
                return self.keys[index.row()]
            except IndexError:
                pass

    def refresh(self, db):
        self.beginResetModel()
        self.keys = sorted(db, key=lambda x: x.lower())
        self.endResetModel()


class PasswordManager(Dialog):

    def __init__(self, db, parent=None):
        self.db = db
        Dialog.__init__(self, _('vise Password Manager'), 'password-manager', parent=parent)

    def sizeHint(self):
        return QSize(800, 600)

    def setup_ui(self):
        self.l = l = QVBoxLayout(self)
        self.filter_edit = le = QLineEdit(self)
        le.setPlaceholderText(_('Filter the list'))
        l.addWidget(le)
        self.model = KeysModel(self.db, self)
        self.proxy_model = pm = QSortFilterProxyModel(self)
        pm.setSourceModel(self.model), pm.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.view = v = QListView(self)
        v.setStyleSheet('QListView::item { padding: 5px }')
        v.setAlternatingRowColors(True)
        v.setModel(self.proxy_model)
        l.addWidget(v)
        le.textChanged.connect(pm.setFilterFixedString)

        self.bb.setStandardButtons(self.bb.Close)
        l.addWidget(self.bb)
        self.bb.addButton(_('Add entry'), self.bb.ActionRole).clicked.connect(self.add_entry)
        self.bb.addButton(_('Remove selected'), self.bb.ActionRole).clicked.connect(self.remove_selected)
        self.bb.button(self.bb.Close).setDefault(True)

    def add_entry(self):
        pass

    def selected_keys(self):
        for index in self.view.selectedIndexes():
            if index.isValid():
                key = index.data(Qt.DisplayRole)
                if key:
                    yield key

    def remove_selected(self):
        keys = set(self.selected_keys())
        if not keys:
            return error_dialog(self, _('No entries selected'), _(
                'You must select an entry to remove'))
        changed = False
        for key in keys:
            if question_dialog(self, _('Are you sure?'), _(
                    'Are you sure you want to permanently delete all data for: <b>{0}</b>').format(key)):
                del self.db[key]
                changed = True
        if changed:
            self.model.refresh(self.db)


def standalone(password, path=None):
    from ..main import Application
    db = PasswordDB(password, path)
    app = Application([])
    d = PasswordManager(db)
    d.exec_()
    sip.delete(d)
    sip.delete(app)
