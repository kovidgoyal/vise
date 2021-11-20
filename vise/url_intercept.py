#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2016, Kovid Goyal <kovid at kovidgoyal.net>

from gettext import gettext as _

from PyQt6.QtCore import QUrl
from PyQt6.QtWebEngineCore import QWebEngineUrlRequestInterceptor

from .url_substitution import substitute


class Interceptor(QWebEngineUrlRequestInterceptor):

    def interceptRequest(self, req):
        qurl = req.requestUrl()
        url = qurl.toString()
        changed, nurl = substitute(url)
        if changed:
            print(_('Redirecting {0} to {1} because of a URL substitution rule').format(url, nurl))
            req.redirect(QUrl(nurl))
