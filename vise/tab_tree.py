#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2015, Kovid Goyal <kovid at kovidgoyal.net>

from PyQt5.Qt import QTreeView


class TabTree(QTreeView):

    def __init__(self, parent):
        QTreeView.__init__(self, parent)
