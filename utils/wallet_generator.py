import hashlib
import ecdsa
import base58
import requests
import bech32
import os

address_types = ['legacy', 'p2sh-segwit', 'bech32']

def genLegacyP2PKH(ripemd160_hash, network='test'):
    version = b'\x6f' if network == 'test' else b'\x00'  # 测试网络使用0x6f
    version_ripemd160_hash = version + ripemd160_hash
    double_sha256 = hashlib.sha256(hashlib.sha256(version_ripemd160_hash).digest()).digest()
    checksum = double_sha256[:4]
    binary_address = version_ripemd160_hash + checksum
    address = base58.b58encode(binary_address).decode()
    return address

def genP2SHSegWit(ripemd160_hash, network='test'):
    keyhash = ripemd160_hash
    redeemscript = b'\x00\x14' + keyhash
    script_hash = hashlib.new('ripemd160', hashlib.sha256(redeemscript).digest()).digest()
    version = b'\xc4' if network == 'test' else b'\x05'
    version_script_hash = version + script_hash
    double_sha256 = hashlib.sha256(hashlib.sha256(version_script_hash).digest()).digest()
    checksum = double_sha256[:4]
    binary_address = version_script_hash + checksum
    address = base58.b58encode(binary_address).decode()
    return address

def genNativeSegWit(ripemd160_hash, network='test'):
    witprog = ripemd160_hash
    hrp = 'tb' if network == 'test' else 'bc'  # 测试网络使用'tb'前缀
    address = bech32.encode(hrp, 0, witprog)
    return address

def generate_bitcoin_address(private_key_bytes, network='test'):
    """
    生成比特币地址
    address_type: 'legacy' (P2PKH), 'p2sh-segwit' (P2SH-SegWit), 或 'bech32' (Native SegWit)
    """
    # ... 保持现有私钥和公钥生成代码不变直到 ripemd160_hash ...
    # 生成私钥 (32字节随机数)
    
    # 生成公钥
    signing_key = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1)
    verifying_key = signing_key.get_verifying_key()
    public_key_bytes = verifying_key.to_string()
    public_key_hex = verifying_key.to_string().hex()
    
    # 添加前缀 0x04 (未压缩公钥)
    public_key_bytes = b'\x04' + public_key_bytes
    
    # 计算 RIPEMD160(SHA256(public_key))
    sha256_hash = hashlib.sha256(public_key_bytes).digest()
    ripemd160_hash = hashlib.new('ripemd160', sha256_hash).digest()
    
    address_map = {}
    for address_type in address_types:
        if address_type == 'legacy':
            # Legacy P2PKH 地址 (1开头)
            address = genLegacyP2PKH(ripemd160_hash, network)
            address_map[address_type] = address

        elif address_type == 'p2sh-segwit':
            # P2SH-SegWit 地址 (3开头)
            address = genP2SHSegWit(ripemd160_hash, network)
            address_map[address_type] = address

        elif address_type == 'bech32':
            # Native SegWit 地址 (bc1开头)
            address = genNativeSegWit(ripemd160_hash, network)
            address_map[address_type] = address
        else:
            raise ValueError("不支持的地址类型")

    return {
        # 'private_key': private_key_wif,
        'public_key': public_key_hex,
        'address_map': address_map
    }
