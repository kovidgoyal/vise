#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2015, Kovid Goyal <kovid at kovidgoyal.net>

from threading import Lock
from ctypes import (
    c_int, CFUNCTYPE, CDLL, c_ubyte, POINTER, c_ulonglong, c_char_p, c_size_t,
    c_void_p, create_string_buffer, cast)
libsodium = CDLL('libsodium.so')
INPUT = 1
OUTPUT = 2
INPUTZ = 4
c_ubyte_p = POINTER(c_ubyte)


def arg(name, atype, default=None, io=INPUT):
    return {'type': atype, 'name': name, 'default': default, 'io': io}


def bind(name, restype, *args):
    typsig = tuple(x['type'] for x in args)
    flags = tuple((x['io'], x['name'], x['default']) for x in args)
    return CFUNCTYPE(restype, *typsig)((name, libsodium), flags)

sodium_init = bind('sodium_init', c_int)
init_lock = Lock()
with init_lock:
    if sodium_init() == -1:
        raise RuntimeError('sodium_init() failed')

try:
    crypto_aead_aes256gcm_is_available = bind('crypto_aead_aes256gcm_is_available', c_int)
except AttributeError:
    def crypto_aead_aes256gcm_is_available():
        return 0

crypto_pwhash_scryptsalsa208sha256_opslimit_interactive = bind(
    'crypto_pwhash_scryptsalsa208sha256_opslimit_interactive', c_size_t)

crypto_pwhash_scryptsalsa208sha256_opslimit_sensitive = bind(
    'crypto_pwhash_scryptsalsa208sha256_opslimit_sensitive', c_size_t)

crypto_pwhash_scryptsalsa208sha256_memlimit_interactive = bind(
    'crypto_pwhash_scryptsalsa208sha256_memlimit_interactive', c_size_t)

crypto_pwhash_scryptsalsa208sha256_memlimit_sensitive = bind(
    'crypto_pwhash_scryptsalsa208sha256_memlimit_sensitive', c_size_t)

crypto_pwhash_scryptsalsa208sha256_saltbytes = bind(
    'crypto_pwhash_scryptsalsa208sha256_saltbytes', c_size_t)

randombytes_buf = bind(
    'randombytes_buf', None,
    arg('buf', c_void_p),
    arg('size', c_size_t, default=crypto_pwhash_scryptsalsa208sha256_saltbytes())
)

crypto_box_seedbytes = bind('crypto_box_seedbytes', c_size_t)
crypto_secretbox_keybytes = bind('crypto_secretbox_keybytes', c_size_t)
crypto_secretbox_macbytes = bind('crypto_secretbox_macbytes', c_size_t)
crypto_secretbox_noncebytes = bind('crypto_secretbox_noncebytes', c_size_t)
crypto_secretbox_primitive = bind('crypto_secretbox_primitive', c_char_p)

crypto_pwhash_scryptsalsa208sha256 = bind(
    'crypto_pwhash_scryptsalsa208sha256', c_int,
    arg('out', c_ubyte_p),
    arg('outlen', c_ulonglong),
    arg('passwd', c_char_p),
    arg('pwlen', c_ulonglong),
    arg('salt', c_ubyte_p),
    arg('opslimit', c_ulonglong, default=crypto_pwhash_scryptsalsa208sha256_opslimit_interactive()),
    arg('memlimit', c_size_t, default=crypto_pwhash_scryptsalsa208sha256_memlimit_interactive())
)

crypto_secretbox_easy = bind(
    'crypto_secretbox_easy', c_int,
    arg('out', c_ubyte_p),
    arg('message', c_ubyte_p),
    arg('mlen', c_ulonglong),
    arg('nonce', c_ubyte_p),
    arg('key', c_ubyte_p)
)

crypto_secretbox_open_easy = bind(
    'crypto_secretbox_open_easy', c_int,
    arg('message', c_ubyte_p),
    arg('ciphertext', c_ubyte_p),
    arg('ciphertext_len', c_ulonglong),
    arg('nonce', c_ubyte_p),
    arg('key', c_ubyte_p)
)

sodium_mlock = bind(
    'sodium_mlock', c_int,
    arg('addr', c_void_p),
    arg('len', c_size_t)
)


def random_bytes(num):
    x = create_string_buffer(num)
    randombytes_buf(x, num)
    return x.raw


def generate_salt_v1():
    return random_bytes(crypto_pwhash_scryptsalsa208sha256_saltbytes())


def lock_python_bytes(data):
    if sodium_mlock(cast(data, c_void_p), len(data)) != 0:
        raise RuntimeError('Failed to lock memory')


def derive_key_v1(passwd, salt=None):
    key_len = crypto_secretbox_keybytes()
    if key_len != 32:
        raise RuntimeError('secretbox key length has changed')
    if salt is None:
        salt = generate_salt_v1()
    if not isinstance(passwd, bytes):
        passwd = passwd.encode('utf-8')
    out = create_string_buffer(key_len)
    sbuf = cast(salt, c_ubyte_p)
    if crypto_pwhash_scryptsalsa208sha256(
            cast(out, c_ubyte_p), key_len, passwd, len(passwd), sbuf,
            crypto_pwhash_scryptsalsa208sha256_opslimit_sensitive(), crypto_pwhash_scryptsalsa208sha256_memlimit_sensitive()) != 0:
        raise MemoryError('Out of memory deriving key from password')
    key = out.raw
    lock_python_bytes(key)
    return key, salt


def nonce_size_v1():
    return crypto_secretbox_noncebytes()


def encrypt_v1(data, key):
    if crypto_secretbox_primitive() != b'xsalsa20poly1305':
        raise RuntimeError('libsodium cryptobox primitive has changed')
    if not isinstance(data, bytes):
        data = data.encode('utf-8')
    nonce = create_string_buffer(nonce_size_v1())
    randombytes_buf(nonce, nonce_size_v1())
    ciphertext_len = len(data) + crypto_secretbox_macbytes()
    ciphertext = create_string_buffer(ciphertext_len)
    crypto_secretbox_easy(cast(ciphertext, c_ubyte_p), cast(data, c_ubyte_p), len(data), cast(nonce, c_ubyte_p), cast(key, c_ubyte_p))
    return ciphertext.raw, nonce.raw


class MessageForged(ValueError):
    pass


def decrypt_v1(encrypted_data, nonce, key):
    if crypto_secretbox_primitive() != b'xsalsa20poly1305':
        raise RuntimeError('libsodium cryptobox primitive has changed')
    ans = create_string_buffer(len(encrypted_data) - crypto_secretbox_macbytes())
    if crypto_secretbox_open_easy(cast(ans, c_ubyte_p), cast(encrypted_data, c_ubyte_p), len(encrypted_data),
                                  cast(nonce, c_ubyte_p), cast(key, c_ubyte_p)) != 0:
        raise MessageForged('Message forged!')
    return ans.raw


def test():
    passwd = 'testpw'
    key, salt = derive_key_v1(passwd)
    assert derive_key_v1(passwd, salt) == (key, salt)
    data = b'testing'
    encrypted, nonce = encrypt_v1(data, key)
    assert decrypt_v1(encrypted, nonce, key) == data
    bad_data = bytes(bytearray(reversed(encrypted)))
    try:
        decrypt_v1(bad_data, nonce, key)
        raise AssertionError('Bad data was decrypted!')
    except MessageForged:
        pass

if __name__ == '__main__':
    test()
