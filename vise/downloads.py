#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2015, Kovid Goyal <kovid at kovidgoyal.net>

import mimetypes
import os
import tempfile
import weakref
from binascii import hexlify, unhexlify
from functools import lru_cache
from gettext import gettext as _
from itertools import count
from time import monotonic
from urllib.parse import unquote

from PyQt6 import sip
from PyQt6.QtCore import QByteArray, QObject, Qt, QTimer, QUrl, pyqtSignal
from PyQt6.QtGui import QPainter, QPalette
from PyQt6.QtWebEngineCore import QWebEngineDownloadRequest
from PyQt6.QtWidgets import QApplication, QWidget

from .config import misc_config
from .constants import DOWNLOADS_URL as DU
from .constants import STATUS_BAR_HEIGHT
from .resources import get_data, get_icon
from .utils import icon_data_for_filename, open_local_file, safe_disconnect


def get_download_dir():
    if not hasattr(get_download_dir, 'ans'):
        get_download_dir.ans = os.path.expanduser(misc_config('download_dir', default='~/downloads'))
        try:
            os.makedirs(get_download_dir.ans)
        except FileExistsError:
            pass
    return get_download_dir.ans


DOWNLOADS_URL = QUrl(DU)
DOWNLOAD_ICON_NAME = 'download.svg'
save_page_path_map = {}


@lru_cache(maxsize=150)
def filename_icon_data(encoded_file_name):
    return QByteArray(icon_data_for_filename(unhexlify(encoded_file_name).decode('utf-8'), size=64) or get_data('images/blank.png'))


class Indicator(QWidget):  # {{{

    downloads_tooltip = _(
        'Click to see ongoing downloads')
    no_downloads_tooltip = _(
        'No active downloads\nClick to see downloads')

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setToolTip(self.no_downloads_tooltip)
        pal = (parent or QApplication.instance()).palette()
        self.dark = pal.color(QPalette.ColorRole.Text)
        self.light = pal.color(QPalette.ColorRole.Base)
        self.update()
        self.setMinimumWidth(STATUS_BAR_HEIGHT - 4)
        self.setMinimumHeight(STATUS_BAR_HEIGHT - 4)
        self.running = False

    def start(self):
        self.running = True
        self.setToolTip(self.downloads_tooltip)
        self.update()

    def stop(self):
        self.running = False
        self.setToolTip(self.no_downloads_tooltip)
        self.update()

    def paintEvent(self, ev):
        r = self.rect()
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)
        icon = get_icon('busy.svg' if self.running else DOWNLOAD_ICON_NAME)
        pmap = icon.pixmap(r.width(), r.height())
        x = (r.width() - int(pmap.width() / pmap.devicePixelRatio())) // 2
        y = (r.height() - int(pmap.height() / pmap.devicePixelRatio())) // 2 + 1
        painter.drawPixmap(x, y, pmap)

    def mousePressEvent(self, ev):
        if ev.button() == Qt.MouseButton.LeftButton:
            from .actions import show_downloads
            app = QApplication.instance()
            w = app.activeWindow()
            if hasattr(w, 'get_tab_for_load'):
                show_downloads(w)
# }}}


file_counter = count()


def download_requested(download_item):
    app = QApplication.instance()
    if download_item.savePageFormat() == download_item.UnknownSaveFormat:
        fname = download_item.fname = unquote(os.path.basename(download_item.path())) or 'file%d' % next(file_counter)
        download_item.setPath(os.path.join(get_download_dir(), fname))
    else:
        fmt = misc_config('save_format', default='files')
        download_item.setSavePageFormat(download_item.MimeHtmlSaveFormat if fmt == 'mhtml' else download_item.CompleteHtmlSaveFormat)
        path = save_page_path_map.pop(download_item.url().toString(), None)
        if path:
            download_item.setPath(path)
            download_item.fname = os.path.basename(path)
        else:
            fname = download_item.fname = unquote(os.path.basename(download_item.path()))
            if fmt != 'mhtml' and fname.endswith('.mhtml'):
                fname = fname.rpartition('.')[0] + '.html'
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
        self.items.append(download_item)
        download_item.downloadProgress.connect(self.on_state_change)
        download_item.finished.connect(self.on_state_change)
        download_item.stateChanged.connect(self.on_state_change)
        download_item.last_tick = (monotonic(), 0)
        download_item.rates = [-1]
        for tab in self.itertabs():
            self.create_item(tab, download_item)
        self.has_active_downloads = True
        w = QApplication.instance().activeWindow()
        if hasattr(w, 'show_status_message'):
            w.show_status_message(_('Download of %s started!') % os.path.basename(download_item.path()), 2)

    def on_state_change(self):
        item = self.sender()
        state = item.state()
        now = monotonic()
        if now - item.last_tick[0] >= self.INTERVAL:
            item.rates.append((item.receivedBytes() - item.last_tick[1]) / (now - item.last_tick[0]))
            item.last_tick = (now, item.receivedBytes())
        if state not in (QWebEngineDownloadRequest.DownloadState.DownloadRequested, QWebEngineDownloadRequest.DownloadState.DownloadInProgress):
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
                    'vise:filename-icon/' + hexlify((download_item.fname or '').encode('utf-8')).decode('ascii'),
                    download_item.url().host() or 'localhost')

    def update_item(self, tab, download_item):
        state = {QWebEngineDownloadRequest.DownloadState.DownloadCancelled: 'canceled', QWebEngineDownloadRequest.DownloadState.DownloadCompleted: 'completed',
                 QWebEngineDownloadRequest.DownloadState.DownloadInterrupted: 'interrupted'}.get(download_item.state(), 'running')
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
            self._state = QWebEngineDownloadRequest.DownloadState.DownloadRequested
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
            return self._state not in (QWebEngineDownloadRequest.DownloadState.DownloadInProgress, QWebEngineDownloadRequest.DownloadState.DownloadRequested)

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
            if self._state not in (QWebEngineDownloadRequest.DownloadState.DownloadInProgress, QWebEngineDownloadRequest.DownloadState.DownloadRequested):
                return
            if self._total == -1:
                self._total = self._size
                self._received = 0
                self._state = QWebEngineDownloadRequest.DownloadState.DownloadInProgress
                self.stateChanged.emit(self._state)
                self.downloadProgress.emit(self._received, self._total)
                QTimer.singleShot(100, self._tick)
            elif self._received < self._total:
                self._received += min(self._total - self._received, self._size // 100)
                self.downloadProgress.emit(self._received, self._total)
                if self._received >= self._total:
                    self._state = QWebEngineDownloadRequest.DownloadState.DownloadCompleted
                    self.stateChanged.emit(self._state)
                    self.finished.emit()
                else:
                    QTimer.singleShot(100, self._tick)

        def cancel(self):
            self._state = QWebEngineDownloadRequest.DownloadState.DownloadCancelled
            self.stateChanged.emit(self._state)

    def create_downloads(*args):
        di = FakeDownloadItem()
        app = QApplication.instance()
        app.downloads.download_created(di)
        app.downloads.download_created(FakeDownloadItem(size=100 * 1024))

    Downloads.for_develop = create_downloads
    run_app([DU], new_instance=True)
# }}}
