import base64
from Crypto.Cipher import AES

from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA


def encrypt(entry, key):
    msg_text = entry.ljust(64)
    cipher = AES.new(key, AES.MODE_ECB)
    encoded = base64.b64encode(cipher.encrypt(msg_text))
    return encoded


def decrypt(entry, key):
    cipher = AES.new(key, AES.MODE_ECB)
    decoded = cipher.decrypt(base64.b64decode(entry))
    return decoded.strip()


def sign(text, key_path):

    digest = SHA256.new()
    digest.update(text.encode())

    # Read shared key from file
    with open(key_path, "r") as key:
        key = key.read()
        private_key = RSA.importKey(key)

    # Load private key and sign message
    signer = PKCS1_v1_5.new(private_key)

    return signer.sign(digest)


def verify(text, signature, key_path):

    digest = SHA256.new()
    digest.update(text.encode())

    # Load public key and verify message
    with open(key_path, "r") as myfile:
        public_key = RSA.importKey(myfile.read())
    verifier = PKCS1_v1_5.new(public_key)
    verified = verifier.verify(digest, signature)
    assert verified, 'Signature verification failed'


