from bit import PrivateKeyTestnet
import hashlib
import base58
from bit import Key
from bit.format import verify_sig
import hashlib

def verify_mainnet_addresses(private_key_wif, address_map):
    """
    使用 bit 库验证主网地址
    """
    try:
        # 创建主网密钥对象
        key = Key(private_key_wif)
        
        print("\n=== 主网地址验证报告 ===")
        print(f"私钥(WIF): {key.to_wif()}")
        print(f"公钥(HEX): {key.public_key.hex()}")
        
        # bit 库生成的地址
        bit_addresses = {
            'legacy': key.address,                    # 1开头
            'p2sh-segwit': key.segwit_address,       # 3开头
            'bech32': key.segwit_address             # bc1开头
        }
        
        # 验证地址
        for addr_type, original_addr in address_map.items():
            print(f"\n{addr_type.upper()} 地址验证:")
            print(f"原始地址: {original_addr}")
            print(f"Bit生成: {bit_addresses[addr_type]}")
            
            # 检查地址格式
            if addr_type == 'legacy' and not original_addr.startswith('1'):
                print("❌ Legacy地址应该以'1'开头")
            elif addr_type == 'p2sh-segwit' and not original_addr.startswith('3'):
                print("❌ P2SH-SegWit地址应该以'3'开头")
            elif addr_type == 'bech32' and not original_addr.startswith('bc1'):
                print("❌ Native SegWit地址应该以'bc1'开头")
            
            # 比较地址
            if original_addr == bit_addresses[addr_type]:
                print("✅ 地址验证通过")
            else:
                print("❌ 地址验证失败")
            
            try:
                # 查询余额（单位：satoshi）
                balance = key.get_balance()
                print(f"余额: {balance} satoshis ({balance/100000000:.8f} BTC)")
                
                # 获取交易历史
                transactions = key.get_transactions()
                print(f"交易历史数量: {len(transactions)}")
                
                # 显示最近的交易（如果有）
                if transactions:
                    print("\n最近的交易:")
                    for tx in transactions[:3]:  # 只显示最近3笔
                        print(f"交易ID: {tx}")
                
            except Exception as e:
                print(f"余额查询失败: {str(e)}")
        
        return True, "验证完成"
        
    except Exception as e:
        return False, f"验证失败: {str(e)}"

def create_mainnet_wallet():
    """
    创建新的主网钱包
    """
    # 创建新的私钥
    key = Key()
    
    return {
        'private_key': key.to_wif(),
        'address_map': {
            'legacy': key.address,
            'p2sh-segwit': key.segwit_address,
            'bech32': key.segwit_address
        }
    }

def comprehensive_address_verification(private_key_wif, address_map):
    """
    综合地址验证
    """
    try:
        # 使用 bit 库创建密钥对象
        key = PrivateKeyTestnet(private_key_wif)
        
        print("\n=== 地址验证报告 ===")
        print(f"私钥(WIF): {key.to_wif()}")
        print(f"公钥(压缩): {key.public_key.hex()}")
        
        # 验证各类地址
        addresses = {
            'legacy': key.address,
            'p2sh-segwit': key.segwit_address,
            'bech32': key.segwit_address
        }
        
        for addr_type, original_addr in address_map.items():
            print(f"\n{addr_type.upper()} 地址验证:")
            print(f"原始地址: {original_addr}")
            print(f"验证生成: {addresses[addr_type]}")
            
            # 查询余额
            balance = key.get_balance()
            print(f"余额: {balance} satoshis")
            
            # 获取交易历史
            transactions = key.get_transactions()
            print(f"交易数量: {len(transactions)}")
            
        return True, "验证完成"
        
    except Exception as e:
        return False, f"验证失败: {str(e)}"

# 使用示例
if __name__ == "__main__":
    # 假设这是你之前生成的钱包信息
    wallet = {
        'private_key': 'your_private_key_wif',
        'address_map': {
            'legacy': 'your_legacy_address',
            'p2sh-segwit': 'your_p2sh_address',
            'bech32': 'your_bech32_address'
        }
    }
    
    success, message = comprehensive_address_verification(
        wallet['private_key'],
        wallet['address_map']
    )
    
    print(f"\n验证结果: {message}")


    # 1. 创建新钱包
    print("\n=== 创建新的主网钱包 ===")
    wallet = create_mainnet_wallet()
    
    print("\n私钥(WIF):", wallet['private_key'])
    print("\n地址:")
    for addr_type, address in wallet['address_map'].items():
        print(f"{addr_type}: {address}")
    
    # 2. 验证钱包
    print("\n=== 验证钱包 ===")
    success, message = verify_mainnet_addresses(
        wallet['private_key'],
        wallet['address_map']
    )
    
    print(f"\n最终验证结果: {message}")
    
    # 3. 显示导入说明
    print("\n=== 导入说明 ===")
    print("您可以将这些地址导入任何比特币钱包:")
    print("- Legacy地址用于最大兼容性")
    print("- P2SH-SegWit地址用于较低费用")
    print("- Native SegWit (Bech32)地址用于最低费用")
    print("\n请务必安全保存私钥！")