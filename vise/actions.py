#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2015, Kovid Goyal <kovid at kovidgoyal.net>

from functools import partial
from gettext import gettext as _

from PyQt5.Qt import (
    QApplication, QKeyEvent, QEvent, Qt, QUrl
)


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


def set_passthrough_mode(window, *args, **kwargs):
    if window.current_tab is not None:
        window.current_tab.force_passthrough = True
        return True


def quickmark(window, *args, **kwargs):
    window.quickmark_pending = 'sametab'
    return True


def quickmark_newtab(window, *args, **kwargs):
    window.quickmark_pending = 'newtab'
    return True


def search_forward(window, *args, **kwargs):
    window.start_search(forward=True)


def search_back(window, *args, **kwargs):
    window.start_search(forward=False)


def next_match(window, *args, **kwargs):
    window.do_search()


def prev_match(window, *args, **kwargs):
    window.do_search(forward=False)


def show_downloads(window, *args, **kwargs):
    tab = window.get_tab_for_load(in_current_tab=False)
    from .downloads import load
    load(tab)
    window.show_tab(tab)


def copy_url(window, *args, **kwargs):
    if window.current_tab is not None:
        qurl = window.current_tab.url()
        if not qurl.isEmpty():
            QApplication.clipboard().setText(qurl.toString())
            window.statusBar().showMessage(_('Copied: ') + qurl.toString(), 2000)
        window.statusBar()


def _paste_and_go(window, in_current_tab=True):
    c = QApplication.clipboard()
    for mode in c.Clipboard, c.Selection:
        text = c.text(mode).strip()
        if text:
            if text.partition(':')[0].lower() in {'file', 'http', 'https', 'about'}:
                qurl = QUrl.fromUserInput(text)
                if qurl.isValid() and not qurl.isEmpty():
                    window.open_url(qurl, in_current_tab=in_current_tab)
                    return
    window.statusBar().showMessage(_('No URL in clipboard'))


def paste_and_go(window, *args, **kwargs):
    _paste_and_go(window)


def paste_and_go_newtab(window, *args, **kwargs):
    _paste_and_go(window, in_current_tab=False)


def scroll_line(key, window, focus_widget, key_filter, *args, **kwargs):
    if focus_widget is not None:
        with key_filter.disable_filtering:
            QApplication.sendEvent(focus_widget, QKeyEvent(QEvent.KeyPress, key, Qt.KeyboardModifiers(0)))
    return True

scroll_line_down = partial(scroll_line, Qt.Key_Down)
scroll_line_up = partial(scroll_line, Qt.Key_Up)
scroll_line_left = partial(scroll_line, Qt.Key_Left)
scroll_line_right = partial(scroll_line, Qt.Key_Right)


def passthrough(*args, **kwargs):
    pass
