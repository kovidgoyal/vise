#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2016, Kovid Goyal <kovid at kovidgoyal.net>

import json

from PyQt5.Qt import QWebEngineView, QWebEngineScript


signals = {}


def python_to_js(page_or_tab, name, *args):
    page = page_or_tab.page() if isinstance(page_or_tab, QWebEngineView) else page_or_tab
    page.runJavaScript('window.send_message_to_javascript(%s, %s)' % (json.dumps(name), json.dumps(args)), QWebEngineScript.ApplicationWorld)


def connect_signal(name=None, func_name=None):
    def connect(f):
        fname = func_name or f.__name__
        n = name or fname
        if n in signals:
            raise KeyError('A signal with the name of %s has already been connected' % name)

        signals[n] = fname
        return f
    return connect


def js_to_python(page, name, args):
    func_name = signals.get(name)
    if func_name is None:
        print('Unknown signal received from js:', name)
        return
    func = getattr(page, func_name, None)
    if func is None:
        func = getattr(page.parent(), func_name, None)
    if func is None:
        print('Unknown signal received from js:', name)
        return
    func = getattr(func, 'emit', func)
    func(*args)
