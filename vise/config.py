#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2016, Kovid Goyal <kovid at kovidgoyal.net>

import os
from functools import lru_cache

from yaml import safe_load

from .constants import config_dir
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
