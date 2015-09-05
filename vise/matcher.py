#!/usr/bin/env python
# vim:fileencoding=utf-8


import atexit
import os
from math import ceil
from unicodedata import normalize
from threading import Thread, Lock
from queue import Queue
from operator import itemgetter
from collections import OrderedDict
from multiprocessing import cpu_count as get_cpu_count

from . import matcher_native

DEFAULT_LEVEL1 = '/ .'
DEFAULT_LEVEL2 = '-_0123456789'
DEFAULT_LEVEL3 = ':;'

_cpu_count = None


def cpu_count():
    global _cpu_count
    if _cpu_count is None:
        _cpu_count = get_cpu_count()
    return _cpu_count


class PluginFailed(RuntimeError):
    pass


class Worker(Thread):

    daemon = True

    def __init__(self, requests, results):
        Thread.__init__(self)
        self.requests, self.results = requests, results
        atexit.register(lambda: requests.put(None))

    def run(self):
        while True:
            x = self.requests.get()
            if x is None:
                break
            try:
                i, scorer, query = x
                self.results.put((True, (i, scorer(query))))
            except Exception as e:
                self.results.put((False, str(e)))
                # import traceback
                # traceback.print_exc()
wlock = Lock()
workers = []


def split(tasks, pool_size):
    '''
    Split a list into a list of sub lists, with the number of sub lists being
    no more than pool_size. Each sublist contains
    2-tuples of the form (i, x) where x is an element from the original list
    and i is the index of the element x in the original list.
    '''
    ans, count = [], 0
    delta = int(ceil(len(tasks) / pool_size))
    while tasks:
        section = [(count + i, task) for i, task in enumerate(tasks[:delta])]
        tasks = tasks[delta:]
        count += len(section)
        ans.append(section)
    return ans


class Matcher(object):

    def __init__(self, items, level1=DEFAULT_LEVEL1, level2=DEFAULT_LEVEL2, level3=DEFAULT_LEVEL3, scorer=None):
        with wlock:
            if not workers:
                requests, results = Queue(), Queue()
                w = [Worker(requests, results) for i in range(max(1, cpu_count()))]
                [x.start() for x in w]
                workers.extend(w)
        items = map(lambda x: normalize('NFC', str(x)), filter(None, items))
        self.items = items = tuple(items)
        tasks = split(items, len(workers))
        self.task_maps = [{j: i for j, (i, _) in enumerate(task)} for task in tasks]
        scorer = scorer or CScorer
        self.scorers = [scorer(tuple(map(itemgetter(1), task_items))) for task_items in tasks]
        self.sort_keys = None

    def __call__(self, query, limit=None):
        query = normalize('NFC', str(query))
        with wlock:
            for i, scorer in enumerate(self.scorers):
                workers[0].requests.put((i, scorer, query))
            if self.sort_keys is None:
                self.sort_keys = {i: x.casefold() for i, x in enumerate(self.items)}
            num = len(self.task_maps)
            scores, positions = {}, {}
            error = None
            while num > 0:
                ok, x = workers[0].results.get()
                num -= 1
                if ok:
                    task_num, vals = x
                    task_map = self.task_maps[task_num]
                    for i, (score, pos) in enumerate(vals):
                        item = task_map[i]
                        scores[item] = score
                        positions[item] = pos
                else:
                    error = x

        if error is not None:
            raise Exception('Failed to score items: %s' % error)
        items = sorted(((-scores[i], item, positions[i]) for i, item in enumerate(self.items)),
                       key=itemgetter(0))
        if limit is not None:
            del items[limit:]
        return OrderedDict(x[1:] for x in filter(itemgetter(0), items))


def get_items_from_dir(basedir, acceptq=lambda x: True):
    relsep = os.sep != '/'
    for dirpath, dirnames, filenames in os.walk(basedir):
        for f in filenames:
            x = os.path.join(dirpath, f)
            if acceptq(x):
                x = os.path.relpath(x, basedir)
                if relsep:
                    x = x.replace(os.sep, '/')
                yield x


class FilesystemMatcher(Matcher):

    def __init__(self, basedir, *args, **kwargs):
        Matcher.__init__(self, get_items_from_dir(basedir), *args, **kwargs)


class CScorer(object):

    def __init__(self, items, level1=DEFAULT_LEVEL1, level2=DEFAULT_LEVEL2, level3=DEFAULT_LEVEL3):
        self.m = matcher_native.Matcher(items, str(level1), str(level2), str(level3))

    def __call__(self, query):
        scores, positions = self.m.calculate_scores(query)
        for score, pos in zip(scores, positions):
            yield score, pos


def test():
    import unittest

    class Test(unittest.TestCase):

        def test_non_bmp(self):
            raw = '_\U0001f431-'
            m = Matcher([raw], scorer=CScorer)
            positions = next(iter(m(raw).values()))
            self.assertEqual(positions, (0, 1, 2))

    class TestRunner(unittest.main):

        def createTests(self):
            tl = unittest.TestLoader()
            self.test = tl.loadTestsFromTestCase(Test)

    TestRunner(verbosity=4)


if __name__ == '__main__':
    test()
