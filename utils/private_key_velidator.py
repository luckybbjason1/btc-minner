from bit import PrivateKeyTestnet
import hashlib
import base58
from bit import Key
from bit.format import verify_sig
import hashlib
from private_key_gen import gen_private_key_wif
from wallet_gen_bit import gen_addresses
from wallet_generator import generate_bitcoin_address

def verify_addresses(address_map, address_map_by_bit, network='test'):
    """
    使用 bit 库验证主网地址
    """
    try:
        for addr_type, original_addr in address_map.items():
            print(f"\n{addr_type.upper()} 地址验证:")
            print(f"原始地址: {original_addr}")
            print(f"Bit生成: {address_map_by_bit[addr_type]}")
            
            # 比较地址
            if original_addr == address_map_by_bit[addr_type]:
                print("✅ 地址验证通过")
            else:
                print("❌ 地址验证失败")        
        return True, "验证完成"
        
    except Exception as e:
        return False, f"验证失败: {str(e)}"

# 使用示例
if __name__ == "__main__":

    private_key = gen_private_key_wif()
    print(private_key)
    address_map_by_bit = gen_addresses(private_key['private_key_wif'])
    address_map_by_self = generate_bitcoin_address(private_key['private_key_bytes'])
    print(address_map_by_bit)
    print(address_map_by_self)
