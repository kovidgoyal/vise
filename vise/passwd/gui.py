#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2016, Kovid Goyal <kovid at kovidgoyal.net>

from gettext import gettext as _

from PyQt5 import sip
from PyQt5.Qt import (
    QSize, QAbstractListModel, Qt, QSortFilterProxyModel, QListView,
    QVBoxLayout, QLineEdit, QFormLayout, QCheckBox, QPlainTextEdit,
    QLabel, QWidget, QListWidget, QSplitter, QListWidgetItem, pyqtSignal,
    QPushButton
)

from ..message_box import error_dialog, question_dialog
from ..utils import Dialog, choose_files, BusyCursor
from .db import PasswordDB, import_lastpass_db


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


class EditAccount(QWidget):

    changed = pyqtSignal()
    delete_requested = pyqtSignal()

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.l = l = QFormLayout(self)
        self.username = u = QLineEdit(self)
        u.textChanged.connect(self.changed.emit)
        l.addRow(_('&Username:'), u)
        u.setPlaceholderText(_('Username for this account'))
        self.password = p = QLineEdit(self)
        l.addRow(_('&Password:'), p)
        p.setPlaceholderText(_('Password for this account'))
        p.textChanged.connect(self.changed.emit)
        p.setEchoMode(p.Password)
        self.show_password = sp = QCheckBox(_('&Show password'))
        l.addWidget(sp)
        sp.toggled.connect(lambda checked: p.setEchoMode(p.Normal if checked else p.Password))
        self.la = la = QLabel(_('&Notes:'))
        l.addRow(la)
        self.notes = n = QPlainTextEdit(self)
        la.setBuddy(n)
        n.textChanged.connect(self.changed.emit)
        l.addRow(n)
        self.autosubmit = asb = QCheckBox(_('&Auto login with these credentials'), self)
        l.addRow(asb)
        asb.stateChanged.connect(lambda: self.changed.emit())
        self.rb = b = QPushButton(_('&Delete this account'))
        b.clicked.connect(self.delete_requested.emit)
        l.addRow(b)

    @property
    def data(self):
        return {
            'username': self.username.text(),
            'password': self.password.text(),
            'notes': self.notes.toPlainText().strip() or None,
            'autologin': self.autosubmit.isChecked(),
        }

    @data.setter
    def data(self, val):
        self.blockSignals(True)
        self.username.setText(val.get('username') or '')
        self.password.setText(val.get('password') or '')
        self.notes.setPlainText(val.get('notes') or '')
        self.autosubmit.setChecked(val.get('autologin', False))
        self.blockSignals(False)


class EditItem(Dialog):

    def __init__(self, db, key, parent=None):
        self.db, self.key = db, key
        Dialog.__init__(self, _('Edit passwords'), 'password-edit', parent=parent)

    def sizeHint(self):
        return QSize(800, 600)

    def setup_ui(self):
        self.l = l = QVBoxLayout(self)
        self.splitter = s = QSplitter(self)
        l.addWidget(s)
        self.ab = b = self.bb.addButton(_('Add new account'), self.bb.ActionRole)
        b.clicked.connect(self.add_account)
        l.addWidget(self.bb)
        self.accounts = a = QListWidget(self)
        a.setDragDropMode(a.InternalMove)
        self.edit_account = e = EditAccount(self)
        e.changed.connect(self.data_changed)
        e.delete_requested.connect(self.delete_requested)
        s.addWidget(a), s.addWidget(e)
        for n, account in enumerate(self.db[self.key]['accounts']):
            if n == 0:
                e.data = account
            i = QListWidgetItem(account['username'], a)
            i.setData(Qt.UserRole, account)
        if a.count() < 1:
            na = {'username': '', 'password': '', 'notes': ''}
            i = QListWidgetItem('', a)
            i.setData(Qt.UserRole, na)
        a.setCurrentRow(0)
        a.currentItemChanged.connect(self.current_item_changed)

    def current_item_changed(self, curr, prev):
        self.edit_account.data = curr.data(Qt.UserRole) if curr else {}

    def delete_requested(self):
        item = self.accounts.currentItem()
        if item is not None:
            self.accounts.takeItem(self.accounts.row(item))

    def add_account(self):
        i = QListWidgetItem('', self.accounts)
        i.setData(Qt.UserRole, {})
        self.accounts.setCurrentItem(i)

    def data_changed(self):
        i = self.accounts.currentItem()
        if i is not None:
            data = self.edit_account.data
            i.setText(data['username'])
            i.setData(Qt.UserRole, data)

    def accept(self):
        accounts = [self.accounts.item(i).data(Qt.UserRole) for i in range(self.accounts.count())]
        accounts = list(filter(lambda a: bool(a['username']), accounts))
        self.db.set_accounts(self.key, accounts)
        Dialog.accept(self)


