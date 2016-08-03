#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2016, Kovid Goyal <kovid at kovidgoyal.net>

import base64

from PyQt5.Qt import QUrl, QByteArray

from .constants import WELCOME_URL as WU
from .resources import get_icon, get_data

WELCOME_URL = QUrl(WU)


def welcome_icon():
    if not hasattr(welcome_icon, 'icon'):
        welcome_icon.icon = get_icon('vise.svg')
    return welcome_icon.icon


def get_welcome_html():
    if not hasattr(get_welcome_html, 'html'):
        d = get_data('welcome.html').decode('utf-8')
        ic = get_data('images/vise.svg')
        d = d.replace('VISE_ICON', 'data:image/svg+xml;base64,' + base64.standard_b64encode(ic).decode('ascii'))
        get_welcome_html.html = QByteArray(d.encode('utf-8'))
    return get_welcome_html.html
