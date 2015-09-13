#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2015, Kovid Goyal <kovid at kovidgoyal.net>

import os
from PyQt5.Qt import QIcon, QPixmap


def get_data_as_file(name):
    base = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'resources')
    return open(os.path.join(base, name), 'rb')


def get_data(name):
    return get_data_as_file(name).read()

_icon_cache = {}


def get_icon(name):
    if not name.startswith('images/'):
        name = 'images/' + name
    try:
        return _icon_cache[name]
    except KeyError:
        raw = get_data_as_file(name).read()
        pixmap = QPixmap()
        pixmap.loadFromData(raw)
        icon = _icon_cache[name] = QIcon()
        icon.addPixmap(pixmap)
        return icon
