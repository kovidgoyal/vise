#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2015, Kovid Goyal <kovid at kovidgoyal.net>

import os
from functools import lru_cache

from PyQt5.Qt import QIcon


def get_data_as_path(name):
    base = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'resources')
    return os.path.join(base, name)


def get_data_as_file(name):
    return open(get_data_as_path(name), 'rb')


def get_data(name):
    return get_data_as_file(name).read()


@lru_cache(maxsize=512)
def get_icon(name):
    if not name.startswith('images/'):
        name = 'images/' + name
    return QIcon(get_data_as_path(name))
