#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2016, Kovid Goyal <kovid at kovidgoyal.net>

import re
import os
from collections import namedtuple
from gettext import gettext as _
from urllib.parse import urlparse

from .constants import config_dir

Host = namedtuple('Host', 'pat prefix postfix')


def compile_host(host):
    host = host.lower()
    has_prefix_wildcard = has_postfix_wildcard = False
    if host.startswith('*.'):
        host = host[2:]
        has_prefix_wildcard = True
    if host.endswith('.*'):
        host = host[:-2]
        has_postfix_wildcard = True
    return Host(re.compile(re.escape(host)), has_prefix_wildcard, has_postfix_wildcard)


def validate_rule(rule):
    if not rule.get('name'):
        return _('Rule has no name')
    if not rule.get('host'):
        return _('The rule {0} has no hosts'.format(rule['name']))
    rules = rule.get('rules')
    if not rules:
        return _('Rule for {0} has no from/to regexps'.format(rule['name']))
    compiled_rules = []
    for x in rules:
        if len(x) != 2:
            return _('From/to expression {0} has {1} parts. Must have only two parts.').format(x[0], len(x))
        f, t = x
        try:
            f = re.compile(f)
        except re.error:
            return _('Could not compile the regular expression: {0}').format(f)
        compiled_rules.append((f, t))
    rule['rules'] = compiled_rules
    rule['host'] = tuple(compile_host(x) for x in rule['host'])
    return None


def parse_rules(raw):
    rules = []
    current_rule = {}

    def commit_rule():
        err = validate_rule(current_rule)
        if err is None:
            rules.append(current_rule)
        else:
            print(_('Invalid URL substitution rule: {0}').format(err))
        return {}

    for line in raw.splitlines():
        if line.startswith('#'):
            continue
        line = line.strip()
        if not line:
            if current_rule:
                current_rule = commit_rule()
            continue
        if 'name' not in current_rule:
            current_rule['name'] = line
        elif 'host' not in current_rule:
            current_rule['host'] = line.split()
        elif 'rules' not in current_rule:
            current_rule['rules'] = [re.split(r'\s+', line, 1)]
        else:
            current_rule['rules'].append(re.split(r'\s+', line, 1))
    if current_rule:
        current_rule = commit_rule()
    return rules


def substitution_rules(refresh=False):
    if refresh:
        substitution_rules.rules = None
    rules = getattr(substitution_rules, 'rules', None)
    if rules is None:
        try:
            with open(os.path.join(config_dir, 'url-substitution.rules'), 'rb') as f:
                raw = f.read().decode('utf-8')
        except FileNotFoundError:
            raw = ''
        rules = substitution_rules.rules = parse_rules(raw)
    return rules


def host_matches(host, compiled_host):
    parts = compiled_host.pat.split(host, 1)
    if len(parts) != 2:
        return False
    before, after = parts
    if before and (not compiled_host.prefix or not before.endswith('.')):
        return False
    if after and (not compiled_host.postfix or not after.startswith('.') or after.count('.') != 1):
        return False
    return True


def test_host_matching():
    for line in '''
            foo.com foo.com y
            foo.com *.foo.com y
            www.foo.com *.foo.com y
            www.ab.foo.com *.foo.com y
            xfoo.com *.foo.com n
            foo.co.in foo.co.* y
            www.foo.co.in *.foo.co.* y
            www.foo.co.in foo.co.* n
            foo.co.in.me foo.co.* n
    '''.splitlines():
        line = line.strip()
        if line:
            host, q, ok = line.split()
            ok = ok == 'y'
            if host_matches(host, compile_host(q)) != ok:
                raise AssertionError('{} {} {}'.format(q, '==' if ok else '!=', host))


def substitute(url, ruleset=None):
    purl = urlparse(url)
    host = purl.hostname
    if not host:
        return False, url
    if ruleset is None:
        ruleset = substitution_rules()
    for rule in ruleset:
        for q in rule['host']:
            if host_matches(host, q):
                break
        else:
            continue
        for f, t in rule['rules']:
            nurl, num = f.subn(t, url)
            if num > 0:
                return True, nurl
        break
    return False, url


def test_substitute():
    rules = parse_rules('''
foo
*.foo.com
^http: https:
''')
    for line in '''
http://foo.com https://foo.com
http://a.foo.com/xxx?x=y#1 https://a.foo.com/xxx?x=y#1
'''.splitlines():
        line = line.strip()
        if line:
            url, expected = line.partition(' ')[::2]
            ok, nurl = substitute(url, rules)
            assert nurl == expected, '{} == {}'.format(nurl, expected)
