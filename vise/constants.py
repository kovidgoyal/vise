#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2015, Kovid Goyal <kovid at kovidgoyal.net>

import sys
import os
import socket

from PyQt5.Qt import QStandardPaths

appname = 'vise'
numeric_version = (0, 1, 0)
version = str_version = '.'.join(map(str, numeric_version))

_plat = sys.platform.lower()
iswindows = 'win32' in _plat or 'win64' in _plat
isosx = 'darwin' in _plat
isnewosx = isosx and getattr(sys, 'new_app_bundle', False)
isfreebsd = 'freebsd' in _plat
isnetbsd = 'netbsd' in _plat
isdragonflybsd = 'dragonfly' in _plat
isbsd = isfreebsd or isnetbsd or isdragonflybsd
islinux = not(iswindows or isosx or isbsd)
DOWNLOADS_URL = 'vise:downloads'
hostname = socket.gethostname()


def _get_cache_dir():
    if 'VISE_CACHE_DIRECTORY' in os.environ:
        return os.path.abspath(os.path.expanduser(os.environ['VISE_CACHE_DIRECTORY']))

    candidate = QStandardPaths.writableLocation(QStandardPaths.CacheLocation)
    if not candidate and not iswindows and not isosx:
        candidate = os.path.expanduser(os.environ.get('XDG_CACHE_HOME', u'~/.cache'))
    if not candidate:
        raise RuntimeError(
            'Failed to find path for application cache directory')
    ans = os.path.join(candidate, appname)
    try:
        os.makedirs(ans)
    except FileExistsError:
        pass
    return ans
cache_dir = _get_cache_dir()
del _get_cache_dir


def _get_config_dir():
    if 'VISE_CONFIG_DIRECTORY' in os.environ:
        return os.path.abspath(os.path.expanduser(os.environ['VISE_CONFIG_DIRECTORY']))

    candidate = QStandardPaths.writableLocation(QStandardPaths.ConfigLocation)
    if not candidate:
        if isosx:
            candidate = os.path.expanduser('~/Library/Preferences')
        elif not iswindows:
            candidate = os.path.expanduser(os.environ.get('XDG_CONFIG_HOME', u'~/.config'))
    if not candidate:
        raise RuntimeError(
            'Failed to find path for application config directory')
    ans = os.path.join(candidate, appname)
    try:
        os.makedirs(ans)
    except FileExistsError:
        pass
    return ans
config_dir = _get_config_dir()
del _get_config_dir
