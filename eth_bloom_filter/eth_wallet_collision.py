from eth_wallet_generator import generate_eth_wallet, generate_multiple_wallets
from bloom_with_map import BloomFilterWithMap
import time
import json
from datetime import datetime
import os
import sys

class WalletCollisionChecker:
    def __init__(self, bloom_filter_path: str, output_dir: str = "collisions"):
        """
        初始化钱包碰撞检查器
        
        Args:
            bloom_filter_path: 布隆过滤器文件路径
            output_dir: 碰撞结果输出目录
        """
        self.bloom_filter = BloomFilterWithMap.load_from_file(bloom_filter_path)
        self.output_dir = output_dir
        self.collision_count = 0
        self.check_count = 0
        self.start_time = time.time()
        
        # 创建输出目录
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        # 创建碰撞记录文件
        self.collision_file = os.path.join(output_dir, f"collisions_{int(time.time())}.json")
        
    def check_wallet(self, private_key: str, address: str) -> bool:
        """
        检查单个钱包地址是否发生碰撞
        
        Returns:
            bool: 是否发生碰撞
        """
        self.check_count += 1
        # 移除地址中的 '0x' 前缀（如果有）
        address = address.replace('0x', '')
        
        # 检查地址是否在布隆过滤器中
        bloom_result, exact_result = self.bloom_filter.contains(address)
        
        if exact_result:  # 发生碰撞
            self.collision_count += 1
            self._save_collision(private_key, address)
            return True
        return False
    
    def _save_collision(self, private_key: str, address: str):
        """保存碰撞结果到文件"""
        collision_data = {
            "timestamp": datetime.now().isoformat(),
            "private_key": private_key,
            "address": address
        }
        
        with open(self.collision_file, 'a') as f:
            f.write(json.dumps(collision_data) + '\n')
    
    def get_stats(self) -> dict:
        """获取当前统计信息"""
        elapsed_time = time.time() - self.start_time
        return {
            "检查总数": self.check_count,
            "碰撞次数": self.collision_count,
            "运行时间(秒)": round(elapsed_time, 2),
            "每秒检查数": round(self.check_count / elapsed_time, 2) if elapsed_time > 0 else 0
        }

def main(BLOOM_FILTER_PATH):
    # 配置参数
    BATCH_SIZE = 100  # 每批生成的钱包数量
    
    # 初始化检查器
    checker = WalletCollisionChecker(BLOOM_FILTER_PATH)
    
    try:
        print("开始检查钱包碰撞...")
        while True:
            # 批量生成钱包
            wallets = generate_multiple_wallets(BATCH_SIZE)
            
            # 检查每个钱包
            for private_key, address in wallets:
                if checker.check_wallet(private_key, address):
                    print(f"\n发现碰撞!")
                    print(f"地址: {address}")
                    print(f"私钥: {private_key}")
                
                # 每1000个钱包显示一次统计信息
                if checker.check_count % 1000 == 0:
                    stats = checker.get_stats()
                    print("\n当前统计:")
                    for key, value in stats.items():
                        print(f"{key}: {value}")
                    
    except KeyboardInterrupt:
        print("\n程序终止")
        print("\n最终统计:")
        stats = checker.get_stats()
        for key, value in stats.items():
            print(f"{key}: {value}")

"""
BLOOM_FILTER_PATH = "/Users/gtja/Desktop/eth_pkl/bloom_with_map_big.pkl"  # 布隆过滤器文件路径

"""
if __name__ == "__main__":
    BLOOM_FILTER_PATH = sys.argv[1]
    main(BLOOM_FILTER_PATH)
