#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2015, Kovid Goyal <kovid at kovidgoyal.net>

import json
import os
import hashlib
import struct
import tempfile
from binascii import hexlify, unhexlify
from threading import Thread
from urllib.parse import urlparse

from ..constants import config_dir
from ..crypto import derive_key_v1, generate_salt_v1, nonce_size_v1, decrypt_v1, encrypt_v1, lock_python_bytes, MessageForged
from ..utils import atomic_write


class PasswordWrong(ValueError):
    pass


class PasswordStore:  # {{{

    def __init__(self, password, dirpath=None):
        dirpath = os.path.realpath(dirpath or os.path.join(config_dir, 'passwd'))
        self.root = dirpath
        if isinstance(password, str):
            password = password.encode('utf-8')
        lock_python_bytes(password)
        try:
            os.makedirs(self.root)
        except FileExistsError:
            pass
        self.metadata_path = os.path.join(self.root, 'metadata.json')
        try:
            with open(self.metadata_path, 'rb') as f:
                self.metadata = json.loads(f.read().decode('utf-8'))
        except FileNotFoundError:
            self.metadata = {
                'version': 1,
                'salt': hexlify(generate_salt_v1()).decode('ascii')
            }
        self.password = password
        self.run_derive()

    def run_derive(self):
        self.key = self.key_error = None
        self.derive_worker = Thread(name='DeriveKey', target=self.derive_key)
        self.derive_worker.daemon = True
        self.derive_worker.start()

    def commit_metadata(self):
        raw = json.dumps(self.metadata, indent=2, ensure_ascii=False).encode('utf-8')
        atomic_write(self.metadata_path, raw)

    def derive_key(self):
        pw, self.password = self.password, None
        try:
            self.key = derive_key_v1(pw, unhexlify(self.metadata['salt']))[0]
            if 'sentinel' not in self.metadata:
                cipher, nonce = encrypt_v1(b'sentinel', self.key)
                self.metadata['sentinel'] = (hexlify(nonce).decode('ascii'), hexlify(cipher).decode('ascii'))
                self.commit_metadata()
            else:
                nonce, cipher = unhexlify(self.metadata['sentinel'][0]), unhexlify(self.metadata['sentinel'][1])
                try:
                    decrypt_v1(cipher, nonce, self.key)
                except MessageForged:
                    raise PasswordWrong('The password is incorrect')
        except Exception as e:
            self.key_error = e

    def generate_file_name(self, key):
        if isinstance(key, str):
            key = key.encode('utf-8')
        return hashlib.sha1(key).hexdigest()

    def join(self):
        self.derive_worker.join()
        if self.key_error is not None:
            raise self.key_error

    def read_data(self, fname, key=None):
        try:
            with open(os.path.join(self.root, fname), 'rb') as f:
                version = f.read(2)
                if struct.unpack('!H', version)[0] != 1:
                    raise ValueError('Unsupported encryption version')
                nonce = f.read(nonce_size_v1())
                data = decrypt_v1(f.read(), nonce, key or self.key)
                keysize, = struct.unpack_from('!I', data)
                offset = struct.calcsize('!I')
                key = data[offset:keysize + offset].decode('utf-8')
                return key, data[keysize + offset:]
        except FileNotFoundError:
            return None, None

    def __iter__(self):
        for entry in os.scandir(self.root):
            if not entry.is_symlink() and entry.is_file(follow_symlinks=False):
                name = entry.name
                if '.' not in name and '-' not in name:
                    yield name

    # External API {{{

    def get_data(self, key):
        self.join()
        fname = self.generate_file_name(key)
        try:
            return self.read_data(fname)[1]
        except MessageForged:
            raise ValueError('The data for %s is corrupted' % key)

    def get_all_data(self):
        self.join()
        for name in self:
            try:
                key, data = self.read_data(name)
            except Exception:
                key = None
            if key is not None:
                yield key, data

    def set_data(self, key, data=None):
        self.join()
        fname = self.generate_file_name(key)
        if isinstance(key, str):
            key = key.encode('utf-8')
        if isinstance(data, str):
            data = data.encode('utf-8')
        fpath = os.path.join(self.root, fname)
        if data is None:
            try:
                os.remove(fpath)
            except FileNotFoundError:
                pass
        else:
            keysize = struct.pack('!I', len(key))
            data, nonce = encrypt_v1(keysize + key + data, self.key)
            atomic_write(fpath, struct.pack('!H', 1) + nonce + data)

    def change_password(self, new_password):
        self.join()
        old_key = self.key
        self.password = new_password
        self.metadata.pop('sentinel', None)
        self.run_derive()
        self.join()
        if self.key_error is not None:
            raise self.key_error

        for name in self:
            try:
                key, data = self.read_data(name, key=old_key)
            except Exception:
                pass
            else:
                self.set_data(key, data)
    # }}}
# }}}


def test():
    with tempfile.TemporaryDirectory() as tdir:
        p = PasswordStore('test', tdir)
        p.join()
        p.set_data('a', 'one')
        assert p.get_data('a') == b'one'
        assert tuple(p.get_all_data()) == (('a', b'one'),)
        p.change_password('pw2')
        assert tuple(p.get_all_data()) == (('a', b'one'),)


def key_from_url(url):
    u = urlparse(url)
    scheme = u.scheme.lower()
    if scheme in ('', 'file'):
        key = 'file:' + u.path
    elif scheme in ('http', 'https'):
        key = 'http:' + u.netloc
    else:
        key = scheme + ':' + u.netloc
    return key


class PasswordDB:

    def __init__(self, password, path=None):
        self.store = PasswordStore(password, path)

    def __getitem__(self, key):
        data = self.store.get_data(key)
        if data is None:
            return {'version': 1, 'accounts': []}
        return json.loads(data.decode('utf-8'))

    def __setitem__(self, key, val):
        if val is None:
            self.store.set_data(key)
        else:
            self.store.set_data(key, json.dumps(val))

    def __delitem__(self, key):
        self[key] = None

    def __iter__(self):
        for key, data in self.store.get_all_data():
            yield key

    def add_account(self, key, username, password, notes=None):
        data = self[key]
        accounts = [a for a in data['accounts'] if a['username'] != username]
        accounts.insert(0, {'username': username, 'password': password, 'notes': notes})
        data['accounts'] = accounts
        self[key] = data

    def remove_account(self, key, username):
        data = self[key]
        accounts = [a for a in data['accounts'] if a['username'] != username]
        if accounts:
            data['accounts'] = accounts
            self[key] = data
        else:
            del self[key]

    def set_accounts(self, key, accounts):
        if accounts:
            self[key] = {'version': 1, 'accounts': accounts}
        else:
            del self[key]


def import_lastpass_db(path, password_for_store):
    import csv
    db = PasswordDB(password_for_store)
    with open(path, 'r') as f:
        for i, row in enumerate(csv.reader(f)):
            if not row or i == 0:
                continue
            url, username, password, *_ = row
            key = key_from_url(url)
            db.add_account(key, username, password)
