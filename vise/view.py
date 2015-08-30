#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2015, Kovid Goyal <kovid at kovidgoyal.net>

from PyQt5.Qt import (
    QWebEngineView, QWebEnginePage, QSize, QNetworkRequest, QIcon,
    QApplication, QPixmap, pyqtSignal
)

view_id = 0


class WebPage(QWebEnginePage):

    def __init__(self, profile, parent):
        QWebEnginePage.__init__(self, profile, parent)


class WebView(QWebEngineView):

    icon_changed = pyqtSignal(object)

    def __init__(self, profile, parent):
        global view_id
        QWebEngineView.__init__(self, parent)
        self.create_page(profile)
        self.view_id = view_id
        view_id += 1
        self.iconUrlChanged.connect(self.icon_url_changed)
        self._icon_reply = None
        self.icon = QIcon()

    def create_page(self, profile):
        self._page = WebPage(profile, self)
        self.setPage(self._page)

    def sizeHint(self):
        return QSize(800, 600)

    def icon_url_changed(self, qurl):
        if qurl.isEmpty():
            self.icon_loaded()
            return
        req = QNetworkRequest(qurl)
        self._icon_reply = QApplication.instance().network_access_manager.get(req)
        self._icon_reply.setParent(self)
        self._icon_reply.finished.connect(self.icon_loaded)

    def icon_loaded(self):
        self.icon = QIcon()
        if self._icon_reply is not None:
            if self._icon_reply.error() == self._icon_reply.NoError:
                data = self._icon_reply.readAll()
                pixmap = QPixmap()
                pixmap.loadFromData(data)
                self.icon.addPixmap(pixmap)
                self._icon_reply.deleteLater()
                self._icon_reply = None
            else:
                QApplication.instance().error('Failed to download favicon from %s with error: %s' % (
                    self._icon_reply.url().toString(), self._icon_reply.errorString()))
        self.icon_changed.emit(self.icon)
