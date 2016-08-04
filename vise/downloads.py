#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2015, Kovid Goyal <kovid at kovidgoyal.net>

import os
import tempfile
import mimetypes
import weakref
from time import monotonic
from functools import partial, lru_cache
from itertools import count
from gettext import gettext as _

import sip
from PyQt5.Qt import (
    QApplication, QObject, QUrl, QByteArray,
    QWebEngineDownloadItem, pyqtSignal, QTimer, Qt, QWidget, QPainter
)

from .config import misc_config
from .constants import DOWNLOADS_URL as DU, STATUS_BAR_HEIGHT
from .resources import get_data, get_icon
from .utils import safe_disconnect, get_content_type_icon, open_local_file, draw_snake_spinner


def get_download_dir():
    if not hasattr(get_download_dir, 'ans'):
        get_download_dir.ans = os.path.expanduser(misc_config('download_dir', default='~/downloads'))
        try:
            os.makedirs(get_download_dir.ans)
        except FileExistsError:
            pass
    return get_download_dir.ans

DOWNLOADS_URL = QUrl(DU)


def downloads_icon():
    if not hasattr(downloads_icon, 'icon'):
        downloads_icon.icon = get_icon('download.svg')
    return downloads_icon.icon


@lru_cache(maxsize=50)
def mimetype_icon_data(mime_type):
    raw = get_content_type_icon(mime_type, as_data=True) or get_data('images/blank.png')
    return QByteArray(raw)


class Indicator(QWidget):  # {{{

    downloads_tooltip = _(
        'Click to see ongoing downloads')
    no_downloads_tooltip = _(
        'No active downloads\nClick to see downloads')

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setCursor(Qt.PointingHandCursor)
        self.setToolTip(self.no_downloads_tooltip)
        self.timer = tt = QTimer(self)
        tt.setInterval(10)
        tt.timeout.connect(self.tick)
        self.angle = 0
        pal = (parent or QApplication.instance()).palette()
        self.dark = pal.color(pal.Text)
        self.light = pal.color(pal.Base)
        self.errored_out = False
        self.update()
        self.setMinimumWidth(STATUS_BAR_HEIGHT - 4)
        self.setMinimumHeight(STATUS_BAR_HEIGHT - 4)

    def tick(self):
        self.angle -= 4
        self.update()

    def start(self):
        self.timer.start()
        self.setToolTip(self.downloads_tooltip)
        self.update()

    def stop(self):
        self.timer.stop()
        self.setToolTip(self.no_downloads_tooltip)
        self.update()

    def paintEvent(self, ev):
        if self.timer.isActive():
            if not self.errored_out:
                try:
                    draw_snake_spinner(QPainter(self), self.rect(), self.angle, self.light, self.dark)
                except Exception:
                    import traceback
                    traceback.print_exc()
                    self.errored_out = True
        else:
            r = self.rect()
            painter = QPainter(self)
            painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
            icon = downloads_icon()
            pmap = icon.pixmap(r.width(), r.height())
            x = (r.width() - pmap.width()) // 2
            y = (r.height() - pmap.height()) // 2
            painter.drawPixmap(x, y, pmap)

    def mousePressEvent(self, ev):
        if ev.button() == Qt.LeftButton:
            from .actions import show_downloads
            app = QApplication.instance()
            w = app.activeWindow()
            if hasattr(w, 'get_tab_for_load'):
                show_downloads(w)
# }}}


file_counter = count()


def download_requested(download_item):
    app = QApplication.instance()
    fname = download_item.fname = os.path.basename(download_item.path()) or 'file%d' % next(file_counter)
    download_item.setPath(os.path.join(get_download_dir(), fname))
    download_item.accept()
    app.downloads.download_created(download_item)


