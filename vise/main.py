#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2015, Kovid Goyal <kovid at kovidgoyal.net>

import argparse
import gc

from PyQt5.Qt import QApplication

from .constants import appname, str_version
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
        self.windows = []

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
    del app.windows
    delete_profile()
    del app
    gc.collect(), gc.collect(), gc.collect()
