#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2026, Kovid Goyal <kovid at kovidgoyal.net>

# A floating, translucent overlay that displays all tabs in a window organized
# into groups, with a search box to filter them.

from functools import partial
from gettext import gettext as _

from PyQt6.QtCore import QEvent, QPointF, QRect, QRectF, QSize, Qt, QTimer
from PyQt6.QtGui import (QColor, QFont, QFontMetrics, QImage,
                         QPainter, QPainterPath, QPen, QPixmap, QTextLayout)
from PyQt6.QtWidgets import (QApplication, QFrame, QGraphicsBlurEffect,
                             QGraphicsPixmapItem, QGraphicsScene, QLabel,
                             QLineEdit, QMenu, QScrollArea, QVBoxLayout,
                             QWidget)

from .config import color
from .resources import get_icon
from .utils import make_highlighted_text, match_positions, split_query, substring_match

ICON_SIZE = 48
TILE_SIZE = 64
CARD_WIDTH = 176
GAP = 12
CARD_PADDING = 10
BLUR_DOWNSCALE = 4
BLUR_RADIUS = 12


def in_dark_mode():
    return QApplication.instance().in_dark_mode


def qcolor(key, dark_default, light_default):
    return QColor(color(key, dark_default if in_dark_mode() else light_default))


def blur_pixmap(pixmap, downscale=BLUR_DOWNSCALE, radius=BLUR_RADIUS):
    ''' Return a blurred version of pixmap with a size of pixmap.size() /
    downscale. Blurring a downscaled image is much faster and the result is
    indistinguishable once scaled back up. '''
    if pixmap.isNull():
        return QPixmap()
    w, h = max(1, pixmap.width() // downscale), max(1, pixmap.height() // downscale)
    small = pixmap.scaled(w, h, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)
    small.setDevicePixelRatio(1)
    # Pad the image by stretching it so that the blur does not fade to
    # transparent at the edges
    m = radius * 2
    padded = QPixmap(w + 2 * m, h + 2 * m)
    padded.fill(Qt.GlobalColor.black)
    p = QPainter(padded)
    p.drawPixmap(padded.rect(), small)
    p.drawPixmap(m, m, small)
    p.end()

    scene = QGraphicsScene()
    item = QGraphicsPixmapItem(padded)
    effect = QGraphicsBlurEffect()
    effect.setBlurRadius(radius)
    effect.setBlurHints(QGraphicsBlurEffect.BlurHint.QualityHint)
    item.setGraphicsEffect(effect)
    scene.addItem(item)
    img = QImage(padded.size(), QImage.Format.Format_ARGB32_Premultiplied)
    img.fill(Qt.GlobalColor.black)
    p = QPainter(img)
    scene.render(p, QRectF(img.rect()), QRectF(padded.rect()))
    p.end()
    return QPixmap.fromImage(img.copy(m, m, w, h))


def wrap_text(text, font, width, max_lines=2):
    ''' Wrap text into at most max_lines lines, eliding the last line if
    needed. Returns a list of (start, end, line_text) where line_text may have
    a trailing ellipsis. '''
    fm = QFontMetrics(font)
    layout = QTextLayout(text, font)
    layout.beginLayout()
    lines = []
    while True:
        line = layout.createLine()
        if not line.isValid():
            break
        line.setLineWidth(width)
        lines.append((line.textStart(), line.textStart() + line.textLength()))
    layout.endLayout()
    if not lines:
        return []
    ans = []
    for i, (start, end) in enumerate(lines[:max_lines]):
        if i == max_lines - 1 and end < len(text):
            end = len(text)
        line_text = text[start:end]
        if i == max_lines - 1:
            elided = fm.elidedText(line_text.rstrip(), Qt.TextElideMode.ElideRight, width)
            if elided != line_text.rstrip():
                # Qt replaces the end with an ellipsis
                kept = elided.rstrip('…')
                ans.append((start, start + len(kept), kept + '…'))
                continue
        ans.append((start, end, line_text.rstrip()))
    return ans


class Card:

    __slots__ = ('item', 'rect', 'group', 'title_lines', 'host_text', 'is_root')

    def __init__(self, item, group, is_root):
        self.item = item
        self.group = group
        self.is_root = is_root
        self.rect = QRect()
        self.title_lines = []
        self.host_text = None


class Group:

    __slots__ = ('root', 'cards', 'header_rect', 'header_text', 'total')

    def __init__(self, root, total):
        self.root = root
        self.total = total
        self.cards = []
        self.header_rect = QRect()
        self.header_text = None


class TabGrid(QWidget):

    def __init__(self, overlay, parent=None):
        QWidget.__init__(self, parent)
        self.overlay = overlay
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setMouseTracking(True)
        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent, False)
        self.groups = []
        self.cards = []
        self.rows = []
        self.substrings = []
        self.selected = None
        self.hovered = None
        self.close_hovered = False
        self.show_marks = False
        self.laid_out_width = -1
        f = QFont(self.font())
        self.title_font = f
        self.header_font = QFont(f)
        self.header_font.setBold(True)
        self.header_font.setPointSizeF(f.pointSizeF() * 1.1)
        self.host_font = QFont(f)
        self.host_font.setPointSizeF(f.pointSizeF() * 0.85)
        self.mark_font = QFont(f)
        self.mark_font.setBold(True)
        self.update_colors()

    def update_colors(self):
        self.text_color = qcolor('tab overlay foreground', '#eeeeee', '#111111')
        self.dim_text_color = QColor(self.text_color)
        self.dim_text_color.setAlphaF(0.65)
        self.accent = qcolor('tab overlay accent', '#5294e2', '#2a6fd6')
        self.card_bg = qcolor('tab overlay card', '#1affffff', '#14000000')
        self.card_hover_bg = qcolor('tab overlay card hover', '#30ffffff', '#24000000')
        self.card_selected_bg = qcolor('tab overlay card selected', '#4a5294e2', '#3a2a6fd6')
        self.tile_bg = qcolor('tab overlay icon tile', '#1fffffff', '#ccffffff')
        self.highlight = 'color:' + color('tab overlay match', '#ff79c6' if in_dark_mode() else '#c0007a')
        self.mark_bg = QColor(color('hint background', 'khaki'))
        self.mark_fg = QColor(color('hint foreground', 'black'))

    # Data {{{
    def set_data(self, tab_tree, substrings, show_marks=False):
        selected_item = self.selected.item if self.selected is not None else None
        hovered_item = self.hovered.item if self.hovered is not None else None
        self.substrings = substrings
        self.show_marks = show_marks
        self.groups, self.cards = [], []
        for root, items in tab_tree.groups():
            g = Group(root, len(items))
            for item in items:
                if item.tab is None:
                    continue
                if not substrings or substring_match(substrings, item.title, item.url):
                    c = Card(item, g, item is root)
                    g.cards.append(c)
            if g.cards:
                self.groups.append(g)
                self.cards.extend(g.cards)
        self.selected = self.hovered = None
        if selected_item is not None:
            self.selected = self.card_for_item(selected_item)
        if hovered_item is not None:
            self.hovered = self.card_for_item(hovered_item)
        self.laid_out_width = -1
        self.do_layout()
        self.update()

    def card_for_item(self, item):
        for c in self.cards:
            if c.item is item:
                return c

    def select_item(self, item, ensure_visible=True):
        c = self.card_for_item(item) if item is not None else None
        self.set_selected(c or (self.cards[0] if self.cards else None), ensure_visible)

    def set_selected(self, card, ensure_visible=True):
        self.selected = card
        if card is not None and ensure_visible:
            self.overlay.ensure_visible(card.rect)
        self.update()
    # }}}

    # Layout {{{
    def card_height(self):
        lh = QFontMetrics(self.title_font).lineSpacing()
        hh = QFontMetrics(self.host_font).lineSpacing()
        return CARD_PADDING + TILE_SIZE + 8 + 2 * lh + 4 + hh + CARD_PADDING

    def resizeEvent(self, ev):
        QWidget.resizeEvent(self, ev)
        if self.width() != self.laid_out_width:
            self.do_layout()

    def do_layout(self):
        width = self.width()
        self.laid_out_width = width
        avail = max(CARD_WIDTH, width - 2 * GAP)
        cols = max(1, (avail + GAP) // (CARD_WIDTH + GAP))
        card_width = (avail - (cols - 1) * GAP) // cols
        card_height = self.card_height()
        hfm = QFontMetrics(self.header_font)
        header_height = hfm.lineSpacing() + 12
        y = GAP // 2
        self.rows = []
        text_width = card_width - 2 * CARD_PADDING
        hostfm = QFontMetrics(self.host_font)
        for g in self.groups:
            g.header_rect = QRect(GAP, y, avail, header_height)
            title = g.root.title
            if len(g.cards) < g.total:
                count = ' (%d/%d)' % (len(g.cards), g.total)
            else:
                count = (' (%d)' % g.total) if g.total > 1 else ''
            g.header_text = hfm.elidedText(title, Qt.TextElideMode.ElideRight, avail - 28 - hfm.horizontalAdvance(count)) + count
            y += header_height + 4
            for i, c in enumerate(g.cards):
                col = i % cols
                if col == 0:
                    if i > 0:
                        y += card_height + GAP
                    self.rows.append([])
                self.rows[-1].append(c)
                c.rect = QRect(GAP + col * (card_width + GAP), y, card_width, card_height)
                c.title_lines = self.layout_title(c.item.title, text_width)
                host = c.item.host
                htext = hostfm.elidedText(host, Qt.TextElideMode.ElideMiddle, text_width)
                c.host_text = make_highlighted_text(
                    htext, match_positions(htext, self.substrings) if htext == host else [], emph=self.highlight)
            y += card_height + GAP * 2
        self.setMinimumHeight(y)
        self.update()

    def layout_title(self, title, width):
        ans = []
        fm = QFontMetrics(self.title_font)
        positions = match_positions(title, self.substrings)
        for start, end, text in wrap_text(title, self.title_font, width):
            pos = [p - start for p in positions if start <= p < end and p - start < len(text)]
            st = make_highlighted_text(text, pos, emph=self.highlight)
            ans.append((st, fm.horizontalAdvance(text)))
        return ans
    # }}}

    # Painting {{{
    def paintEvent(self, ev):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        p.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        try:
            self.paint(p, ev.rect())
        finally:
            p.end()

    def paint(self, p, clip):
        current = self.overlay.tab_tree.current_item
        if not self.cards:
            p.setPen(self.dim_text_color)
            p.setFont(self.header_font)
            p.drawText(self.rect().adjusted(0, 40, 0, 0), Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop, _('No matching tabs'))
            return
        for g in self.groups:
            if g.header_rect.intersects(clip):
                self.paint_header(p, g)
            for c in g.cards:
                if c.rect.intersects(clip):
                    self.paint_card(p, c, c.item is current)

    def paint_header(self, p, g):
        r = g.header_rect
        icon_rect = QRect(r.left() + 2, r.top() + (r.height() - 20) // 2 - 2, 20, 20)
        g.root.display_icon.paint(p, icon_rect)
        p.setPen(self.text_color)
        p.setFont(self.header_font)
        tr = QRect(icon_rect.right() + 8, r.top(), r.width() - 30, r.height() - 4)
        p.drawText(tr, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft | Qt.TextFlag.TextSingleLine, g.header_text)
        line_color = QColor(self.text_color)
        line_color.setAlphaF(0.15)
        p.setPen(QPen(line_color, 1))
        p.drawLine(r.left(), r.bottom(), r.right(), r.bottom())

    def paint_card(self, p, c, is_current):
        r = QRectF(c.rect)
        path = QPainterPath()
        path.addRoundedRect(r, 10, 10)
        is_selected = c is self.selected
        is_hovered = c is self.hovered
        bg = self.card_selected_bg if is_selected else (self.card_hover_bg if is_hovered else self.card_bg)
        p.fillPath(path, bg)
        if is_selected or is_current:
            pen = QPen(self.accent, 2.5 if is_selected else 1.5)
            if not is_selected:
                pen.setStyle(Qt.PenStyle.DashLine)
            p.setPen(pen)
            p.drawPath(path)

        # Icon tile
        tile = QRectF(r.center().x() - TILE_SIZE / 2, r.top() + CARD_PADDING, TILE_SIZE, TILE_SIZE)
        tpath = QPainterPath()
        tpath.addRoundedRect(tile, 14, 14)
        p.fillPath(tpath, self.tile_bg)
        self.paint_icon(p, c.item.display_icon, tile.toRect())
        badge = 20
        if c.item.loading:
            br = QRect(int(tile.right()) - badge + 4, int(tile.top()) - 4, badge, badge)
            get_icon('busy.svg').paint(p, br)
        if c.item.muted:
            br = QRect(int(tile.right()) - badge + 4, int(tile.bottom()) - badge + 4, badge, badge)
            get_icon('volume-off.svg').paint(p, br)

        # Title
        p.setPen(self.text_color)
        p.setFont(self.title_font)
        lh = QFontMetrics(self.title_font).lineSpacing()
        y = tile.bottom() + 8
        for st, w in c.title_lines:
            x = r.left() + (r.width() - w) / 2
            p.drawStaticText(QPointF(x, y), st)
            y += lh
        # Host
        y = r.top() + CARD_PADDING + TILE_SIZE + 8 + 2 * lh + 4
        p.setPen(self.dim_text_color)
        p.setFont(self.host_font)
        st = c.host_text
        x = r.left() + (r.width() - st.size().width()) / 2
        p.drawStaticText(QPointF(x, y), st)

        if self.show_marks and c.item.mark:
            p.setFont(self.mark_font)
            fm = QFontMetrics(self.mark_font)
            s = max(fm.height(), fm.horizontalAdvance(c.item.mark)) + 8
            mr = QRectF(r.left() + 6, r.top() + 6, s, s)
            mp = QPainterPath()
            mp.addRoundedRect(mr, 5, 5)
            p.fillPath(mp, self.mark_bg)
            p.setPen(self.mark_fg)
            p.drawText(mr, Qt.AlignmentFlag.AlignCenter, c.item.mark)
        elif is_hovered:
            cr = self.close_rect(c)
            if self.close_hovered:
                cp = QPainterPath()
                cp.addEllipse(QRectF(cr))
                p.fillPath(cp, QColor(220, 50, 50, 200))
            p.setPen(QPen(self.text_color, 1.6))
            m = 7
            p.drawLine(cr.left() + m, cr.top() + m, cr.right() - m + 1, cr.bottom() - m + 1)
            p.drawLine(cr.right() - m + 1, cr.top() + m, cr.left() + m, cr.bottom() - m + 1)

    def paint_icon(self, p, icon, tile):
        sizes = icon.availableSizes()
        largest = max((s.width() for s in sizes), default=0)
        if largest and largest < ICON_SIZE:
            # Scale small favicons up by an integer factor so they stay crisp
            sz = largest * max(1, ICON_SIZE // largest)
        else:
            sz = ICON_SIZE
        dpr = self.devicePixelRatioF()
        pm = icon.pixmap(QSize(sz, sz), dpr)
        if pm.isNull():
            return
        target = QRect(0, 0, sz, sz)
        target.moveCenter(tile.center())
        p.drawPixmap(target, pm)
    # }}}

    # Mouse handling {{{
    def close_rect(self, c):
        s = 22
        return QRect(c.rect.right() - s - 4, c.rect.top() + 4, s, s)

    def card_at(self, pos):
        for c in self.cards:
            if c.rect.contains(pos):
                return c

    def mouseMoveEvent(self, ev):
        pos = ev.position().toPoint()
        c = self.card_at(pos)
        close_hovered = c is not None and self.close_rect(c).contains(pos)
        if c is not self.hovered or close_hovered != self.close_hovered:
            self.hovered, self.close_hovered = c, close_hovered
            self.setCursor(Qt.CursorShape.PointingHandCursor if c is not None else Qt.CursorShape.ArrowCursor)
            self.update()

    def leaveEvent(self, ev):
        self.hovered = None
        self.close_hovered = False
        self.update()

    def mousePressEvent(self, ev):
        ev.accept()

    def mouseReleaseEvent(self, ev):
        pos = ev.position().toPoint()
        c = self.card_at(pos)
        if c is None:
            return
        if ev.button() == Qt.MouseButton.LeftButton:
            if self.close_rect(c).contains(pos) and not self.show_marks:
                self.overlay.close_item(c.item)
            else:
                self.overlay.activate_item(c.item)
        elif ev.button() == Qt.MouseButton.MiddleButton:
            self.overlay.close_item(c.item)

    def contextMenuEvent(self, ev):
        c = self.card_at(ev.pos())
        if c is None:
            return
        self.set_selected(c)
        self.overlay.show_context_menu(c.item, ev.globalPos())
    # }}}

    # Keyboard navigation {{{
    def move_selection(self, delta):
        if not self.cards:
            return
        if self.selected is None:
            self.set_selected(self.cards[0 if delta > 0 else -1])
            return
        idx = self.cards.index(self.selected)
        self.set_selected(self.cards[(idx + delta) % len(self.cards)])

    def move_row(self, delta):
        if not self.rows:
            return
        if self.selected is None:
            self.move_selection(delta)
            return
        for ri, row in enumerate(self.rows):
            if self.selected in row:
                break
        nri = ri + delta
        if nri < 0 or nri >= len(self.rows):
            return
        x = self.selected.rect.center().x()
        target = min(self.rows[nri], key=lambda c: abs(c.rect.center().x() - x))
        self.set_selected(target)

    def move_page(self, delta):
        h = self.overlay.scroll_area.viewport().height()
        rows = max(1, h // (self.card_height() + GAP))
        for i in range(rows):
            self.move_row(delta)

    def move_to_end(self, end):
        if self.cards:
            self.set_selected(self.cards[-1 if end else 0])
    # }}}


class SearchEdit(QLineEdit):

    passthrough_keys = True

    def __init__(self, overlay):
        QLineEdit.__init__(self, overlay)
        self.overlay = overlay
        self.setAttribute(Qt.WidgetAttribute.WA_MacShowFocusRect, False)
        self.setPlaceholderText(_('Search tabs…'))
        self.setClearButtonEnabled(False)
        f = QFont(self.font())
        f.setPointSizeF(f.pointSizeF() * 1.3)
        self.setFont(f)

    def keyPressEvent(self, ev):
        if self.overlay.handle_key(ev):
            ev.accept()
            return
        QLineEdit.keyPressEvent(self, ev)

    def event(self, ev):
        # Prevent Tab from moving focus out of the search box
        if ev.type() == QEvent.Type.KeyPress and ev.key() in (Qt.Key.Key_Tab, Qt.Key.Key_Backtab):
            self.keyPressEvent(ev)
            return True
        return QLineEdit.event(self, ev)


class TabOverlay(QWidget):

    def __init__(self, window):
        QWidget.__init__(self, window)
        self.window_ = window
        self.tab_tree = window.tab_tree
        self.hide()
        self.background = QPixmap()
        self.marks_mode = False
        self.setAutoFillBackground(False)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.panel = QFrame(self)
        self.panel.setAutoFillBackground(False)
        l = QVBoxLayout(self.panel)
        l.setContentsMargins(20, 20, 20, 12)
        l.setSpacing(14)
        self.search = s = SearchEdit(self.panel)
        s.overlay = self
        s.textChanged.connect(self.search_changed)
        l.addWidget(s)
        self.marks_label = ml = QLabel(_('Press the key shown on a tab to switch to it, Esc to cancel'), self.panel)
        ml.setAlignment(Qt.AlignmentFlag.AlignCenter)
        f = QFont(ml.font())
        f.setPointSizeF(f.pointSizeF() * 1.2)
        ml.setFont(f)
        l.addWidget(ml)
        self.scroll_area = sa = QScrollArea(self.panel)
        sa.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        sa.setFrameShape(QFrame.Shape.NoFrame)
        sa.setWidgetResizable(True)
        sa.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        sa.viewport().setAutoFillBackground(False)
        self.grid = TabGrid(self)
        sa.setWidget(self.grid)
        l.addWidget(sa)

        self.refresh_timer = t = QTimer(self)
        t.setSingleShot(True), t.setInterval(30)
        t.timeout.connect(self.refresh)
        self.tab_tree.changed.connect(self.schedule_refresh)
        self.background_timer = bt = QTimer(self)
        bt.setSingleShot(True), bt.setInterval(150)
        bt.timeout.connect(self.update_background)
        window.centralWidget().installEventFilter(self)
        self.update_styles()

    def update_styles(self):
        self.grid.update_colors()
        fg = self.grid.text_color.name()
        edit_bg = qcolor('tab overlay search background', '#33ffffff', '#99ffffff')
        sel = self.grid.accent.name()
        self.search.setStyleSheet(f'''
            QLineEdit {{
                border-radius: 10px;
                padding: 8px 12px;
                background: rgba({edit_bg.red()}, {edit_bg.green()}, {edit_bg.blue()}, {edit_bg.alpha()});
                color: {fg};
                border: 1px solid rgba(127, 127, 127, 90);
                selection-background-color: {sel};
            }}
        ''')
        self.marks_label.setStyleSheet(f'QLabel {{ color: {fg}; background: transparent }}')
        self.scroll_area.setStyleSheet('''
            QScrollArea { background: transparent; border: none }
            QScrollArea > QWidget > QWidget { background: transparent }
            QScrollBar:vertical { background: transparent; width: 8px; margin: 0 }
            QScrollBar::handle:vertical { background: rgba(127, 127, 127, 140); border-radius: 4px; min-height: 30px }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0 }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: none }
        ''')

    # Showing/hiding {{{
    def toggle(self):
        if self.isVisible():
            self.dismiss()
        else:
            self.show_overlay()

    def show_overlay(self, marks_mode=False):
        if self.isVisible() and self.marks_mode != marks_mode:
            self.dismiss()
        self.marks_mode = marks_mode
        self.window_.save_scroll()
        self.update_styles()
        self.update_geometry()
        self.update_background()
        self.search.setVisible(not marks_mode)
        self.marks_label.setVisible(marks_mode)
        self.search.blockSignals(True)
        self.search.clear()
        self.search.blockSignals(False)
        self.refresh()
        self.grid.select_item(self.tab_tree.current_item)
        self.show()
        self.raise_()
        if marks_mode:
            # Keys are handled by the KeyFilter via choose_tab_pending. Focus
            # the overlay itself rather than the web view, as the web view
            # swallows some keys, such as Escape.
            self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
            self.setFocus(Qt.FocusReason.OtherFocusReason)
        else:
            self.search.setFocus(Qt.FocusReason.OtherFocusReason)
        QTimer.singleShot(0, lambda: self.grid.select_item(self.tab_tree.current_item))

    def dismiss(self):
        if not self.isVisible():
            return
        self.hide()
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.background = QPixmap()
        if self.marks_mode:
            self.marks_mode = False
            self.window_.choose_tab_pending = None
            self.tab_tree.mark_tabs(unmark=True)
        ct = self.window_.current_tab
        if ct is not None:
            ct.setFocus(Qt.FocusReason.OtherFocusReason)
        self.window_.restore_state_after_popup()
    # }}}

    # Geometry and background {{{
    def eventFilter(self, obj, ev):
        if ev.type() in (QEvent.Type.Resize, QEvent.Type.Move) and self.isVisible():
            self.update_geometry()
            self.background_timer.start()
        return False

    def update_geometry(self):
        cw = self.window_.centralWidget()
        self.setGeometry(cw.geometry())
        w, h = self.width(), self.height()
        mx = max(12, min(64, w // 16))
        my = max(12, min(48, h // 16))
        pw = min(w - 2 * mx, 1280)
        ph = h - 2 * my
        self.panel.setGeometry((w - pw) // 2, my, pw, ph)

    def update_background(self):
        cw = self.window_.centralWidget()
        try:
            pm = cw.grab()
        except Exception:
            pm = QPixmap()
        self.background = blur_pixmap(pm) if not pm.isNull() else QPixmap()
        self.update()

    def paintEvent(self, ev):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        r = self.rect()
        if not self.background.isNull():
            p.drawPixmap(r, self.background)
        p.fillRect(r, qcolor('tab overlay tint', '#73000000', '#59ffffff'))
        pr = QRectF(self.panel.geometry())
        path = QPainterPath()
        path.addRoundedRect(pr, 18, 18)
        p.fillPath(path, qcolor('tab overlay panel', '#a0202024', '#b0f4f4f6'))
        p.setPen(QPen(QColor(255, 255, 255, 40) if in_dark_mode() else QColor(0, 0, 0, 40), 1))
        p.drawPath(path)
        p.end()

    def mousePressEvent(self, ev):
        if not self.panel.geometry().contains(ev.position().toPoint()):
            self.dismiss()
        ev.accept()

    def keyPressEvent(self, ev):
        # Only reached in marks mode if the KeyFilter did not handle the key
        if ev.key() in (Qt.Key.Key_Shift, Qt.Key.Key_Control, Qt.Key.Key_Alt, Qt.Key.Key_Meta):
            return
        if self.marks_mode and self.window_.choose_tab_pending:
            self.window_.choose_tab(ev.keyCombination())
        elif ev.key() == Qt.Key.Key_Escape:
            self.dismiss()
        ev.accept()

    def wheelEvent(self, ev):
        ev.accept()

    def ensure_visible(self, rect):
        c = rect.center()
        self.scroll_area.ensureVisible(c.x(), c.y(), rect.width() // 2 + GAP, rect.height() // 2 + GAP)
    # }}}

    # Data {{{
    def schedule_refresh(self):
        if self.isVisible():
            self.refresh_timer.start()

    def search_changed(self):
        self.refresh(ensure_selected_visible=True)

    def refresh(self, ensure_selected_visible=False):
        # Only scroll to the selected card when the set of displayed cards
        # changes because of the search text, otherwise changes to the tabs,
        # such as closing some tab, would cause the overlay to scroll away
        # from where the user is.
        self.grid.set_data(self.tab_tree, split_query(self.search.text()), show_marks=self.marks_mode)
        if self.grid.selected is None and self.grid.cards:
            self.grid.select_item(self.tab_tree.current_item, ensure_selected_visible)
        elif self.grid.selected is not None and ensure_selected_visible:
            self.ensure_visible(self.grid.selected.rect)
    # }}}

    # Actions {{{
    def activate_item(self, item):
        if self.marks_mode:
            self.window_.choose_tab_pending = None
        self.tab_tree.activate_item(item)
        self.dismiss()

    def close_item(self, item):
        tab = item.tab
        if tab is None:
            return
        cards = self.grid.cards
        selection_moved = False
        if self.grid.selected is not None and self.grid.selected.item is item and len(cards) > 1:
            # Select a neighbor of the card being closed
            idx = cards.index(self.grid.selected)
            neighbor = cards[idx + 1] if idx + 1 < len(cards) else cards[idx - 1]
            self.grid.selected = neighbor
            selection_moved = True
        self.window_.close_tab(tab)
        self.refresh(ensure_selected_visible=selection_moved)
        # The current tab may have changed, update the blurred background
        self.background_timer.start()
        self.search.setFocus(Qt.FocusReason.OtherFocusReason)

    def close_group(self, item):
        self.tab_tree.close_tree(item)
        if not self.window_.tabs:
            self.window_.close_tab()

    def show_context_menu(self, item, pos):
        m = QMenu(self)
        m.addAction(_('Switch to this tab'), partial(self.activate_item, item))
        m.addAction(_('Close this tab'), partial(self.close_item, item))
        m.addSeparator()
        m.addAction(_('Close tabs to the bottom'), partial(self.tab_tree.close_tabs_to_bottom, item))
        m.addAction(_('Close other tabs'), partial(self.tab_tree.close_other_tabs, item))
        root = item
        while root.parent() is not None:
            root = root.parent()
        m.addAction(_('Close this group'), partial(self.close_group, root))
        m.exec(pos)
        if self.isVisible() and not self.marks_mode:
            self.search.setFocus(Qt.FocusReason.OtherFocusReason)

    def handle_key(self, ev):
        key, mods = ev.key(), ev.modifiers()
        ctrl = bool(mods & Qt.KeyboardModifier.ControlModifier)
        g = self.grid
        empty = not self.search.text()
        if key == Qt.Key.Key_Escape:
            self.dismiss()
        elif ctrl and key == Qt.Key.Key_T:
            self.dismiss()
        elif key in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            if g.selected is not None:
                self.activate_item(g.selected.item)
        elif key == Qt.Key.Key_Down:
            g.move_row(1)
        elif key == Qt.Key.Key_Up:
            g.move_row(-1)
        elif key == Qt.Key.Key_Tab or (ctrl and key in (Qt.Key.Key_N, Qt.Key.Key_J)) or (key == Qt.Key.Key_Right and empty):
            g.move_selection(1)
        elif key == Qt.Key.Key_Backtab or (ctrl and key in (Qt.Key.Key_P, Qt.Key.Key_K)) or (key == Qt.Key.Key_Left and empty):
            g.move_selection(-1)
        elif key == Qt.Key.Key_PageDown:
            g.move_page(1)
        elif key == Qt.Key.Key_PageUp:
            g.move_page(-1)
        elif ctrl and key in (Qt.Key.Key_Home, Qt.Key.Key_End):
            g.move_to_end(key == Qt.Key.Key_End)
        elif ctrl and key == Qt.Key.Key_W or (key == Qt.Key.Key_Delete and mods & Qt.KeyboardModifier.ShiftModifier):
            if g.selected is not None:
                self.close_item(g.selected.item)
        else:
            return False
        return True
    # }}}
