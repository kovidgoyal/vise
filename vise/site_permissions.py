#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2016, Kovid Goyal <kovid at kovidgoyal.net>

import os
from collections import defaultdict

import apsw
from PyQt6.QtCore import QUrl

from .constants import config_dir
from .utils import ascii_lowercase


class Permissions:

    def __init__(self):
        self._conn = None
        self.path = os.path.join(config_dir, 'site-permissions.sqlite')
        self.temporary = defaultdict(set)

    @property
    def conn(self):
        if self._conn is None:
            self._conn = apsw.Connection(self.path)
            c = self._conn.cursor()
            uv = next(c.execute('PRAGMA user_version'))[0]
            if uv == 0:
                c.execute(
                    'CREATE TABLE permissions (id INTEGER PRIMARY KEY, domain TEXT NOT NULL, type TEXT NOT NULL, UNIQUE(domain, type)); PRAGMA user_version=1;')
            c.close()
        return self._conn

    def has_permission(self, qurl_or_domain, permission_type):
        domain = qurl_or_domain
        if isinstance(domain, QUrl):
            domain = domain.host()
        domain = ascii_lowercase(domain)
        if permission_type in self.temporary[domain]:
            return True
        try:
            next(self.conn.cursor().execute('SELECT domain FROM permissions WHERE domain=? AND type=?', (domain, permission_type)))
            return True
        except StopIteration:
            pass
        return False

    def add_permission(self, qurl_or_domain, permission_type, permanent=True):
        domain = qurl_or_domain
        if isinstance(domain, QUrl):
            domain = domain.host()
        domain = ascii_lowercase(domain)
        if permanent:
            c = self.conn.cursor()
            c.execute('INSERT OR REPLACE INTO permissions(domain, type) VALUES (?, ?)', (domain, permission_type))
        else:
            self.temporary[domain].add(permission_type)


site_permissions = Permissions()
