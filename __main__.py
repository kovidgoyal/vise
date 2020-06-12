#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2015, Kovid Goyal <kovid at kovidgoyal.net>

import os
import sys

from vise.main import main


def add_webengine_flag(flag):
    val = os.environ.get('QTWEBENGINE_CHROMIUM_FLAGS', '')
    if val:
        val += ' '
    os.environ['QTWEBENGINE_CHROMIUM_FLAGS'] = val + flag


while '--force-dark-mode' in sys.argv:
    add_webengine_flag('--force-dark-mode')
    sys.argv.remove('--force-dark-mode')

if 'auto_proxy' in os.environ:
    add_webengine_flag('--proxy-pac-url=' + os.environ['auto_proxy'])

try:
    import PyQt5.QtWebEngine as dummy
    del dummy
except ImportError:
    raise SystemExit(
        'Your system appears to be missing the qt-webengine package')

main()
