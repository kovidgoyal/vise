#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2016, Kovid Goyal <kovid at kovidgoyal.net>

import os
from functools import lru_cache

from yaml import safe_load

from .constants import config_dir, hostname
from .resources import get_data_as_file


@lru_cache()
def load_config(user=False):
    if user:
        p = os.path.join(config_dir, 'config.yaml')
        try:
            with open(p, 'rb') as f:
                return safe_load(f)
        except FileNotFoundError:
            return {}
    return safe_load(get_data_as_file('config.yaml'))


@lru_cache()
def font_families():
    uff = (load_config(user=True).get('fonts') or {}).get('families') or {}
    dff = load_config(user=False)['fonts']['families']
    families = {}

    def get_ff(x):
        if isinstance(x, dict):
            return x.get(hostname)
        return x

    for ftype, val in uff.items():
        val = get_ff(val)
        if isinstance(val, str):
            families[ftype] = val

    for ftype, val in dff.items():
        if ftype not in families:
            val = get_ff(val)
            if isinstance(val, str):
                families[ftype] = val

    return families


@lru_cache()
def font_sizes():
    uff = (load_config(user=True).get('fonts') or {}).get('sizes') or {}
    dff = load_config(user=False)['fonts']['sizes']
    sizes = {}

    def conv(x):
        if x == 'default':
            return 0
        try:
            return int(x)
        except Exception:
            pass

    def get_ff(x):
        if isinstance(x, dict):
            return conv(x.get(hostname))
        return conv(x)

    for ftype, val in uff.items():
        val = get_ff(val)
        if isinstance(val, int):
            sizes[ftype] = val

    for ftype, val in dff.items():
        if ftype not in sizes:
            val = get_ff(val)
            if isinstance(val, int):
                sizes[ftype] = val

    return sizes
