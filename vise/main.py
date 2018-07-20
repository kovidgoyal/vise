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
import socket
import signal
import struct
import pickle
from datetime import datetime
from gettext import gettext as _

from PyQt5 import sip
from PyQt5.Qt import (
    QApplication, QFontDatabase, QNetworkDiskCache, QLocalSocket, QLocalServer,
    QSslSocket, QTextStream, QAbstractSocket, QTimer, Qt, pyqtSignal,
    QSocketNotifier, QNetworkCacheMetaData
)

from .constants import appname, str_version, cache_dir, iswindows, isosx, local_socket_address, config_dir
from .downloads import Downloads
from .keys import KeyFilter
from .message_box import error_dialog
from .settings import delete_profile
from .window import MainWindow
from .utils import parse_url, BusyCursor, icon_to_data, pipe2
from .places import places
from .passwd.db import password_db, key_from_url
from .style import Style
from .welcome import WELCOME_URL

ADDRESS = None


def option_parser():
    parser = argparse.ArgumentParser(description='Run the {} browser'.format(appname))
    parser.add_argument('--shell', action='store_true', default=False, help=_(
        'Start an interactive shell'))
    parser.add_argument('-c', '--cmd', default=None, help=_(
        'Run python code in the vise context'))
    parser.add_argument('--pw-from-stdin', action='store_true', default=False, help=_(
        'Read the master password for the password manager from stdin'))
    parser.add_argument('--new-instance', action='store_true', default=False, help=_(
        'Do not try to connect to an already running instance'))
    parser.add_argument('--shutdown', action='store_true', default=False, help=_(
        'Shutdown a running vise instance, if any'))
    parser.add_argument('--no-session', action='store_true', default=False, help=_(
        'Do not save/restore the session at shutdown/startup'))
    parser.add_argument('--startup-session', default=None, help=_(
        'Path to a session previously saved with the export command. It will'
        ' be used to startup this instance of vise. Note that if vise is already'
        ' running this will have no effect'))
    parser.add_argument('urls', metavar='URL', nargs='*', help='urls to open')
    return parser


def create_favicon_cache():
    c = QNetworkDiskCache()
    c.setCacheDirectory(os.path.join(cache_dir, 'favicons'))
    c.setMaximumCacheSize(25 * 1024 * 1024)
    return c


