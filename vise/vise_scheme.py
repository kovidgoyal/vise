#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2016, Kovid Goyal <kovid at kovidgoyal.net>

from PyQt5.Qt import QWebEngineUrlSchemeHandler, QBuffer

from .downloads import get_downloads_html


class UrlSchemeHandler(QWebEngineUrlSchemeHandler):

    def requestStarted(self, rq):
        if bytes(rq.requestMethod()) != b'GET':
            rq.fail(rq.RequestDenied)
            return
        url = rq.requestUrl()
        q = url.path()
        if q == 'downloads':
            rq.reply(b'text/html', QBuffer(get_downloads_html(), self))
        else:
            rq.fail(rq.UrlNotFound)
