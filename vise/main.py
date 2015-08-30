#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2015, Kovid Goyal <kovid at kovidgoyal.net>

import argparse
import gc
import os
import sys
import traceback
from datetime import datetime
from gettext import gettext as _

from PyQt5.Qt import (
    QApplication, QFontDatabase, QNetworkAccessManager, QNetworkDiskCache
)

from .constants import appname, str_version, cache_dir
from .message_box import error_dialog
from .settings import delete_profile
from .window import MainWindow
from .utils import parse_url

app = None


def option_parser():
    parser = argparse.ArgumentParser(description='Run the {} browser'.format(appname))
    parser.add_argument('urls', metavar='URL', nargs='*', help='urls to open')
    return parser


class Application(QApplication):

    def __init__(self, args):
        QApplication.__init__(self, [])
        sys.excepthook = self.on_unhandled_error
        self.windows = []
        f = self.font()
        if (f.family(), f.pointSize()) == ('Sans Serif', 9):  # Hard coded Qt settings, no user preference detected
            f.setPointSize(10)
            if 'Ubuntu' in QFontDatabase().families():
                f.setFamily('Ubuntu')
            self.setFont(f)
        self.network_access_manager = nam = QNetworkAccessManager(self)
        c = QNetworkDiskCache(nam)
        c.setCacheDirectory(os.path.join(cache_dir, 'favicons'))
        c.setMaximumCacheSize(10 * 1024 * 1024)
        nam.setCache(c)

    def new_window(self, is_private=False):
        w = MainWindow(is_private=is_private)
        self.windows.append(w)
        return w

    def remove_window(self, window):
        try:
            self.windows.remove(window)
        except ValueError:
            pass

    def open_urls(self, urls):
        if not self.windows:
            self.new_window().show()
        w = self.windows[0]
        for i, url in enumerate(urls):
            w.open_url(parse_url(url), in_current_tab=i == 0)

    def error(self, *args, **kwargs):
        kwargs['file'] = sys.stderr
        prefix = '[%s %s]' % (appname, datetime.now().isoformat(' '))
        try:
            print(prefix, *args, **kwargs)
        except OSError:
            pass

    def on_unhandled_error(self, etype, value, tb):
        if type == KeyboardInterrupt:
            return
        sys.__excepthook__(etype, value, tb)
        try:
            msg = str(value)
        except Exception:
            msg = repr(value)
        msg = '<p>' + msg + '<br>' + _('Click "Show details" for more information')
        det_msg = '%s: %s\n%s' % (appname, str_version, ''.join(traceback.format_exception(type, value, tb)))
        parent = self.activeWindow()
        error_dialog(parent, _('Unhandled exception'), msg, det_msg=det_msg)

    def break_cycles(self):
        # Make sure the application object has no references in python and the
        # other global objects can also be garbage collected
        del self.windows, self.network_access_manager
        sys.excepthook = sys.__excepthook__


def main():
    global app
    parser = option_parser()
    args = parser.parse_args()
    app = Application(args)
    app.setOrganizationName('kovidgoyal')
    app.setApplicationName(appname)
    app.setApplicationVersion(str_version)
    app.open_urls(args.urls)
    app.exec_()
    app.break_cycles()
    delete_profile()
    del app
    gc.collect(), gc.collect(), gc.collect()
