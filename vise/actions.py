#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2015, Kovid Goyal <kovid at kovidgoyal.net>


def forward(window, *args, **kwargs):
    if window.current_tab is not None:
        window.current_tab.forward()
        return True


def back(window, *args, **kwargs):
    if window.current_tab is not None:
        window.current_tab.back()
        return True


def close_tab(window, *args, **kwargs):
    if window.current_tab is not None:
        window.close_tab(window.current_tab)
        return True


def search_forward(window, *args, **kwargs):
    pass


def search_back(window, *args, **kwargs):
    pass


def next_match(window, *args, **kwargs):
    pass


def prev_match(window, *args, **kwargs):
    pass
