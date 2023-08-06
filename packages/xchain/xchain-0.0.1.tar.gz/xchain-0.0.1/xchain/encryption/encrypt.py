import json
import copy

from .crypto import encrypt, decrypt, sign, verify


def issuer_signup(_entries, key_path):
    _tmp_entries = copy.deepcopy(_entries)
    for _entry in _tmp_entries:
        _entry['signature'] = sign(str(_entry['listing']), key_path)
    return _tmp_entries


def encrypt_entries(_entries, enc_key):
    _tmp_entries = copy.deepcopy(_entries)
    for _entry in _tmp_entries:
        _entry['listing'] = encrypt(str(_entry['listing']), enc_key).decode('utf-8')
    return _tmp_entries


def issuer_verify(_entries, ver_key):
    _tmp_entries = copy.deepcopy(_entries)
    for _entry in _tmp_entries:
        verify(str(_entry['listing']), _entry['signature'], ver_key)
    return _tmp_entries


def decrypt_entries(_entries, dec_key):
    _tmp_entries = copy.deepcopy(_entries)
    for _entry in _tmp_entries:
        deced = decrypt(str(_entry['listing']), dec_key).decode('utf-8')
        deced = json.loads(deced.replace("'", "\""))
        _entry['listing'] = deced
    return _tmp_entries
