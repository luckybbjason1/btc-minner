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

# 使用示例
def get_wallet(network='test'):
    private_key = gen_private_key_wif()
    res = gen_addresses(private_key['private_key_wif'], network)
    # wallet = generate_bitcoin_address(private_key['private_key_bytes'])
    print("比特币地址:", res['address'])
    print("私钥(WIF格式):", res['private_key'])
    print("公钥:", res['public_key'])
    address_map = res['address']
    # is_valid, message = verify_private_key(wallet['private_key'], wallet['address_map'])
    # print(f"\n私钥验证结果: {message}")
    for address_type, address in address_map.items():
        balance = get_balance(address, 'main')
        print(f"地址 {address} 的余额为: {balance} BTC")

if __name__ == "__main__":
    print("")
    get_wallet('main')
    # test_network()
