from eth_account import Account
import secrets
from typing import Tuple

def generate_eth_wallet() -> Tuple[str, str]:
    """
    生成一个新的ETH钱包
    
    Returns:
        Tuple[str, str]: (私钥的十六进制字符串, 钱包地址)
    """
    # 生成一个安全的随机私钥
    private_key = secrets.token_hex(32)
    
    # 从私钥创建账户
    account = Account.from_key(private_key)
    
    # 返回私钥和地址
    return private_key, account.address

def generate_multiple_wallets(count: int) -> list[Tuple[str, str]]:
    """
    生成多个ETH钱包
    
    Args:
        count: 要生成的钱包数量
        
    Returns:
        list[Tuple[str, str]]: 包含(私钥, 地址)元组的列表
    """
    return [generate_eth_wallet() for _ in range(count)]

if __name__ == "__main__":
    # 示例：生成一个钱包
    private_key, address = generate_eth_wallet()
    print(f"生成的ETH钱包：")
    print(f"私钥: {private_key}")
    print(f"地址: {address}")
    
    # 示例：生成多个钱包
    wallets = generate_multiple_wallets(3)
    print("\n批量生成的钱包：")
    for i, (pk, addr) in enumerate(wallets, 1):
        print(f"\n钱包 {i}:")
        print(f"私钥: {pk}")
        print(f"地址: {addr}")
