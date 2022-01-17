#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2015, Kovid Goyal <kovid at kovidgoyal.net>

from gettext import gettext as _

from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import QLineEdit, QCheckBox, QFormLayout, QLabel, QDialog

from .utils import Dialog
from .message_box import error_dialog


class Credentials(Dialog):

    def __init__(self, msg, parent=None):
        self.msg = msg
        Dialog.__init__(self, _('Password needed'), 'http-auth-credentials', parent)

    def setup_ui(self):
        self.l = l = QFormLayout(self)
        l.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)
        self.la = la = QLabel(self.msg)
        la.setMinimumWidth(450)
        la.setWordWrap(True)
        l.addRow(la)
        self.username = un = QLineEdit(self)
        l.addRow(_('&Username:'), un)
        self.password = pw = QLineEdit(self)
        l.addRow(_('&Password:'), pw)
        pw.setEchoMode(QLineEdit.EchoMode.Password)
        self.pwt = c = QCheckBox(_('&Show password'), self)
        l.addRow(c)
        c.toggled.connect(self.show_password_toggled)
        l.addRow(self.bb)

    def show_password_toggled(self):
        self.pwt.setEchoMode(QLineEdit.EchoMode.Normal if self.pwt.isChecked() else QLineEdit.EchoMode.Password)

    @property
    def credentials(self):
        return self.username.text(), self.password.text()

    @credentials.setter
    def credentials(self, x):
        self.username.setText(x[0])
        self.password.setText(x[1])

    def accept(self):
        un, pw = self.credentials
        if not un or not pw:
            return error_dialog(self, _('Data required'), _(
                'You must specify the username and password'))
        return Dialog.accept(self)


def get_http_auth_credentials(qurl, authenticator, parent=None):
    qurl = QUrl(qurl)
    qurl.setFragment(None)
    realm = authenticator.realm()
    trealm = (' (%s)' % realm) if realm else ''
    ac = parent and parent.get_login_credentials(qurl.toString())
    d = Credentials(_('Please specify a password for {0}{1}').format(qurl.toString(), trealm), parent)
    if ac is not None:
        if ac['autologin']:
            authenticator.setUser(ac['username'])
            authenticator.setPassword(ac['password'])
            return
        d.credentials = ac['username'], ac['password']

    if d.exec() == QDialog.DialogCode.Accepted:
        username, password = d.credentials
        authenticator.setUser(username)
        authenticator.setPassword(password)
        if parent is not None:
            parent.on_login_form_submit(qurl.toString(), username, password)
    else:
        if parent is not None:
            parent.setHtml('<p style="font-family:sans-serif">{} {}</p>'.format(
                _('Authentication required to access: '), '<a href="{0}">{0}</a>'.format(qurl.toDisplayString())))


def get_proxy_auth_credentials(qurl, authenticator, proxy_host, parent=None):
    qurl = QUrl(qurl)
    qurl.setFragment(None)
    d = Credentials(_('Please specify a password for {0} at the proxy: {1}').format(qurl.toString(), proxy_host), parent)
    if d.exec() == d.Accepted:
        username, password = d.credentials
        authenticator.setUser(username)
        authenticator.setPassword(password)