class PasswordManager(Dialog):

    def __init__(self, db, parent=None):
        self.db = db
        Dialog.__init__(self, _('Password Manager'), 'password-manager', parent=parent)

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
        v.activated.connect(self.item_activated)
        l.addWidget(v)
        le.textChanged.connect(pm.setFilterFixedString)

        self.bb.setStandardButtons(self.bb.Close)
        l.addWidget(self.bb)
        self.bb.addButton(_('Import from LastPass'), self.bb.ActionRole).clicked.connect(self.import_from_lastpass)
        self.bb.addButton(_('Change password'), self.bb.ActionRole).clicked.connect(self.change_password)
        self.bb.addButton(_('Add entry'), self.bb.ActionRole).clicked.connect(self.add_entry)
        self.bb.addButton(_('Remove selected'), self.bb.ActionRole).clicked.connect(self.remove_selected)
        self.bb.button(self.bb.Close).setDefault(True)

    def item_activated(self, index):
        if index.isValid():
            EditItem(self.db, index.data(Qt.DisplayRole), parent=self).exec_()

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

    def import_from_lastpass(self):
        csv = choose_files('import-lastpass-csv', self, _('Choose file with exported passwords'),
                           filters=[(_('CSV files'), 'csv')], select_only_single_file=True)
        if csv:
            import_lastpass_db(csv, self.db)
            self.model.refresh(self.db)

    def change_password(self):
        d = AskForPassword(parent=self, create_password=True)
        if d.exec_() == d.Accepted:
            with BusyCursor():
                self.db.change_password(d.password)


class AskForPassword(Dialog):

    def __init__(self, parent=None, create_password=False):
        self.create_password = create_password
        Dialog.__init__(self, _('Master password required'), 'master-password-input', parent=parent)

    def setup_ui(self):
        self.l = l = QVBoxLayout(self)
        self.la = la = QLabel(_('Enter the master password for the password manager'))
        la.setWordWrap(True)
        l.addWidget(la)
        self.pw = pw = QLineEdit(self)
        pw.setEchoMode(pw.Password)
        l.addWidget(pw)
        self.showp = sp = QCheckBox(_('&Show password'), self)
        l.addWidget(sp)
        sp.toggled.connect(lambda show: pw.setEchoMode(pw.Normal if show else pw.Password))
        if self.create_password:
            self.la2 = la = QLabel(_('Confirm (re-enter) the password'))
            l.addWidget(la)
            self.confirm = c = QLineEdit(self)
            l.addWidget(c)
        l.addWidget(self.bb)

    @property
    def password(self):
        return self.pw.text()

    def accept(self):
        if self.create_password and self.password != self.confirm.text():
            return error_dialog(self, _('Passwords do not match'), _(
                'The password and its confirmation do not match'))
        Dialog.accept(self)

    def sizeHint(self):
        ans = Dialog.sizeHint(self)
        ans.setWidth(max(ans.width(), 400))
        return ans


def standalone(password, path=None):
    from ..main import Application
    db = PasswordDB(password, path)
    app = Application([])
    d = PasswordManager(db)
    d.exec_()
    sip.delete(d)
    sip.delete(app)