class Application(QApplication):

    password_loaded = pyqtSignal(object, object)

    def __init__(self, master_password=None, urls=(), new_instance=False, shutdown=False, restart_state=None, no_session=False, run_local_server=True):
        if not isosx:  # OS X turns this on automatically
            for v in ('QT_AUTO_SCREEN_SCALE_FACTOR', 'QT_SCALE_FACTOR', 'QT_SCREEN_SCALE_FACTORS', 'QT_DEVICE_PIXEL_RATIO'):
                if os.environ.get(v):
                    break
            else:
                QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        QApplication.__init__(self, [appname, '-name', appname])
        self.setAttribute(Qt.AA_UseHighDpiPixmaps)
        self.setOrganizationName('kovidgoyal')
        self.setApplicationName(appname)
        self.setApplicationVersion(str_version)
        self.no_session = no_session
        self.handle_unix_signals()
        if not QSslSocket.supportsSsl():
            raise SystemExit('Qt has been compiled without SSL support!')
        from .config import font_families, font_sizes
        ff = font_families().get('sans-serif') or 'default'
        if ff == 'default':
            ff = font_families().get('default') or 'default'
        f = self.font()
        if ff != 'default':
            f.setFamily(ff)
            fs = font_sizes().get('default-size')
            try:
                f.setPixelSize(int(fs))
            except Exception:
                pass
        self.setFont(f)
        self.password_loaded.connect(self.on_password_load, type=Qt.QueuedConnection)
        if master_password is not None:
            password_db.start_load(master_password, self.password_loaded.emit)
        elif restart_state and 'key' in restart_state:
            password_db.start_load(restart_state.pop('key'), self.password_loaded.emit, pw_is_key=True)

        self.lastWindowClosed.connect(self.shutdown)
        if run_local_server:
            self.run_local_server(urls, new_instance, shutdown)
        sys.excepthook = self.on_unhandled_error
        self.windows = []
        f = self.font()
        if (f.family(), f.pointSize()) == ('Sans Serif', 9):  # Hard coded Qt settings, no user preference detected
            f.setPointSize(10)
            if 'Ubuntu' in QFontDatabase().families():
                f.setFamily('Ubuntu')
            self.setFont(f)
        self.downloads = Downloads(self)
        self.disk_cache = create_favicon_cache()
        self.key_filter = KeyFilter(self)
        self.installEventFilter(self.key_filter)

    def handle_unix_signals(self):
        if iswindows:
            # TODO: test this on windows
            self.signal_read_socket, self.signal_write_socket = socket.socketpair()
            self.signal_read_socket.setblocking(False)
            self.signal_write_socket.setblocking(False)
            read_fd, write_fd = self.signal_read_socket.fileno(), self.signal_write_socket.fileno()
        else:
            read_fd, write_fd = pipe2()
        for sig in (signal.SIGINT, signal.SIGTERM):
            signal.signal(sig, lambda x, y: None)
            signal.siginterrupt(sig, False)
        signal.set_wakeup_fd(write_fd)
        self.signal_notifier = QSocketNotifier(read_fd, QSocketNotifier.Read, self)
        self.signal_notifier.setEnabled(True)
        self.signal_notifier.activated.connect(self.signal_received, type=Qt.QueuedConnection)

    def signal_received(self, read_fd):
        try:
            data = self.signal_read_socket.recv(1024) if iswindows else os.read(read_fd, 1024)
        except BlockingIOError:
            return
        if data:
            signals = struct.unpack('%uB' % len(data), data)
            if signal.SIGINT in signals or signal.SIGTERM in signals:
                self.shutdown()

    def show_password_load_error(self, error, tb, parent=None):
        error_dialog(parent or (self.windows[0] if self.windows else None), _('Failed to load password database'), _(
            'There was an error processing the password database:') + '<br>' + str(error), det_msg=tb, show=True)

    def on_password_load(self, error, tb):
        if error:
            self.show_password_load_error(error, tb)

    def ask_for_master_password(self, parent=None):
        from .passwd.gui import AskForPassword
        with BusyCursor():
            pw_loaded = password_db.join()
        if not pw_loaded:
            while True:
                d = AskForPassword(parent=parent, create_password=not password_db.has_password())
                if d.exec_() != AskForPassword.Accepted:
                    return
                with BusyCursor():
                    password_db.start_load(d.password)
                    password_db.join()
                if password_db.error[0] is None:
                    break
                self.show_password_load_error(password_db.error[0], password_db.error[1], parent=parent)
        return password_db.is_loaded

    def store_password(self, url, username, password):
        key = key_from_url(url)
        password_db.add_account(key, username, password)

    def run_local_server(self, urls, new_instance, shutdown):
        if shutdown:
            new_instance = False
        server_name = local_socket_address()
        s = QLocalSocket()
        s.connectToServer(server_name)
        if s.waitForConnected(500):
            if new_instance:
                return
            stream = QTextStream(s)
            stream.setCodec('UTF-8')
            if shutdown:
                cargs = json.dumps({'action': 'shutdown'})
            else:
                cargs = json.dumps({'open': urls}, ensure_ascii=False)
            stream << cargs
            stream.flush()
            s.waitForBytesWritten()
            raise SystemExit(0)
        if shutdown:
            raise SystemExit('No running vise instance found')
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
        raw = stream.readAll()
        try:
            command = json.loads(raw)
        except Exception as e:
            self.error('Invalid data from other instance: %s' % e)
            return
        finally:
            s.close()
            del s
        if not isinstance(command, dict):
            self.error('Invalid data from other instance: %r' % command)
            return
        ac = command.get('action')
        if ac == 'shutdown':
            return self.shutdown()
        urls = command.get('open', [])
        if not isinstance(urls, list):
            self.error('Invalid data from other instance: %r' % command)
            return
        urls = [x for x in urls if isinstance(x, str)]
        if urls:
            self.open_urls(urls, in_current_tab='dynamic', switch_to_tab=True)

    def save_favicon_in_cache(self, icon, qurl):
        md = QNetworkCacheMetaData()
        md.setUrl(qurl)
        md.setSaveToDisk(True)
        dio = self.disk_cache.prepare(md)
        if dio:
            ic = icon_to_data(icon, w=None)
            if ic:
                while len(ic) > 0:
                    written = dio.write(ic)
                    if written < 0:
                        print('Failed to save favicon with error:', dio.errorString())
                        return  # error occurred
                    ic = ic[written:]
                self.disk_cache.insert(dio)

    def shutdown(self):
        self.lastWindowClosed.disconnect()
        if not self.no_session:
            state = self.serialize_state()
            state = pickle.dumps(state, pickle.HIGHEST_PROTOCOL)
            f = tempfile.NamedTemporaryFile(dir=cache_dir)
            try:
                f.write(state)
                os.replace(f.name, os.path.join(cache_dir, 'last-session.pickle'))
            finally:
                try:
                    f.close()
                except FileNotFoundError:
                    pass
        for w in self.windows:
            w.close()

    def new_window(self, is_private=False, restart_state=None):
        w = MainWindow(is_private=is_private, restart_state=restart_state)
        w.window_closed.connect(self.remove_window, type=Qt.QueuedConnection)
        self.windows.append(w)
        return w

    def remove_window(self, window):
        window.break_cycles()
        try:
            self.windows.remove(window)
        except ValueError:
            pass

    def open_urls(self, urls, in_current_tab=True, switch_to_tab=False):
        if not self.windows:
            self.new_window().show()
        w = self.activeWindow() or self.windows[0]
        if in_current_tab == 'dynamic':
            in_current_tab = w.current_tab is not None and w.current_tab.url() == WELCOME_URL
        for i, url in enumerate(urls):
            w.open_url(parse_url(url), in_current_tab=in_current_tab and i == 0, switch_to_tab=switch_to_tab and i == 0)

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
        b = d.shutdown_button = d.bb.addButton(_('Shutdown'), d.bb.ActionRole)
        b.clicked.connect(self.exit_with_error)
        d.exec_()

    def exit_with_error(self):
        self.exit(1)

    def break_cycles(self):
        # Make sure the application object has no references in python and the
        # other global objects can also be garbage collected

        # Reset excepthook otherwise we get a segfault on exit, since the application object is deleted
        # before we exit
        sys.excepthook = sys.__excepthook__
        if hasattr(self, 'local_server'):
            self.local_server.close()
            del self.local_server
        self.downloads.break_cycles()
        for w in self.windows:
            w.break_cycles()
            w.deleteLater()
        for s in (self.password_loaded,):
            s.disconnect()
        del self.windows

    def serialize_state(self, include_favicons=False, include_key=False):
        ans = {'windows': [w.serialize_state(include_favicons) for w in self.windows]}
        w = self.activeWindow()
        if getattr(w, 'window_id', None) is not None:
            ans['active_window'] = w.window_id
        if include_key and password_db.is_loaded and password_db.key and not password_db.key_error:
            ans['key'] = password_db.key
        return ans

    def unserialize_state(self, state):
        active_window = state.get('active_window')
        for wstate in state['windows']:
            w = self.new_window(restart_state=wstate, is_private=wstate['is_private'])
            w.show()
            if wstate['window_id'] == active_window:
                active_window = w
        if hasattr(active_window, 'raise_') and self.activeWindow() != active_window and len(self.windows) > 1:
            w.raise_()

    def restart_app(self):
        password_db.join()
        state = self.serialize_state(include_key=True)
        self.restart_state = pickle.dumps(state, pickle.HIGHEST_PROTOCOL)
        self.no_session = True
        self.shutdown()


