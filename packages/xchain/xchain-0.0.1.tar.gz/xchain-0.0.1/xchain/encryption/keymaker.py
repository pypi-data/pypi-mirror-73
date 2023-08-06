from Crypto.PublicKey import RSA


def generate_key(path):
    key = RSA.generate(4096)
    f = open(f'{path}/key.pem', 'wb')
    f.write(key.exportKey('PEM'))
    f.close()


# #Read key from file
# f = open('keyfile.pem', 'rb')
# key = RSA.importKey(f.read())
