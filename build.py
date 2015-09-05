#!/usr/bin/env python3
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2015, Kovid Goyal <kovid at kovidgoyal.net>

import os
import subprocess
import sysconfig
import shlex

icu_libs = ['icudata', 'icui18n', 'icuuc', 'icuio']
conf = sysconfig.get_config_vars()
cc = shlex.split(os.environ.get('CC', conf['CC']))
debug = ''
cflags = conf['CFLAGS'] + ' ' + conf['CFLAGSFORSHARED']
cflags = shlex.split(cflags) + ['-fPIC']
ldflags = conf['LDFLAGS']
ldflags = shlex.split(ldflags)
cflags += shlex.split(os.environ.get('CFLAGS', ''))
ldflags += shlex.split(os.environ.get('LDFLAGS', ''))
cflags.append('-pthread')
ldflags.append('-shared')
cflags.append('-I' + sysconfig.get_path('include'))
ldflags.append('-lpython' + conf['LDVERSION'])
ldflags.extend('-l'+x for x in icu_libs)

cmd = cc + ['-I.', 'matcher.c'] + cflags + ['-o', 'matcher_native.so'] + ldflags
print(' '.join(cmd))
subprocess.check_call(cmd, cwd='vise')
