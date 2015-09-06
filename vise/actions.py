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


def exit_text_input(window, *args, **kwargs):
    if window.current_tab is not None:
        window.current_tab.page().runJavaScript('document.activeElement.blur()')
        return True


def edit_text(window, *args, **kwargs):
    if window.current_tab is not None:
        window.current_tab.page().runJavaScript('window.vise_get_editable_text()')
        return True


def passthrough(window, *args, **kwargs):
    if window.current_tab is not None:
        window.current_tab.force_passthrough = True
        return True


def search_forward(window, *args, **kwargs):
    pass


def search_back(window, *args, **kwargs):
    pass


def next_match(window, *args, **kwargs):
    pass


def prev_match(window, *args, **kwargs):
    pass
