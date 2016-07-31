#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2016, Kovid Goyal <kovid at kovidgoyal.net>

import json

from PyQt5.Qt import QWebSocketServer, QHostAddress, QObject, pyqtSignal, Qt


class Connection(QObject):

    handshake_initiated = pyqtSignal(object, object)
    message_received = pyqtSignal(object, object)

    def __init__(self, socket, parent):
        QObject.__init__(self, parent)
        self.socket = socket
        socket.textMessageReceived.connect(self.text_message_received, type=Qt.QueuedConnection)
        socket.disconnected.connect(self.break_cycles, type=Qt.QueuedConnection)

    def text_message_received(self, msg):
        from .settings import AUTH_TOKEN
        try:
            msg = json.loads(msg)
        except Exception:
            print('Un-parseable message received from websocket client')
            return
        if msg.pop('auth_token', None) != AUTH_TOKEN:
            print('Un-authenticated message received from websocket client')
            return
        mtype = msg.pop('type', None)
        data = msg.pop('data', {})
        if mtype == 'handshake':
            self.handshake_initiated.emit(self, data)
        else:
            self.message_received.emit(mtype, data)

    def break_cycles(self):
        if hasattr(self, 'socket'):
            try:
                self.socket.textMessageReceived.disconnect()
            except TypeError:
                pass
            try:
                self.message_received.disconnect()
            except TypeError:
                pass
            try:
                self.handshake_initiated.disconnect()
            except TypeError:
                pass
            self.socket.close()
            del self.socket


class WebSocketServer(QWebSocketServer):

    new_connection = pyqtSignal(object, object)

    def __init__(self, parent=None):
        QWebSocketServer.__init__(self, 'vise', QWebSocketServer.NonSecureMode, parent=None)
        self.acceptError.connect(self.on_accept_error)
        if not self.listen(QHostAddress.LocalHost):
            raise RuntimeError('Failed to start WebSocket Server listening on localhost')
        self.port = self.serverPort()
        self.newConnection.connect(self.on_new_connection)
        self.pending_connections = []

    def on_accept_error(self, err):
        print('Connecting to WebSocket client failed with error code: %d' % err)

    def on_new_connection(self):
        conn = self.nextPendingConnection()
        if conn:
            conn = Connection(conn, self)
            self.pending_connections.append(conn)
            conn.handshake_initiated.connect(self.handshake_initiated)

    def handshake_initiated(self, conn, data):
        try:
            self.pending_connections.remove(conn)
        except ValueError:
            pass
        self.new_connection.emit(conn, data)
