#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2015, Kovid Goyal <kovid at kovidgoyal.net>

import json
import os
import hashlib
import struct
from threading import Thread

from .crypto import derive_key_v1, generate_salt_v1, nonce_size_v1, decrypt_v1, encrypt_v1, lock_python_bytes
from .utils import atomic_write


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
                'salt': generate_salt_v1()
            }
            self.commit_metadata()
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
            self.key = derive_key_v1(pw, self.metadata['salt'])[0]
        except Exception as e:
            self.key_error = e

    def generate_file_name(self, key):
        if isinstance(key, str):
            key = key.encode('utf-8')
        return hashlib.sha1(key).hexdigest()

    def get_data(self, key):
        self.derive_worker.join()
        if self.key_error is not None:
            raise self.key_error
        fname = self.generate_file_name(key)
        return self.read_data(fname)[1]

    def get_all_data(self):
        self.derive_worker.join()
        if self.key_error is not None:
            raise self.key_error
        for name in os.listdir(self.root):
            if '.' in name:
                continue
            key, data = self.read_data(name)
            if key is not None:
                yield key, data

    def set_data(self, key, data):
        self.derive_worker.join()
        if self.key_error is not None:
            raise self.key_error
        fname = self.generate_file_name(key)
        if isinstance(key, str):
            key = key.encode('utf-8')
        if isinstance(data, str):
            data = data.encode('utf-8')
        data, nonce = encrypt_v1(key + data, self.key)
        with open(os.path.join(self.root, fname), 'wb') as f:
            f.write(nonce), f.write(data)

    def read_data(self, fname):
        try:
            with open(os.path.join(self.root, fname), 'wb') as f:
                nonce = f.read(nonce_size_v1())
                data = memoryview(decrypt_v1(f.read(), nonce, self.key))
                keysize, = struct.unpack_from('!I', data)
                key = data[:keysize].decode('utf-8')
                return key, data[keysize + struct.calcsize('!I'):]
        except FileNotFoundError:
            return None, None
