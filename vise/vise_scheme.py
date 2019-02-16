#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2016, Kovid Goyal <kovid at kovidgoyal.net>

from PyQt5.Qt import QBuffer
from PyQt5.QtWebEngineCore import QWebEngineUrlSchemeHandler

from .downloads import get_downloads_html, filename_icon_data
from .welcome import get_welcome_html


class UrlSchemeHandler(QWebEngineUrlSchemeHandler):

    def requestStarted(self, rq):
        if bytes(rq.requestMethod()) != b'GET':
            rq.fail(rq.RequestDenied)
            return
        url = rq.requestUrl()
        q = url.path()
        if q == 'downloads':
            rq.reply(b'text/html', QBuffer(get_downloads_html(), self))
        elif q == 'welcome':
            rq.reply(b'text/html', QBuffer(get_welcome_html(), self))
        elif q.startswith('filename-icon/'):
            q = q.partition('/')[2].strip()
            if q:
                rq.reply(b'image/png', QBuffer(filename_icon_data(q), self))
            else:
                rq.fail(rq.UrlNotFound)
        else:
            rq.fail(rq.UrlNotFound)
