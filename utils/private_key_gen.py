import os

def gen_private_key():
    return int.from_bytes(os.urandom(32), byteorder='big')