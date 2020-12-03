#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2016, Kovid Goyal <kovid at kovidgoyal.net>

from PyQt5.Qt import QProxyStyle, QStyle, Qt


class Style(QProxyStyle):

    def drawPrimitive(self, element, option, painter, widget):
        # do not draw focus rectangles on line edits that have turned them off
        if element == QStyle.PrimitiveElement.PE_FrameLineEdit and widget and not widget.testAttribute(Qt.WidgetAttribute.WA_MacShowFocusRect):
            return

        QProxyStyle.drawPrimitive(self, element, option, painter, widget)
