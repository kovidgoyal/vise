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


def exit_full_screen(window, *args, **kw):
    if window.isFullScreen():
        window.toggle_full_screen(False)
        return True


def toggle_full_screen(window, *args, **kw):
    window.toggle_full_screen(not window.isFullScreen())


def exit_text_input(window, *args, **kwargs):
    if window.current_tab is not None:
        window.current_tab.page().runJavaScript('document.activeElement.blur()')
        return True


def edit_text(window, *args, **kwargs):
    if window.current_tab is not None:
        window.current_tab.page().bridge.get_editable_text.emit()
        return True


def fill_login_form(window, *args, **kwargs):
    if window.current_tab is not None:
        window.current_tab.page().bridge.get_url_for_current_login_form.emit()
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
    return True


def search_back(window, *args, **kwargs):
    window.start_search(forward=False)
    return True


def next_match(window, *args, **kwargs):
    window.do_search()
    return True


def prev_match(window, *args, **kwargs):
    window.do_search(forward=False)
    return True


def clear_search_highlighting(window, *args, **kwargs):
    if window.current_tab is not None:
        window.do_search('')
    return True


def show_downloads(window, *args, **kwargs):
    from .downloads import DOWNLOADS_URL
    tab = window.get_tab_for_load(in_current_tab=False)
    tab.load(DOWNLOADS_URL)
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
    return True


def paste_and_go_newtab(window, *args, **kwargs):
    _paste_and_go(window, in_current_tab=False)
    return True


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
    return False


def ask(window, *args, **kwargs):
    window.ask()
    return True


def ask_open(window, *args, **kwargs):
    window.ask('open ')
    return True


def ask_tabopen(window, *args, **kwargs):
    window.ask('tabopen ')
    return True


def next_tab(window, *args, **kwargs):
    window.tab_tree.next_tab()
    return True


def prev_tab(window, *args, **kwargs):
    window.tab_tree.next_tab(forward=False)
    return True


def reload(window, *args, **kwargs):
    if window.current_tab is not None:
        p = window.current_tab.page()
        p.triggerAction(p.Reload)
        return True


def hard_reload(window, *args, **kwargs):
    if window.current_tab is not None:
        p = window.current_tab.page()
        p.triggerAction(p.ReloadAndBypassCache)
        return True


def choose_tab(window, *args, **kwargs):
    window.choose_tab_pending = True
    window.tab_tree.mark_tabs()
    return True


def follow_next(window, *args, **kw):
    window.follow_next()
    return True


def follow_previous(window, *args, **kw):
    window.follow_next(forward=False)
    return True
