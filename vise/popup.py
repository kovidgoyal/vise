#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2015, Kovid Goyal <kovid at kovidgoyal.net>

from collections import namedtuple

from PyQt5.Qt import (
    QWidget, Qt, QLabel, QDialogButtonBox, QHBoxLayout, QPainter, QPainterPath,
    QRectF, QColor
)

Question = namedtuple('Question', 'id text callback extra_buttons')


class Popup(QWidget):

    def __init__(self, parent):
        QWidget.__init__(self, parent)
        parent.resized.connect(self.parent_resized, type=Qt.QueuedConnection)
        self.questions = []
        self.move(0, 1)
        self.hide()
        self.l = l = QHBoxLayout(self)
        l.setStretch(0, 100)
        self.msg = msg = QLabel('\xa0')
        self.bb = bb = QDialogButtonBox(QDialogButtonBox.Close, self)
        l.addWidget(msg), l.addWidget(bb)
        bb.accepted.connect(self.accept)
        bb.rejected.connect(self.reject)
        self.question_id = 0
        self.shutting_down = False
        self.setFocusPolicy(Qt.NoFocus)
        bb.setFocusPolicy(Qt.NoFocus)
        self.msg.setFocusPolicy(Qt.NoFocus)

    def accept(self):
        self.finish(True)

    def reject(self):
        self.finish(False)

    def parent_resized(self):
        self.resize(self.parent().width(), self.sizeHint().height())

    def ask(self, text, callback=None, extra_buttons=None):
        self.question_id += 1
        self.questions.append(Question(self.question_id, text, callback, extra_buttons or {}))
        self.show_question()
        return self.question_id
    __call__ = ask

    def abort_question(self, question_id):
        if self.isVisible() and self.questions and self.questions[0].id == question_id:
            self.questions.pop(0)
            self.hide()
            return
        for i, question in enumerate(self.questions):
            if question.id == question_id:
                break
        else:
            return
        del self.questions[i]

    def show_question(self):
        if not self.questions:
            return
        q = self.questions[0]
        self.msg.setText(q.text or '')
        self.bb.clear()
        if q.callback is None:
            self.bb.setStandardButtons(self.bb.Close)
        else:
            self.bb.setStandardButtons(self.bb.Yes | self.bb.No)
        for text, val in q.extra_buttons.items():
            b = self.bb.addButton(text, self.bb.AcceptRole)
            b.clicked.connect(self.extra_button_clicked)
            b.setObjectName(val)
        self.show()

    def extra_button_clicked(self):
        button = self.sender()
        q = self.questions[0]
        if q.callback is not None:
            q.callback(button.objectName())

    def show(self):
        self.move(0, 1)
        self.parent_resized()
        QWidget.show(self)
        self.raise_()

    def break_cycles(self):
        while self.questions:
            self.finish(False)

    def finish(self, accepted):
        if self.questions:
            q = self.questions.pop(0)
            if q.callback is not None:
                q.callback(accepted, self.shutting_down)
        if self.questions:
            self.show_question()
        else:
            self.hide()

    def paintEvent(self, ev):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        try:
            self.paint_background(painter)
        except Exception:
            pass
        finally:
            painter.end()
        QWidget.paintEvent(self, ev)

    def paint_background(self, painter):
        br = 12  # border_radius
        bw = 1  # border_width
        c = QColor('#fdfd96')
        p = QPainterPath()
        p.addRoundedRect(QRectF(self.rect()), br, br)
        painter.fillPath(p, c)
        p.addRoundedRect(QRectF(self.rect()).adjusted(bw, bw, -bw, -bw), br, br)
        painter.fillPath(p, QColor('black'))