def restart(state, env):
    import subprocess
    import shlex
    env['IS_VISE_RESTART'] = '1'
    cmd = [sys.executable, sys.argv[0]]
    if '--new-instance' in sys.argv:
        cmd.append('--new-instance')
    print('Restarting with command:', *map(shlex.quote, cmd))
    p = subprocess.Popen(cmd, env=env, stdin=subprocess.PIPE)
    p.stdin.write(state), p.stdin.flush(), p.stdin.close()


def last_saved_session(no_session):
    if no_session:
        return
    try:
        with open(os.path.join(cache_dir, 'last-session.pickle'), 'rb') as f:
            os.unlink(f.name)
            return pickle.load(f)
    except Exception:
        pass


def run_app(
        urls=(), callback=None, callback_wait=0,
        master_password=None, new_instance=False, shutdown=False, restart_state=None, no_session=False, startup_session=None):
    env = os.environ.copy()
    app = Application(
        master_password=master_password, urls=urls, new_instance=new_instance, shutdown=shutdown, restart_state=restart_state, no_session=no_session)
    os.environ['QTWEBENGINE_DICTIONARIES_PATH'] = os.path.join(config_dir, 'spell')
    app.original_env = env
    style = Style()
    app.setStyle(style)
    try:
        if startup_session is not None:
            with open(startup_session, 'rb') as f:
                app.unserialize_state(pickle.load(f))
        elif restart_state is not None:
            app.unserialize_state(restart_state)
        else:
            last_session = last_saved_session(no_session)
            if last_session is None or urls:
                app.open_urls(urls)
            else:
                app.unserialize_state(last_session)
        if callback is not None:
            QTimer.singleShot(callback_wait, callback)
        app.exec_()
    finally:
        app.break_cycles()
        delete_profile()
        places.close()
        app.sendPostedEvents()
        restart_state = getattr(app, 'restart_state', None)
        original_env = app.original_env
        sip.delete(app)
        del app
        gc.collect(), gc.collect(), gc.collect()
        if restart_state is not None:
            restart(restart_state, original_env)


def main():
    parser = option_parser()
    args = parser.parse_args()
    if args.cmd:
        exec(args.cmd)
        raise SystemExit(0)
    elif args.shell:
        from .utils import ipython
        ipython()
        raise SystemExit(0)

    pw = sys.stdin.read().rstrip() if args.pw_from_stdin else None
    restart_state = None
    if os.environ.pop('IS_VISE_RESTART', None) == '1':
        restart_state = pickle.loads(sys.stdin.buffer.read())

    run_app(args.urls, master_password=pw, new_instance=args.new_instance,
            shutdown=args.shutdown, restart_state=restart_state, no_session=args.no_session,
            startup_session=args.startup_session)
