import hashlib
import ecdsa
import base58
import requests
import bech32
import os
from utils.balance_check import get_balance
from utils.wallet_generator import generate_bitcoin_address
from utils.private_key_velidator import verify_private_key

address_types = ['legacy', 'p2sh-segwit', 'bech32']

# 使用示例
def main_network():
    wallet = generate_bitcoin_address('main')
    print("比特币地址:", wallet['address_map'])
    print("私钥(WIF格式):", wallet['private_key'])
    print("公钥:", wallet['public_key'])
    address_map = wallet['address_map']
    # is_valid, message = verify_private_key(wallet['private_key'], wallet['address_map'])
    # print(f"\n私钥验证结果: {message}")
    for address_type, address in address_map.items():
        balance = get_balance(address, 'main')
        print(f"地址 {address} 的余额为: {balance} BTC")

# 修改主函数的测试代码
def test_network():
    # 生成测试网络地址
    wallet = generate_bitcoin_address()
    
    print("\n=== 测试网络比特币钱包 ===")
    print("比特币地址:", wallet['address_map'])
    print("私钥(WIF格式):", wallet['private_key'])
    print("公钥:", wallet['public_key'])
    address_map = wallet['address_map']
    
    # 验证私钥
    # is_valid, message = verify_private_key(wallet['private_key'], wallet['address_map'])
    # print(f"\n私钥验证结果: {message}")

    # 查询每个地址的余额
    for address_type, address in address_map.items():
        balance = get_balance(address, 'test')
        print(f"地址 {address} 的余额为: {balance} BTC")

if __name__ == "__main__":
    print("")
    # main_network()
    test_network()