#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2015, Kovid Goyal <kovid at kovidgoyal.net>

import os


def get_data_as_file(name):
    base = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'resources')
    return open(os.path.join(base, name), 'rb')
