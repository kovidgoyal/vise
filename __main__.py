#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2015, Kovid Goyal <kovid at kovidgoyal.net>

import os

from vise.main import main


def add_webengine_flag(flag):
    val = os.environ.get('QTWEBENGINE_CHROMIUM_FLAGS', '')
    if val:
        val += ' '
    os.environ['QTWEBENGINE_CHROMIUM_FLAGS'] = val + flag


add_webengine_flag('--force-dark-mode')

if 'auto_proxy' in os.environ:
    add_webengine_flag('--proxy-pac-url=' + os.environ['auto_proxy'])

try:
    import PyQt6.QtWebEngineWidgets as dummy
    del dummy
except ImportError:
    raise SystemExit(
        'Your system appears to be missing the qt-webengine package')

main()
