#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2015, Kovid Goyal <kovid at kovidgoyal.net>

import sys
import os
import socket
import string

from PyQt5.Qt import QStandardPaths, Qt

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
WELCOME_URL = 'vise:welcome'
hostname = os.environ.get('VISE_HOSTNAME', socket.gethostname())
STATUS_BAR_HEIGHT = 24
FOLLOW_LINK_KEY_MAP = {getattr(Qt, 'Key_' + x.upper()): x for x in string.ascii_lowercase + string.digits}
FOLLOW_LINK_KEY_MAP[Qt.Key_Escape] = '|escape'
FOLLOW_LINK_KEY_MAP[Qt.Key_Enter] = FOLLOW_LINK_KEY_MAP[Qt.Key_Return] = '|enter'


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


def get_windows_username():
    '''
    Return the user name of the currently logged in user as a unicode string.
    Note that usernames on windows are case insensitive, the case of the value
    returned depends on what the user typed into the login box at login time.
    '''
    import ctypes
    try:
        advapi32 = ctypes.windll.advapi32
        GetUserName = getattr(advapi32, 'GetUserNameW')
    except AttributeError:
        pass
    else:
        buf = ctypes.create_unicode_buffer(257)
        n = ctypes.c_int(257)
        if GetUserName(buf, ctypes.byref(n)):
            return buf.value

    return os.environ.get('USERNAME')


def local_socket_address():
    if getattr(local_socket_address, 'ADDRESS', None) is None:
        if iswindows:
            local_socket_address.ADDRESS = r'\\.\pipe\vise-local-server'
            try:
                user = get_windows_username()
            except Exception:
                user = None
            if user:
                user = user.replace(' ', '_')
                if user:
                    local_socket_address.ADDRESS += '-' + user[:100] + 'x'
        else:
            user = os.environ.get('USER', '')
            if not user:
                user = os.path.basename(os.path.expanduser('~'))
            rdir = QStandardPaths.writableLocation(QStandardPaths.RuntimeLocation) or QStandardPaths.writableLocation(QStandardPaths.TempLocation)
            local_socket_address.ADDRESS = os.path.join(rdir, user + '-vise-local-server')
    return local_socket_address.ADDRESS
