#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2015, Kovid Goyal <kovid at kovidgoyal.net>

import os
import re
import math
import time
import unicodedata
from collections import OrderedDict
from itertools import repeat
from enum import Enum, unique

import apsw
from PyQt5.Qt import QWebEnginePage

from .constants import config_dir
from .resources import get_data


def now():
    return int(time.time() * 1e6)


def normalize(x):
    return unicodedata.normalize('NFC', x)

DAY = int(24 * 60 * 60 * 1e6)


@unique
class VisitType(Enum):
    link_clicked = 0
    typed = 1
    form_submitted = 2
    back_forward = 3
    reload = 4
    other = 5

FRECENCY_NUM_VISITS = 10
VISIT_TYPE_WEIGHTS = {VisitType.link_clicked.value: 120, VisitType.typed.value: 200}
RECENCY_WEIGHTS = [100, 70, 50, 30, 10]


def from_qt(key):
    ans = re.sub(r'[A-Z]', lambda m: '_' + m.group().lower(), key[len('NavigationType'):]).lstrip('_')
    return getattr(VisitType, ans)

qt_visit_types = {
    val: from_qt(key) for key, val in vars(QWebEnginePage).items() if key.startswith('NavigationType') and key != 'NavigationType'
}
del from_qt


class Places:

    path = os.path.join(config_dir, 'places.sqlite')

    def __init__(self, path=None):
        self._conn = None
        if path:
            self.path = path

    @property
    def conn(self):
        if self._conn is None:
            self._conn = apsw.Connection(self.path)
            self._conn.createscalarfunction('lower_case', lambda x: x.lower(), 1)
            c = self._conn.cursor()
            c.execute('PRAGMA foreign_keys = ON')
            uv = next(c.execute('PRAGMA user_version'))[0]
            if uv == 0:
                c.execute(get_data('places.sqlite').decode('utf-8'))
            c.close()
        return self._conn

    def insert(self, table, cursor=None, **kw):
        cursor = cursor or self.conn.cursor()
        values = ('?,' * len(kw)).rstrip(',')
        kw = OrderedDict(kw.items())
        cursor.execute('INSERT INTO %s (%s) VALUES (%s)' % (table, ','.join(kw), values), tuple(kw.values()))
        return self.conn.last_insert_rowid()

    def on_visit(self, qurl, visit_type, is_main_frame):
        if not is_main_frame:
            return
        visit_type = qt_visit_types[visit_type]
        if not VISIT_TYPE_WEIGHTS.get(visit_type.value, 0):
            return
        url = normalize(qurl.toString())
        timestamp = now()
        with self.conn:
            c = self.conn.cursor()
            try:
                place_id, visit_count, typed = next(c.execute('SELECT id, visit_count, typed FROM places WHERE url=?', (url,)))
                typed = bool(typed)
            except StopIteration:
                typed = visit_type is VisitType.typed
                place_id = self.insert('places', cursor=c, url=url, typed=int(typed))
                visit_count = 0
            typed = typed or visit_type is VisitType.typed
            self.insert('visits', cursor=c, place_id=place_id, visit_date=timestamp, type=visit_type.value)
            frecency = self.calculate_frecency(place_id, visit_count, cursor=c)
            c.execute('UPDATE places SET visit_count = ?, last_visit_date = ?, typed = ?, frecency = ? WHERE id=?', (
                visit_count + 1, timestamp, typed, frecency, place_id))

    def calculate_frecency(self, place_id, visit_count, cursor=None):
        ' Algorithm taken from: https://developer.mozilla.org/en-US/docs/Mozilla/Tech/Places/Frecency_algorithm '
        cursor = cursor or self.conn.cursor()
        visit_weights = []
        for visit_date, visit_type in cursor.execute(
                'SELECT visit_date, type FROM visits WHERE place_id=? ORDER BY visit_date DESC LIMIT ?', (place_id, FRECENCY_NUM_VISITS)):
            type_weight = VISIT_TYPE_WEIGHTS.get(visit_type, 0)
            if type_weight == 0:
                continue
            days = abs(now() - visit_date) // DAY
            bucket = 4
            if days <= 4:
                bucket = 0
            elif days <= 14:
                bucket = 1
            elif days <= 31:
                bucket = 2
            elif days <= 90:
                bucket = 3
            visit_weights.append((type_weight / 100) * RECENCY_WEIGHTS[bucket])
        try:
            frecency = int(math.ceil(visit_count * sum(visit_weights) / len(visit_weights)))
        except ZeroDivisionError:
            frecency = 0
        return frecency

    def on_title_change(self, qurl, title):
        title = normalize(title.strip())
        if qurl.isEmpty() or not title:
            return
        url = normalize(qurl.toString())
        with self.conn:
            c = self.conn.cursor()
            try:
                place_id, old_title = next(c.execute('SELECT id,title FROM places WHERE url=?', (url,)))
            except StopIteration:
                return
            if old_title == title:
                return
            c.execute('UPDATE places SET title=? WHERE id=?', (title, place_id))

    def on_favicon_change(self, qurl, favicon_qurl):
        if qurl.isEmpty():
            return
        url = qurl.toString()
        favicon = favicon_qurl.toString()
        with self.conn:
            c = self.conn.cursor()
            try:
                place_id = next(c.execute('SELECT id FROM places WHERE url=?', (url,)))[0]
            except StopIteration:
                return
            if not favicon:
                c.execute('DELETE FROM favicons_link WHERE place_id=?', (place_id,))
                return
            ts = now()
            try:
                favicon_id = next(c.execute('SELECT id FROM favicons WHERE url=?', (favicon,)))[0]
                c.execute('UPDATE favicons SET last_visit_date=? WHERE id=?', (ts, favicon_id))
            except StopIteration:
                favicon_id = self.insert('favicons', url=favicon, last_visit_date=ts)
            c.execute('INSERT OR IGNORE INTO favicons_link (favicon_id, place_id) VALUES (?, ?)', (favicon_id, place_id))

    def prune(self, days=400):
        limit = now() - (days * DAY)
        c = self.conn.cursor()
        c.execute('DELETE FROM places WHERE last_visit_date < ?; DELETE FROM favicons WHERE last_visit_date < ?', (limit, limit))

    def close(self):
        if self._conn:
            self.prune()
            self._conn.close()
            self._conn = None

    def subsequence_matches(self, subsequence=None, limit=50):
        c = self.conn.cursor()
        if not subsequence:
            for url, title in c.execute('SELECT url, title FROM PLACES ORDER BY frecency DESC LIMIT ?', (limit,)):
                yield url, title
            return

        subsequence = normalize((subsequence or ''))[:20]
        like_expr = re.sub(r'([|%_])', r'|\1', subsequence.lower())
        like_expr = '%' + '%'.join(like_expr) + '%'

        for url, title in c.execute(
                'SELECT url, title FROM places WHERE url_lower LIKE ? ESCAPE "|" OR title_lower LIKE ? ESCAPE "|" ORDER BY frecency DESC LIMIT ?',
                (like_expr, like_expr, limit)):
            yield url, title

    def substring_matches(self, substrings=None, limit=50):
        c = self.conn.cursor()
        if not substrings:
            for url, title in c.execute('SELECT url, title FROM PLACES ORDER BY frecency DESC LIMIT ?', (limit,)):
                yield url, title
            return
        substrings = map(normalize, substrings)
        like_expressions = tuple('%' + re.sub(r'([|%_])', r'|\1', x.lower()) + '%' for x in substrings)
        where_clause = ' AND '.join(repeat('(url_lower LIKE ? OR title_lower LIKE ?)', len(like_expressions)))

        for url, title in c.execute(
                'SELECT url, title FROM places WHERE %s ORDER BY frecency DESC LIMIT %d' % (where_clause, limit),
                (x for x in like_expressions for y in (0, 1))):
            yield url, title


