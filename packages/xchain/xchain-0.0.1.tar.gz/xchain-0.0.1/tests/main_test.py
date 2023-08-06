import pytest
from os import path, remove

from xchain.xchain import Blockchain
from xchain.encryption.crypto import encrypt, decrypt, sign, verify
from xchain.encryption.encrypt import issuer_signup, encrypt_entries, issuer_verify, decrypt_entries
from xchain.encryption.keymaker import generate_key

from tests.entries import entries


# ======= TEST FIXTURES ========


@pytest.fixture()
def blockchain():
    blockchain = Blockchain()
    return blockchain


@pytest.fixture()
def enc_key():
    return b'1234567890123456'


@pytest.fixture(scope="module")
def rsa_key():
    current_dir = path.dirname(path.abspath(__file__))
    generate_key(path.dirname(path.abspath(__file__)))
    yield f'{current_dir}/key.pem'
    remove(f'{current_dir}/key.pem')


# ========= TEST CASES =========


def test_base_chain(blockchain):
    assert len(blockchain.chain) == 1


def test_mine_block(blockchain):
    blockchain.mine_block(entries)
    assert len(blockchain.chain) == 2
    assert len(blockchain.chain[1]['entries']) == len(entries)


def test_encryption(enc_key):
    plain_text = 'text to encrypt'
    encrypted = encrypt(plain_text, enc_key)
    decrypted = decrypt(encrypted, enc_key).decode('utf-8')
    assert plain_text == decrypted


def test_entries_encryption(enc_key):
    encrypted_entries = encrypt_entries(entries, enc_key)
    decrypted_entries = decrypt_entries(encrypted_entries, enc_key)
    for i, _entry in enumerate(entries):
        assert _entry['listing'] == decrypted_entries[i]['listing']


def test_signing(rsa_key):
    plain_text = 'text to encrypt'
    signature = sign(plain_text, rsa_key)
    verify(plain_text, signature, rsa_key)


def test_entries_signing(rsa_key):
    signed_entries = issuer_signup(entries, rsa_key)
    issuer_verify(signed_entries, rsa_key)


def test_block_encryption(blockchain, enc_key):
    encrypted_entries = encrypt_entries(entries, enc_key)
    blockchain.mine_block(encrypted_entries)
    chain_entries = blockchain.chain[1]['entries']
    decrypted_entries = decrypt_entries(chain_entries, enc_key)
    for i, _entry in enumerate(entries):
        assert _entry['listing'] == decrypted_entries[i]['listing']


def test_block_signing(blockchain, rsa_key):
    signed_entries = issuer_signup(entries, rsa_key)
    blockchain.mine_block(signed_entries)
    chain_entries = blockchain.chain[1]['entries']
    issuer_verify(chain_entries, rsa_key)


def test_block_total_security(blockchain, enc_key, rsa_key):
    signed_entries = issuer_signup(entries, rsa_key)
    encrypted_entries = encrypt_entries(signed_entries, enc_key)
    blockchain.mine_block(encrypted_entries)
    chain_entries = blockchain.chain[1]['entries']
    decrypted_entries = decrypt_entries(chain_entries, enc_key)
    for i, _entry in enumerate(entries):
        assert _entry['listing'] == decrypted_entries[i]['listing']
    issuer_verify(decrypted_entries, rsa_key)
