import hashlib
import ecdsa
import base58
import requests
import multiprocessing
from multiprocessing import Pool
import time
import os
from utils.wallet_generator import generate_bitcoin_address
from utils.balance_check import get_balance
from utils.private_key_gen import gen_private_key_wif

def generate_single_address():
    """生成单个比特币地址和私钥"""
    try:
        # 生成私钥
        private_key_data = gen_private_key_wif('test')  # 默认使用测试网络
        
        # 生成地址
        wallet = generate_bitcoin_address(private_key_data['private_key_bytes'])
        
        return {
            'private_key': private_key_data['private_key_wif'],
            'address': wallet['address_map']['legacy'],  # 使用legacy地址
            'public_key': wallet['public_key']
        }
    except Exception as e:
        print(f"生成地址时出错: {e}")
        return None

def generate_addresses_multicore(num_addresses):
    """多核并行生成比特币地址"""
    # 获取CPU核心数
    cpu_count = multiprocessing.cpu_count()
    # 创建进程池
    with Pool(processes=cpu_count) as pool:
        # 并行生成地址，过滤掉None结果
        wallets = [w for w in pool.map(lambda x: generate_single_address(), range(num_addresses)) if w is not None]
    return wallets

def check_balance_multicore(wallets, batch_size=10):
    """多核并行检查余额"""
    def check_wallet_batch(wallet_batch):
        results = []
        for wallet in wallet_batch:
            try:
                balance = get_balance(wallet['address'], 'main')
                results.append({
                    'address': wallet['address'],
                    'balance': balance,
                    'private_key': wallet['private_key']
                })
            except Exception as e:
                print(f"检查地址 {wallet['address']} 时出错: {e}")
                # 即使检查失败也返回结果，余额设为-1表示检查失败
                results.append({
                    'address': wallet['address'],
                    'balance': -1,
                    'private_key': wallet['private_key']
                })
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
        print("\n🎉 发现有余额的地址:")
        for wallet in non_zero_wallets:
            print(f"地址: {wallet['address']}")
            print(f"余额: {wallet['balance']} BTC")
            print(f"私钥: {wallet['private_key']}")
            print("-" * 50)
    else:
        print("\n😔 未发现有余额的地址")
        
    # 打印失败的地址数量
    failed_checks = [w for w in results if w['balance'] == -1]
    if failed_checks:
        print(f"\n⚠️  {len(failed_checks)} 个地址余额检查失败")