#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2015, Kovid Goyal <kovid at kovidgoyal.net>

from functools import partial
from gettext import gettext as _

from PyQt5.Qt import (
    QApplication, QKeyEvent, QEvent, Qt, QUrl
)

from .communicate import python_to_js


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


def close_other_tabs(window, *args, **kwargs):
    if window.current_tab is not None:
        window.tab_tree.close_other_tabs(window.current_tab)
        return True


def exit_full_screen(window, *args, **kw):
    if window.isFullScreen():
        window.toggle_full_screen(False)
        return True


def toggle_full_screen(window, *args, **kw):
    window.toggle_full_screen(not window.isFullScreen())


def exit_text_input(window, *args, **kwargs):
    if window.current_tab is not None:
        window.current_tab.exit_text_input()
        return True


def edit_text(window, *args, **kwargs):
    if window.current_tab is not None:
        python_to_js(window.current_tab, 'get_editable_text')
        return True


def _paste_url(text):
    text = text or ''
    text = text.partition(' ')[2].strip()
    w = QApplication.instance().activeWindow()
    w.setFocus(Qt.MouseFocusReason)  # For some reason calling setFocus directly on the tab does not work
    t = getattr(w, 'current_tab', None)
    if t is not None:
        python_to_js(t, 'insert_text', text)


def paste_url(window, *a, **k):
    if window.current_tab is not None:
        window.ask('copyurl ', _paste_url)
        return True


def fill_login_form(window, *args, **kwargs):
    if window.current_tab is not None:
        python_to_js(window.current_tab, 'get_url_for_current_login_form')
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
    return True


def copy_url(window, *args, **kwargs):
    if window.current_tab is not None:
        qurl = window.current_tab.url()
        if not qurl.isEmpty():
            QApplication.clipboard().setText(qurl.toString())
            window.show_status_message(_('Copied: ') + qurl.toString(), 2, 'success')
        window.statusBar()
        return True


def increase_zoom(window, *args, **kw):
    if window.current_tab is not None:
        window.current_tab.zoom_factor += 0.25
        return True


def decrease_zoom(window, *args, **kw):
    if window.current_tab is not None:
        window.current_tab.zoom_factor -= 0.25
        return True


def reset_zoom(window, *args, **kw):
    if window.current_tab is not None:
        window.current_tab.zoom_factor = 1.0
        return True


def _paste_and_go(window, in_current_tab=True):
    c = QApplication.clipboard()
    for mode in c.Clipboard, c.Selection:
        text = c.text(mode).strip()
        if text:
            if text.partition(':')[0].lower() in {'file', 'http', 'https', 'about', 'chrome'}:
                qurl = QUrl.fromUserInput(text)
                if qurl.isValid() and not qurl.isEmpty():
                    window.open_url(qurl, in_current_tab=in_current_tab)
                    return
    window.show_status_message(_('No URL in clipboard'), 2, 'success')


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


def scroll_page(up, window, focus_widget, key_filter, *args, **kwargs):
    if focus_widget is not None:
        with key_filter.disable_filtering:
            key = Qt.Key_PageUp if up else Qt.Key_PageDown
            QApplication.sendEvent(focus_widget, QKeyEvent(QEvent.KeyPress, key, Qt.KeyboardModifiers(0)))
    return True


def scroll_to_boundary(top, window, focus_widget, key_filter, *args, **kwargs):
    if focus_widget is not None:
        with key_filter.disable_filtering:
            key = Qt.Key_Home if top else Qt.Key_End
            QApplication.sendEvent(focus_widget, QKeyEvent(QEvent.KeyPress, key, Qt.KeyboardModifiers(0)))
    return True


scroll_line_down = partial(scroll_line, Qt.Key_Down)
scroll_line_up = partial(scroll_line, Qt.Key_Up)
scroll_line_left = partial(scroll_line, Qt.Key_Left)
scroll_line_right = partial(scroll_line, Qt.Key_Right)
scroll_page_up = partial(scroll_page, True)
scroll_page_down = partial(scroll_page, False)
scroll_to_top = partial(scroll_to_boundary, True)
scroll_to_bottom = partial(scroll_to_boundary, False)


def passthrough(*args, **kwargs):
    return False


def ask(window, *args, **kwargs):
    window.ask()
    return True


def ask_open(window, *args, **kwargs):
    window.ask('open ')
    return True


def open_modified_url(window, *args, **kw):
    if window.current_tab is not None:
        qurl = window.current_tab.url()
        if not qurl.isEmpty():
            window.ask('open ' + qurl.toString())
            return True


def ask_tabopen(window, *args, **kwargs):
    window.ask('tabopen ')
    return True


def tabopen_modified_url(window, *args, **kw):
    if window.current_tab is not None:
        qurl = window.current_tab.url()
        if not qurl.isEmpty():
            window.ask('tabopen ' + qurl.toString())
            return True


def next_tab(window, *args, **kwargs):
    window.tab_tree.next_tab()
    return True


def prev_tab(window, *args, **kwargs):
    window.tab_tree.next_tab(forward=False)
    return True


def undo_close_tab(window, *a, **k):
    if window.undelete_tab():
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


def restart(window, *a, **k):
    QApplication.instance().restart_app()
    return True


def quit(window, *a, **k):
    QApplication.instance().shutdown()
    return True


def choose_tab(window, *args, **kwargs):
    window.choose_tab_pending = True
    window.tab_tree.mark_tabs()
    return True


def follow_link(window, *args, **kwargs):
    window.start_follow_link('sametab')
    return True


def follow_link_newtab(window, *args, **kwargs):
    window.start_follow_link('newtab')
    return True


def copy_link(window, *a, **k):
    window.start_follow_link('copy')
    return True


def follow_next(window, *args, **kw):
    if window.current_tab is not None:
        python_to_js(window.current_tab, 'follow_next', True)
        return True


def follow_previous(window, *args, **kw):
    if window.current_tab is not None:
        python_to_js(window.current_tab, 'follow_next', False)
        return True
