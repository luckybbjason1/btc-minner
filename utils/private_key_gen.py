import os
import hashlib
import ecdsa
import base58
import requests
import bech32
import os

def gen_private_key_wif():
    private_key = int.from_bytes(os.urandom(32), byteorder='big')
    private_key_bytes = private_key.to_bytes(32, byteorder='big')
    private_key_wif = __create_wif(private_key_bytes)
    dic = {
        # 'private_key': private_key,
        'private_key_wif': private_key_wif,
        # 'private_key_hex': private_key_bytes.hex(),
        'private_key_bytes': private_key_bytes
    }
    return dic

def __create_wif(private_key_bytes, network='test'):
    # 添加版本号前缀(0x80表示私钥)
    version = b'\xef' if network == 'test' else b'\x80'  # 测试网络使用0xef
    version_key = version + private_key_bytes
    
    # 计算校验和
    double_sha256 = hashlib.sha256(hashlib.sha256(version_key).digest()).digest()
    checksum = double_sha256[:4]
    
    # 组合并Base58编码
    wif = base58.b58encode(version_key + checksum).decode()
    return wif


if __name__ == "__main__":
    print(gen_private_key_wif())