#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2015, Kovid Goyal <kovid at kovidgoyal.net>

import argparse
import gc
import os
import sys
import traceback
import json
import tempfile
from datetime import datetime
from gettext import gettext as _

from PyQt5.Qt import (
    QApplication, QFontDatabase, QNetworkAccessManager, QNetworkDiskCache,
    QLocalSocket, QLocalServer, QSslSocket, QTextStream, QAbstractSocket,
    QTimer, QDialog
)

from .constants import appname, str_version, cache_dir, iswindows
from .downloads import Downloads
from .keys import KeyFilter
from .message_box import error_dialog
from .settings import delete_profile
from .window import MainWindow
from .utils import parse_url
from .certs import handle_qt_ssl_error
from .places import places

app = ADDRESS = None


def option_parser():
    parser = argparse.ArgumentParser(description='Run the {} browser'.format(appname))
    parser.add_argument('--shell', action='store_true', default=False, help=_(
        'Start an interactive shell'))
    parser.add_argument('-c', '--cmd', default=None, help=_(
        'Run python code in the vise context'))
    parser.add_argument('urls', metavar='URL', nargs='*', help='urls to open')
    return parser


def create_favicon_cache():
    c = QNetworkDiskCache()
    c.setCacheDirectory(os.path.join(cache_dir, 'favicons'))
    c.setMaximumCacheSize(10 * 1024 * 1024)
    return c


class Application(QApplication):

    def __init__(self, args):
        QApplication.__init__(self, [])
        if not QSslSocket.supportsSsl():
            raise SystemExit('Qt has been compiled without SSL support!')

        self.run_local_server(args)
        sys.excepthook = self.on_unhandled_error
        self.windows = []
        f = self.font()
        if (f.family(), f.pointSize()) == ('Sans Serif', 9):  # Hard coded Qt settings, no user preference detected
            f.setPointSize(10)
            if 'Ubuntu' in QFontDatabase().families():
                f.setFamily('Ubuntu')
            self.setFont(f)
        self.network_access_manager = nam = QNetworkAccessManager(self)
        self.downloads = Downloads(self)
        nam.sslErrors.connect(handle_qt_ssl_error)
        self.disk_cache = c = create_favicon_cache()
        nam.setCache(c)
        self.key_filter = KeyFilter(self)
        self.installEventFilter(self.key_filter)

    def run_local_server(self, args):
        prefix = r'\\.\pipe' if iswindows else tempfile.gettempdir().rstrip('/')
        server_name = prefix + os.sep + appname + '-local-server'
        s = QLocalSocket()
        s.connectToServer(server_name)
        if s.waitForConnected(500):
            stream = QTextStream(s)
            stream.setCodec('UTF-8')
            cargs = json.dumps({'open': args.urls}, ensure_ascii=False)
            stream << cargs
            stream.flush()
            s.waitForBytesWritten()
            raise SystemExit(0)
        self.local_server = ls = QLocalServer(self)
        ls.newConnection.connect(self.another_instance_wants_to_talk)
        if not ls.listen(server_name):
            if ls.serverError() == QAbstractSocket.AddressInUseError:
                try:
                    os.remove(server_name)
                except FileNotFoundError:
                    pass
            if not ls.listen(server_name):
                raise SystemExit('Failed to establish local listening socket at: %s with error: %s' % (
                    server_name, ls.errorString()))

    def another_instance_wants_to_talk(self):
        s = self.local_server.nextPendingConnection()
        if s is None:
            return
        s.waitForReadyRead(1000)
        stream = QTextStream(s)
        stream.setCodec('UTF-8')
        try:
            command = json.loads(stream.readAll())
        except Exception as e:
            self.error('Invalid data from other instance: %s' % e)
            return
        finally:
            s.close()
            del s
        if not isinstance(command, dict):
            self.error('Invalid data from other instance: %r' % command)
            return
        urls = command.get('open', [])
        if not isinstance(urls, list):
            self.error('Invalid data from other instance: %r' % command)
            return
        urls = [x for x in urls if isinstance(x, str)]
        if urls:
            self.open_urls(urls, in_current_tab=False)

    def new_window(self, is_private=False):
        w = MainWindow(is_private=is_private)
        self.windows.append(w)
        return w

    def remove_window(self, window):
        window.break_cycles()
        try:
            self.windows.remove(window)
        except ValueError:
            pass

    def open_urls(self, urls, in_current_tab=True):
        if not self.windows:
            self.new_window().show()
        w = self.activeWindow() or self.windows[0]
        for i, url in enumerate(urls):
            w.open_url(parse_url(url), in_current_tab=in_current_tab and i == 0)

    def error(self, *args, **kwargs):
        kwargs['file'] = sys.stderr
        prefix = '[%s %s]' % (appname, datetime.now().isoformat(' '))
        try:
            print(prefix, *args, **kwargs)
        except OSError:
            pass

    def on_unhandled_error(self, etype, value, tb):
        if etype == KeyboardInterrupt:
            return
        sys.__excepthook__(etype, value, tb)
        try:
            msg = str(value)
        except Exception:
            msg = repr(value)
        msg = '<p>' + msg + '<br>' + _('Click "Show details" for more information')
        det_msg = '%s: %s\n%s' % (appname, str_version, ''.join(traceback.format_exception(etype, value, tb)))
        parent = self.activeWindow()
        d = error_dialog(parent, _('Unhandled exception'), msg, det_msg=det_msg, show=False)
        d.shutdown_button = d.bb.addButton(_('Shutdown'), d.bb.RejectRole)
        ret = d.exec_()
        if ret == QDialog.Rejected:
            QApplication.instance().exit(1)

    def break_cycles(self):
        # Make sure the application object has no references in python and the
        # other global objects can also be garbage collected
        self.local_server.close()
        self.downloads.break_cycles()
        for w in self.windows:
            w.break_cycles()
            w.deleteLater()
        del self.windows, self.network_access_manager, self.local_server
        sys.excepthook = sys.__excepthook__


def run_app(urls=(), callback=None, callback_wait=0):
    env = os.environ.copy()
    app = Application([])
    app.setOrganizationName('kovidgoyal')
    app.setApplicationName(appname)
    app.setApplicationVersion(str_version)
    app.original_env = env
    try:
        app.open_urls(urls)
        if callback is not None:
            QTimer.singleShot(callback_wait, callback)
        app.exec_()
    finally:
        # Without the following cleanup code, PyQt segfaults on exit
        app.break_cycles()
        delete_profile()
        places.close()
        app.sendPostedEvents()
        del app
        gc.collect(), gc.collect(), gc.collect()


def main():
    global app
    parser = option_parser()
    args = parser.parse_args()
    if args.cmd:
        exec(args.cmd)
        raise SystemExit(0)
    elif args.shell:
        from .utils import ipython
        ipython()
        raise SystemExit(0)

    run_app(args.urls)
