#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2015, Kovid Goyal <kovid at kovidgoyal.net>

import re

from PyQt5.Qt import QUrl

upat = re.compile(r'[a-zA-Z0-9]+://')


def parse_url(url_or_path):
    if upat.match(url_or_path) is not None:
        return QUrl(url_or_path)
    return QUrl.fromLocalFile(url_or_path)
