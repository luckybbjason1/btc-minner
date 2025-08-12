import hashlib
import ecdsa
import base58
import requests
import bech32
import os
from utils.balance_check import get_balance
from utils.wallet_generator import generate_bitcoin_address
from utils.wallet_gen_bit import gen_addresses
from utils.private_key_gen import gen_private_key_wif

address_types = ['legacy', 'p2sh-segwit', 'bech32']

def print_security_warning():
    """打印安全警告"""
    print("=" * 60)
    print("🔒 安全警告 / SECURITY WARNING")
    print("=" * 60)
    print("⚠️  私钥是您比特币资产的唯一凭证!")
    print("⚠️  请务必安全保存私钥，不要泄露给他人!")
    print("⚠️  建议在离线环境中生成和使用私钥!")
    print("⚠️  本工具仅供学习和测试用途!")
    print("=" * 60)
    print()

# 使用示例
def get_wallet(network='test'):
    """
    生成比特币钱包并检查余额
    
    Args:
        network (str): 'test' 为测试网络, 'main' 为主网络
    """
    try:
        print_security_warning()
        
        print(f"正在生成 {network} 网络钱包...")
        
        # 生成私钥
        private_key = gen_private_key_wif(network)
        
        # 生成地址
        res = gen_addresses(private_key['private_key_wif'], network)
        
        print("✅ 钱包生成成功!")
        print(f"比特币地址: {res['address']}")
        print(f"私钥(WIF格式): {res['private_key']}")
        print(f"公钥: {res['public_key']}")
        
        address_map = res['address']
        
        print("\n正在检查地址余额...")
        successful_checks = 0
        total_balance = 0
        
        for address_type, address in address_map.items():
            try:
                balance = get_balance(address, network)
                total_balance += balance
                successful_checks += 1
                
                if balance > 0:
                    print(f"✅ {address_type} 地址 {address} 的余额: {balance} 聪 💰")
                else:
                    print(f"💼 {address_type} 地址 {address} 的余额: {balance} 聪")
                    
            except Exception as e:
                print(f"❌ {address_type} 地址 {address} 余额查询失败: {str(e)}")
        
        print(f"\n📊 余额检查完成: {successful_checks}/{len(address_map)} 个地址检查成功")
        if total_balance > 0:
            print(f"🎉 总余额: {total_balance} 聪")
        
        return {
            'addresses': address_map,
            'private_key': res['private_key'],
            'public_key': res['public_key'],
            'total_balance': total_balance
        }
        
    except Exception as e:
        print(f"❌ 钱包生成或余额查询出错: {str(e)}")
        return None

if __name__ == "__main__":
    try:
        print("🚀 比特币钱包生成器")
        print("选择网络:")
        print("1. 测试网络 (testnet)")
        print("2. 主网络 (mainnet) - 请谨慎使用")
        
        choice = input("请选择 (1/2，默认为1): ").strip()
        
        if choice == '2':
            confirm = input("⚠️  您选择了主网络，这将生成真实的比特币地址。确定吗？(y/N): ").strip().lower()
            if confirm == 'y':
                network = 'main'
            else:
                print("已取消，使用测试网络")
                network = 'test'
        else:
            network = 'test'
        
        wallet = get_wallet(network)
        
        if wallet and wallet['total_balance'] > 0:
            print("\n🎉 恭喜！发现有余额的钱包！")
            print("请立即安全保存您的私钥！")
        
    except KeyboardInterrupt:
        print("\n\n程序被用户中断")
    except Exception as e:
        print(f"\n程序运行出错: {e}")
