import hashlib
import ecdsa
import base58
import requests
import multiprocessing
from multiprocessing import Pool
import time

def generate_addresses_multicore(num_addresses):
    """多核并行生成比特币地址"""
    # 获取CPU核心数
    cpu_count = multiprocessing.cpu_count()
    # 创建进程池
    with Pool(processes=cpu_count) as pool:
        # 并行生成地址
        wallets = pool.map(lambda x: generate_single_address(), range(num_addresses))
    return wallets

def check_balance_multicore(wallets, batch_size=10):
    """多核并行检查余额"""
    def check_wallet_batch(wallet_batch):
        results = []
        for wallet in wallet_batch:
            try:
                balance = get_balance(wallet['address'])
                results.append({
                    'address': wallet['address'],
                    'balance': balance,
                    'private_key': wallet['private_key']
                })
            except Exception as e:
                print(f"检查地址时出错: {e}")
        return results

    # 将钱包分成多个批次
    wallet_batches = [wallets[i:i + batch_size] for i in range(0, len(wallets), batch_size)]
    
    # 使用进程池并行处理
    with Pool(processes=multiprocessing.cpu_count()) as pool:
        results = pool.map(check_wallet_batch, wallet_batches)
    
    # 合并结果
    flat_results = [item for batch in results for item in batch]
    return flat_results

if __name__ == "__main__":
    # 设置要生成的地址数量
    num_addresses = 100
    
    # 记录开始时间
    start_time = time.time()
    
    print(f"使用 {multiprocessing.cpu_count()} 个CPU核心生成 {num_addresses} 个比特币地址...")
    
    # 生成地址
    wallets = generate_addresses_multicore(num_addresses)
    
    # 计算生成地址所需时间
    generation_time = time.time() - start_time
    print(f"地址生成完成，耗时: {generation_time:.2f} 秒")
    
    # 检查余额
    print("开始检查地址余额...")
    results = check_balance_multicore(wallets)
    
    # 计算总耗时
    total_time = time.time() - start_time
    
    # 打印结果
    print(f"\n生成并检查了 {num_addresses} 个地址，总耗时: {total_time:.2f} 秒")
    print("\n示例结果（前5个地址）:")
    for wallet in results[:5]:
        print(f"\n地址: {wallet['address']}")
        print(f"余额: {wallet['balance']} BTC")
        print(f"私钥: {wallet['private_key']}")
    
    # 打印有余额的地址（如果有的话）
    non_zero_wallets = [w for w in results if w['balance'] > 0]
    if non_zero_wallets:
        print("\n发现有余额的地址:")
        for wallet in non_zero_wallets:
            print(f"地址: {wallet['address']}")
            print(f"余额: {wallet['balance']} BTC")
            print(f"私钥: {wallet['private_key']}")