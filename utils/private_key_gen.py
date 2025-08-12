import os
import hashlib
import ecdsa
import base58
import requests
import bech32
import secrets  # 更安全的随机数生成

def gen_private_key_wif(network='test'):
    """
    生成比特币私钥 (WIF格式)
    
    Args:
        network (str): 'test' 为测试网络, 'main' 为主网络
        
    Returns:
        dict: 包含私钥信息的字典
    """
    # 使用更安全的随机数生成器
    private_key_bytes = secrets.randbits(256).to_bytes(32, byteorder='big')
    
    # 确保私钥在有效范围内 (1 到 n-1，其中n是secp256k1的阶)
    secp256k1_order = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
    private_key_int = int.from_bytes(private_key_bytes, byteorder='big')
    
    # 如果私钥超出范围，重新生成（极小概率事件）
    while private_key_int == 0 or private_key_int >= secp256k1_order:
        private_key_bytes = secrets.randbits(256).to_bytes(32, byteorder='big')
        private_key_int = int.from_bytes(private_key_bytes, byteorder='big')
    
    private_key_wif = __create_wif(private_key_bytes, network)
    
    return {
        'private_key_wif': private_key_wif,
        'private_key_bytes': private_key_bytes
    }

def __create_wif(private_key_bytes, network='test'):
    """
    创建WIF格式的私钥
    
    Args:
        private_key_bytes (bytes): 32字节私钥
        network (str): 网络类型
        
    Returns:
        str: WIF格式的私钥
    """
    if len(private_key_bytes) != 32:
        raise ValueError("私钥必须是32字节")
        
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