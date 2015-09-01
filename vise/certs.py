#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2015, Kovid Goyal <kovid at kovidgoyal.net>

import string
import re
import os
from collections import defaultdict
from gettext import gettext as _

import apsw
from PyQt5.Qt import (
    QLabel, QGridLayout, QCheckBox, QWebEngineCertificateError, QStyle
)

from .constants import config_dir
from .settings import gprefs
from .utils import Dialog


def ascii_lowercase(val):
    return re.sub('[%s]' % string.ascii_uppercase, lambda m: m.group().lower(), val)


class Ask(Dialog):

    def __init__(self, msg, parent=None):
        self.msg = msg
        Dialog.__init__(self, _('Unsafe SSL certificate'), 'unsafe-ssl-certificate-confirm', parent)

    def setup_ui(self):
        self.l = l = QGridLayout(self)
        self.ic = la = QLabel(self)
        ic = self.style().standardIcon(QStyle.SP_MessageBoxWarning)
        la.setPixmap(ic.pixmap(64, 64))
        l.addWidget(la, 0, 0)
        self.la = la = QLabel(self.msg)
        la.setWordWrap(True)
        l.addWidget(la, 0, 1)
        self.permanent = p = QCheckBox(_('Permanently store exception for this site'))
        p.setToolTip(_('If checked you will never be asked for confirmation for this site again,'
                       '\notherwise, you will be asked again after restarting the browser.'))
        p.setChecked(gprefs.get('permanently_store_ssl_exception', True))
        p.toggled.connect(lambda: gprefs.set('permanently_store_ssl_exception', p.isChecked()))
        l.addWidget(p, 1, 0, 1, -1)
        l.addWidget(self.bb, 2, 0, 1, -1)
        self.bb.setStandardButtons(self.bb.Yes | self.bb.No)
        l.setColumnStretch(1, 100)

    def sizeHint(self):
        ans = Dialog.sizeHint(self)
        ans.setWidth(ans.width() + 150)
        return ans


class CertExceptions:

    def __init__(self):
        self._conn = None
        self.path = os.path.join(config_dir, 'cert-exceptions.sqlite')
        self.temporary = defaultdict(set)

    @property
    def conn(self):
        if self._conn is None:
            self._conn = apsw.Connection(self.path)
            c = self._conn.cursor()
            uv = next(c.execute('PRAGMA user_version'))[0]
            if uv == 0:
                c.execute(
                    'CREATE TABLE exceptions (id INTEGER PRIMARY KEY, domain TEXT NOT NULL, type TEXT NOT NULL, UNIQUE(domain, type)); PRAGMA user_version=1;')
            c.close()
        return self._conn

    def add_exception(self, domain, etype, permanent=True):
        domain = ascii_lowercase(domain)
        etype = str(etype)
        if permanent:
            c = self.conn.cursor()
            c.execute('INSERT OR REPLACE INTO exceptions(domain, type) VALUES (?, ?)', (domain, etype))
        else:
            self.temporary[domain].add(etype)

    def has_exception(self, domain, etype):
        domain = ascii_lowercase(domain)
        etype = str(etype)
        if etype in self.temporary[domain]:
            return True
        try:
            next(self.conn.cursor().execute('SELECT domain FROM exceptions WHERE domain=? AND type=?', (domain, etype)))
            return True
        except StopIteration:
            pass
        return False

    def ask(self, domain, code, parent=None):
        domain = ascii_lowercase(domain)
        if code == QWebEngineCertificateError.CertificateAuthorityInvalid:
            msg = _('The SSL certificate for {0} has an unknown certificate authority'
                    ' do you want to trust it nevertheless?')
        elif code == QWebEngineCertificateError.CertificateWeakSignatureAlgorithm:
            msg = _('The SSL certificate for {0} uses a weak signature algorithm,'
                    ' do you want to trust it nevertheless?')
        else:
            return False
        msg = msg.format('<i>%s</i>' % domain)
        d = Ask(msg, parent=parent)
        if d.exec_() == d.Accepted:
            self.add_exception(domain, code, permanent=d.permanent.isChecked())
            return True
        return False

cert_exceptions = CertExceptions()


def handle_qt_ssl_error(reply, errors):
    domain = reply.url().host()
    for e in errors:
        err = e.error()
        if (
                err in (e.SelfSignedCertificate, e.SelfSignedCertificateInChain, e.UnableToGetLocalIssuerCertificate, e.UnableToVerifyFirstCertificate) and
                cert_exceptions.has_exception(domain, QWebEngineCertificateError.CertificateAuthorityInvalid)
        ):
            continue
        return
    reply.ignoreSslErrors()
