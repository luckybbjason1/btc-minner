import hashlib
import ecdsa
import base58
from numba import cuda
import numpy as np

@cuda.jit
def generate_address(private_keys, addresses):
    idx = cuda.grid(1)
    if idx < private_keys.shape[0]:
        # 生成公钥
        k = ecdsa.SigningKey.from_string(private_keys[idx], curve=ecdsa.SECP256k1)
        pub = k.get_verifying_key().to_string()
        
        # 计算SHA256和RIPEMD160哈希
        ripemd160 = hashlib.new('ripemd160')
        ripemd160.update(hashlib.sha256(pub).digest())
        hash160 = ripemd160.digest()
        
        # 添加版本号
        version = b'\x00'
        hash160_with_version = version + hash160
        
        # 计算校验和
        double_sha256 = hashlib.sha256(hashlib.sha256(hash160_with_version).digest()).digest()
        checksum = double_sha256[:4]
        
        # 生成最终地址
        binary_addr = hash160_with_version + checksum
        addresses[idx] = base58.b58encode(binary_addr)

# 生成随机私钥
num_addresses = 1000000
private_keys = np.random.bytes(32, (num_addresses,))
addresses = np.empty(num_addresses, dtype=np.object)

# 配置GPU
threadsperblock = 256
blockspergrid = (num_addresses + (threadsperblock - 1)) // threadsperblock

# 在GPU上运行
generate_address[blockspergrid, threadsperblock](private_keys, addresses)