places = Places()


def import_from_firefox():
    global places
    from glob import glob
    places.close()
    os.remove(places.path)
    places = Places()
    conn = apsw.Connection(glob(os.path.expanduser('~/.mozilla/firefox/*/places.sqlite'))[0])
    place_id_map = {}
    with places.conn:
        print('Importing places table')
        for place_id, url, title, visit_count, typed, frecency, last_visit_date in conn.cursor().execute(
                'SELECT id,url,title,visit_count,typed,frecency,last_visit_date FROM moz_places'):
            if last_visit_date and visit_count and frecency > 0 and url:
                place_id_map[place_id] = places.insert(
                    'places', url=url, title=title or '_', visit_count=visit_count, typed=typed, frecency=frecency, last_visit_date=last_visit_date)
        print('Importing visits table')
        items = []
        for place_id, visit_date, visit_type in conn.cursor().execute(
                'SELECT place_id,visit_date,visit_type FROM moz_historyvisits'):
            place_id = place_id_map.get(place_id)
            if place_id is not None and visit_date and visit_type in (1, 2):
                items.append((place_id, visit_date, {1: VisitType.link_clicked, 2: VisitType.typed}[visit_type].value))
        places.conn.cursor().executemany(
            'INSERT INTO visits (place_id, visit_date, type) VALUES (?, ?, ?)', items)
    conn.close()
