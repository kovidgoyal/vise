#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2015, Kovid Goyal <kovid at kovidgoyal.net>

import os
import apsw
import json
from base64 import standard_b64decode, standard_b64encode
from binascii import hexlify
from collections import defaultdict
from functools import lru_cache

from PyQt5.Qt import (
    QWebEngineProfile, QApplication, QWebEngineScript, QFile, QIODevice,
    QKeySequence, QByteArray
)

from .constants import config_dir, appname, cache_dir, str_version, DOWNLOADS_URL
from .resources import get_data_as_file


def to_json(obj):
    if isinstance(obj, bytearray):
        return {'__class__': 'bytearray',
                '__value__': standard_b64encode(bytes(obj)).decode('ascii')}
    raise TypeError(repr(obj) + ' is not JSON serializable')


def from_json(obj):
    cls = obj.get('__class__')
    if cls == 'bytearray':
        return bytearray(standard_b64decode(obj['__value__']))
    return obj

nodef = object()


class DynamicPrefs:

    def __init__(self, name):
        self.path = os.path.join(config_dir, '%s.sqlite' % name)
        self._conn = None
        self._cache = {}
        self.defaults = defaultdict(lambda: nodef)
        self.pending_commits = {}
        self._buffer_commits = False

    @property
    def conn(self):
        if self._conn is None:
            self._conn = apsw.Connection(self.path)
            c = self._conn.cursor()
            uv = next(c.execute('PRAGMA user_version'))[0]
            if uv == 0:
                c.execute('CREATE TABLE prefs (id INTEGER PRIMARY KEY, name TEXT NOT NULL, value TEXT NOT NULL, UNIQUE(name)); PRAGMA user_version=1;')
            c.close()
        return self._conn

    def get(self, name, default=None):
        ans = self[name]
        return default if ans is nodef else ans

    def set(self, name, val):
        self[name] = val

    def __getitem__(self, name):
        try:
            return self._cache[name]
        except KeyError:
            try:
                val = next(self.conn.cursor().execute('SELECT value FROM prefs WHERE name=?', (name,)))[0]
                val = json.loads(val, object_hook=from_json)
            except StopIteration:
                val = self.defaults[name]
            self._cache[name] = val
            return val

    def __setitem__(self, name, val):
        if self._buffer_commits:
            self.pending_commits[name] = val
            return
        self._cache.pop(name, None)
        c = self.conn.cursor()
        if val == self.defaults[name]:
            c.execute('DELETE FROM prefs WHERE name=?', (name,))
        else:
            self._cache[name] = val
            val = json.dumps(val, ensure_ascii=False, indent=2, default=to_json)
            c.execute('INSERT or REPLACE INTO prefs(name, value) VALUES (?, ?)', (name, val))

    def __delitem__(self, name):
        self._cache.pop(name, None)
        c = self.conn.cursor()
        c.execute('DELETE FROM prefs WHERE name=?', (name,))

    @property
    def buffer_commits(self):
        return self._buffer_commits

    @buffer_commits.setter
    def buffer_commits(self, val):
        if val:
            self._buffer_commits = True
        else:
            self._buffer_commits = False
            with self.conn:
                for k, v in self.pending_commits.items():
                    self[k] = v

    def __enter__(self):
        self.buffer_commits = True
        return self

    def __exit__(self, *args):
        self.buffer_commits = False

gprefs = DynamicPrefs('gui-dynamic')
qwebchannel_js = QFile(':/qtwebchannel/qwebchannel.js')
if not qwebchannel_js.open(QIODevice.ReadOnly):
    raise SystemExit('Failed to load qwebchannel.js with error: %s' % qwebchannel_js.errorString())
qwebchannel_js = bytes(qwebchannel_js.readAll()).decode('utf-8')
# qwebchannel_js = open('/usr/src/qt5/qtwebchannel/src/webchannel/qwebchannel.js').read()


def safe_makedirs(path):
    try:
        os.makedirs(path)
    except FileExistsError:
        pass


def create_script(name, src, world=QWebEngineScript.ApplicationWorld, injection_point=QWebEngineScript.DocumentCreation, on_subframes=True):
    script = QWebEngineScript()
    script.setSourceCode(src)
    script.setName(name)
    script.setWorldId(world)
    script.setInjectionPoint(injection_point)
    script.setRunsOnSubFrames(on_subframes)
    return script


AUTH_TOKEN = None


@lru_cache()
def client_script():
    global AUTH_TOKEN
    AUTH_TOKEN = hexlify(os.urandom(32)).decode('ascii')
    name = '%s-client.js' % appname
    f = get_data_as_file(name)
    src = f.read().decode('utf-8')
    src = src.replace('__DOWNLOADS_URL__', DOWNLOADS_URL)
    src = src.replace('__WEBSOCKET_PORT__', str(QApplication.instance().web_socket_server.port))
    src = src.replace('__AUTH_TOKEN__', AUTH_TOKEN)
    src = src.replace('__SECRET_KEY__', hexlify(os.urandom(32)).decode('ascii'))
    return create_script(f.name, src)


@lru_cache()
def qwebchannel_script():
    return create_script('qwebchannel.js', qwebchannel_js)


def insert_scripts(profile, *scripts):
    sc = profile.scripts()
    for script in scripts:
        for existing in sc.findScripts(script.name()):
            sc.remove(existing)
    for script in scripts:
        sc.insert(script)


def create_profile(parent=None, private=False):
    from .vise_scheme import UrlSchemeHandler
    if parent is None:
        parent = QApplication.instance()
    if private:
        from .downloads import download_requested
        ans = QWebEngineProfile(parent)
        ans.downloadRequested.connect(download_requested)
    else:
        ans = QWebEngineProfile(appname, parent)
        ans.setCachePath(os.path.join(cache_dir, appname, 'cache'))
        safe_makedirs(ans.cachePath())
        ans.setPersistentStoragePath(os.path.join(cache_dir, appname, 'storage'))
        safe_makedirs(ans.persistentStoragePath())
    ans.setHttpUserAgent(ans.httpUserAgent().replace('QtWebEngine/', '%s/%s QtWebEngine/' % (appname, str_version)))
    try:
        insert_scripts(ans, qwebchannel_script(), client_script())
    except FileNotFoundError as err:
        if '-client.js' in str(err):
            raise SystemExit('You need to compile the rapydscript parts of vise before running it. Install rapydscript-ng and run the build script')
        raise
    ans.url_handler = UrlSchemeHandler(ans)
    ans.installUrlSchemeHandler(QByteArray(b'vise'), ans.url_handler)
    return ans

_profile = None


def profile():
    global _profile
    if _profile is None:
        from .downloads import download_requested
        _profile = create_profile()
        _profile.downloadRequested.connect(download_requested)
    return _profile


def delete_profile():
    from .utils import safe_disconnect
    global _profile
    if _profile is not None:
        safe_disconnect(_profile.downloadRequested)
        _profile.deleteLater()
    _profile = None

_quickmarks = None


def quickmarks():
    global _quickmarks
    if _quickmarks is None:
        from .utils import parse_url
        _quickmarks = {}
        try:
            with open(os.path.join(config_dir, 'quickmarks'), 'rb') as f:
                for line in f.read().decode('utf-8').splitlines():
                    line = line.strip()
                    if line and not line.startswith('#'):
                        key, url = line.partition(' ')[::2]
                        key = QKeySequence.fromString(key)[0]
                        url = parse_url(url)
                        _quickmarks[key] = url
        except FileNotFoundError:
            pass
    return _quickmarks
