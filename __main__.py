#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2015, Kovid Goyal <kovid at kovidgoyal.net>

try:
    import PyQt5.QtWebEngine as dummy
    del dummy
except ImportError:
    raise SystemExit(
        'Your system appears to be missing the qt-webengine package')

from vise.main import main
main()
