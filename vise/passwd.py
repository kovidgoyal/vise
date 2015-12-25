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

from .crypto import derive_key_v1, generate_salt_v1, nonce_size_v1, decrypt_v1, encrypt_v1, lock_python_bytes, MessageForged
from .utils import atomic_write


class PasswordWrong(ValueError):
    pass


class PasswordStore:

    def __init__(self, dirpath, password):
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
                self.metadata = json.load(f)
        except FileNotFoundError:
            self.metadata = {
                'version': 1,
                'salt': hexlify(generate_salt_v1()).decode('ascii')
            }
        self.key = self.key_error = None
        self.password = password
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

    def get_data(self, key):
        self.join()
        fname = self.generate_file_name(key)
        try:
            return self.read_data(fname)[1]
        except MessageForged:
            raise ValueError('The data for %s is corrupted' % key)

    def __iter__(self):
        for entry in os.scandir(self.root):
            if not entry.is_symlink() and entry.is_file(follow_symlinks=False):
                name = entry.name
                if '.' not in name and '-' not in name:
                    yield name

    def get_all_data(self):
        self.join()
        for name in self:
            try:
                key, data = self.read_data(name)
            except Exception:
                key = None
            if key is not None:
                yield key, data

    def set_data(self, key, data):
        self.join()
        fname = self.generate_file_name(key)
        if isinstance(key, str):
            key = key.encode('utf-8')
        if isinstance(data, str):
            data = data.encode('utf-8')
        keysize = struct.pack('!I', len(key))
        data, nonce = encrypt_v1(keysize + key + data, self.key)
        atomic_write(os.path.join(self.root, fname), nonce + data)

    def read_data(self, fname):
        try:
            with open(os.path.join(self.root, fname), 'rb') as f:
                nonce = f.read(nonce_size_v1())
                data = decrypt_v1(f.read(), nonce, self.key)
                keysize, = struct.unpack_from('!I', data)
                offset = struct.calcsize('!I')
                key = data[offset:keysize + offset].decode('utf-8')
                return key, data[keysize + offset:]
        except FileNotFoundError:
            return None, None


def test():
    with tempfile.TemporaryDirectory() as tdir:
        p = PasswordStore(tdir, 'test')
        p.join()
        p.set_data('a', 'one')
        assert p.get_data('a') == b'one'
        assert tuple(p.get_all_data()) == (('a', b'one'),)