class Downloads(QObject):

    INTERVAL = 2
    for_develop = False

    def __init__(self, parent=None):
        QObject.__init__(self, parent)
        self.items = []
        self.tabrefs = []
        self._has_active_downloads = False

    @property
    def has_active_downloads(self):
        return self._has_active_downloads

    @has_active_downloads.setter
    def has_active_downloads(self, val):
        val = bool(val)
        changed = val != self._has_active_downloads
        self._has_active_downloads = val
        if changed:
            app = QApplication.instance()
            for w in app.windows:
                di = w.downloads_indicator
                (di.start if val else di.stop)()

    def itertabs(self):
        remove = []
        for tabref in self.tabrefs:
            tab = tabref()
            if tab is not None:
                if not sip.isdeleted(tab) and tab.url() == DOWNLOADS_URL:
                    yield tab
                else:
                    remove.append(tabref)
            else:
                remove.append(tabref)
        for tabref in remove:
            self.tabrefs.remove(tabref)

    def download_created(self, download_item):
        idx = len(self.items)
        self.items.append(download_item)
        download_item.downloadProgress.connect(partial(self.on_state_change, idx))
        download_item.finished.connect(partial(self.on_state_change, idx))
        download_item.stateChanged.connect(partial(self.on_state_change, idx))
        download_item.last_tick = (monotonic(), 0)
        download_item.rates = [-1]
        for tab in self.itertabs():
            self.create_item(tab, download_item)
        self.has_active_downloads = True
        w = QApplication.instance().activeWindow()
        if hasattr(w, 'show_status_message'):
            w.show_status_message(_('Download of %s started!') % os.path.basename(download_item.path()), 2)

    def on_state_change(self, idx):
        item = self.items[idx]
        state = item.state()
        now = monotonic()
        if now - item.last_tick[0] >= self.INTERVAL:
            item.rates.append((item.receivedBytes() - item.last_tick[1]) / (now - item.last_tick[0]))
            item.last_tick = (now, item.receivedBytes())
        if state not in (QWebEngineDownloadItem.DownloadRequested, QWebEngineDownloadItem.DownloadInProgress):
            self.on_download_finish(item)
        for tab in self.itertabs():
            self.update_item(tab, item)
        for item in self.items:
            if not item.isFinished():
                self.has_active_downloads = True
                return
        self.has_active_downloads = False

    def on_download_finish(self, item):
        item.rates = [0]
        w = QApplication.instance().activeWindow()
        if hasattr(w, 'show_status_message'):
            w.show_status_message(_('Download of %s completed!') % os.path.basename(item.path()), 5, 'success')

    def break_cycles(self):
        for item in self.items:
            safe_disconnect(item.stateChanged)
            safe_disconnect(item.downloadProgress)
        del self.items

    def add_tab(self, newtab):
        for i, ref in enumerate(tuple(self.tabrefs)):
            tab = ref()
            if tab is None:
                del self.tabrefs[i]
            else:
                if newtab is tab:
                    return
        self.tabrefs.append(weakref.ref(newtab))
        for item in self.items:
            self.create_item(newtab, item)
            self.update_item(newtab, item)
        if self.for_develop:
            if newtab.url() == DOWNLOADS_URL:
                self.for_develop()
                self.for_develop = False
            else:
                newtab.urlChanged.connect(self.for_develop)

    def create_item(self, tab, download_item):
        tab.js_func('window.create_download',
                    download_item.id(), download_item.fname, download_item.mimeType(),
                    'vise:mimetype-icon/' + (download_item.mimeType() or 'application/octet-stream'),
                    download_item.url().host() or 'localhost')

    def update_item(self, tab, download_item):
        state = {QWebEngineDownloadItem.DownloadCancelled: 'canceled', QWebEngineDownloadItem.DownloadCompleted: 'completed',
                 QWebEngineDownloadItem.DownloadInterrupted: 'interrupted'}.get(download_item.state(), 'running')
        rates = download_item.rates
        if len(rates) == 1:
            rate = rates[0]
        else:
            rate = sum(rates[-100:]) / 100
        tab.js_func('window.update_download',
                    download_item.id(), state, download_item.receivedBytes(), download_item.totalBytes(), rates[-1], rate)

    def callback(self, tab, data):
        cmd = data.get('cmd')
        if cmd == 'inited':
            self.add_tab(tab)
            return
        dlid = data.get('id')
        for item in self.items:
            if item.id() == dlid:
                if cmd == 'cancel':
                    item.cancel()
                elif cmd == 'open':
                    open_local_file(item.path())
                break


def get_downloads_html():
    if not hasattr(get_downloads_html, 'html'):
        get_downloads_html.html = QByteArray(get_data('downloads.html').decode('utf-8').replace('_TITLE_', _('Downloads')).encode('utf-8'))
    return get_downloads_html.html


def develop():  # {{{
    from .main import run_app

    class FakeDownloadItem(QObject):

        idc = 0
        downloadProgress = pyqtSignal(object, object)
        stateChanged = pyqtSignal(object)
        finished = pyqtSignal()

        def __init__(self, size=10 * 1024 * 1024):
            QObject.__init__(self)
            self._state = QWebEngineDownloadItem.DownloadRequested
            self._received = self._total = -1
            FakeDownloadItem.idc += 1
            self._id = FakeDownloadItem.idc
            self._size = size
            self.fname = '%s.epub' % self.id()
            self.mimeType = lambda: mimetypes.guess_type(self.fname)[0]
            QTimer.singleShot(100, self._tick)

        def id(self):
            return self._id

        def isFinished(self):
            return self._state not in (QWebEngineDownloadItem.DownloadInProgress, QWebEngineDownloadItem.DownloadRequested)

        def path(self):
            return os.path.join(tempfile.gettempdir(), self.fname)

        def state(self):
            return self._state

        def receivedBytes(self):
            return self._received

        def totalBytes(self):
            return self._total

        def url(self):
            return QUrl('http://example.com/%s' % self.fname)

        def _tick(self):
            if self._state not in (QWebEngineDownloadItem.DownloadInProgress, QWebEngineDownloadItem.DownloadRequested):
                return
            if self._total == -1:
                self._total = self._size
                self._received = 0
                self._state = QWebEngineDownloadItem.DownloadInProgress
                self.stateChanged.emit(self._state)
                self.downloadProgress.emit(self._received, self._total)
                QTimer.singleShot(100, self._tick)
            elif self._received < self._total:
                self._received += min(self._total - self._received, self._size // 100)
                self.downloadProgress.emit(self._received, self._total)
                if self._received >= self._total:
                    self._state = QWebEngineDownloadItem.DownloadCompleted
                    self.stateChanged.emit(self._state)
                    self.finished.emit()
                else:
                    QTimer.singleShot(100, self._tick)

        def cancel(self):
            self._state = QWebEngineDownloadItem.DownloadCancelled
            self.stateChanged.emit(self._state)

    def create_downloads(*args):
        di = FakeDownloadItem()
        app = QApplication.instance()
        app.downloads.download_created(di)
        app.downloads.download_created(FakeDownloadItem(size=100 * 1024))

    Downloads.for_develop = create_downloads
    run_app([DU], new_instance=True)
# }}}
