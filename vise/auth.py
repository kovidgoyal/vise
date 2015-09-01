#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2015, Kovid Goyal <kovid at kovidgoyal.net>

from gettext import gettext as _

from PyQt5.Qt import QUrl, QLineEdit, QCheckBox, QFormLayout, QLabel

from .utils import Dialog
from .message_box import error_dialog


class Credentials(Dialog):

    def __init__(self, msg, parent=None):
        self.msg = msg
        Dialog.__init__(self, _('Password needed'), 'http-auth-credentials', parent)

    def setup_ui(self):
        self.l = l = QFormLayout(self)
        l.setFieldGrowthPolicy(l.ExpandingFieldsGrow)
        self.la = la = QLabel(self.msg)
        la.setWordWrap(True)
        l.addRow(la)
        self.username = un = QLineEdit(self)
        l.addRow(_('&Username:'), un)
        self.password = pw = QLineEdit(self)
        l.addRow(_('&Password:'), pw)
        pw.setEchoMode(QLineEdit.Password)
        self.pwt = c = QCheckBox(_('&Show password'), self)
        l.addRow(c)
        c.toggled.connect(lambda: pw.setEchoMode(QLineEdit.Normal if c.isChecked() else QLineEdit.Password))
        l.addRow(self.bb)

    @property
    def credentials(self):
        return self.username.text(), self.password.text()

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
    d = Credentials(_('Please specify a password for {0}{1}').format(qurl.toString(), trealm), parent)
    if d.exec_() == d.Accepted:
        username, password = d.credentials
        authenticator.setUser(username)
        authenticator.setPassword(password)


def get_proxy_auth_credentials(qurl, authenticator, proxy_host, parent=None):
    qurl = QUrl(qurl)
    qurl.setFragment(None)
    d = Credentials(_('Please specify a password for {0} at the proxy: {1}').format(qurl.toString(), proxy_host), parent)
    if d.exec_() == d.Accepted:
        username, password = d.credentials
        authenticator.setUser(username)
        authenticator.setPassword(password)
