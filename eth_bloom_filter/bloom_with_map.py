import math
import mmh3
from bitarray import bitarray
import pickle
from collections import defaultdict

class BloomFilterWithMap:
    def __init__(self, n, fp_rate):
        """
        初始化布隆过滤器和哈希表
        :param n: 预期元素数量
        :param fp_rate: 期望的假阳性率
        """
        self.size = self._get_size(n, fp_rate)
        self.hash_count = self._get_hash_count(self.size, n)
        self.bit_array = bitarray(self.size, endian='little')
        self.bit_array.setall(0)
        
        # 创建桶，包括0-9, a-f, A-F
        self.buckets = {}
        # 数字 0-9
        for i in range(10):
            self.buckets[str(i)] = set()
        # 小写字母 a-f
        for c in 'abcdef':
            self.buckets[c] = set()

    def _get_size(self, n, p):
        """计算布隆过滤器的最优大小"""
        m = -(n * math.log(p)) / (math.log(2) ** 2)
        return int(m)

    def _get_hash_count(self, m, n):
        """计算最优哈希函数数量"""
        k = (m / n) * math.log(2)
        return int(k)

    def _get_bucket_key(self, item):
        """
        获取项目应该存储在哪个桶中
        :param item: 16进制地址字符串
        :return: 桶的键（第二个字符）
        """
        if len(item) < 2:
            raise ValueError(f"地址长度不足: {item}")
        return item[1]  # 返回第二个字符作为桶的键

    def add(self, item):
        """
        添加元素到布隆过滤器和哈希表
        :param item: 要添加的元素（16进制字符串）
        """
        # 转换为小写
        item = item.lower()
        
        # 添加到布隆过滤器
        for i in range(self.hash_count):
            digest = mmh3.hash(item, i) % self.size
            self.bit_array[digest] = True

        # 添加到对应的桶中
        bucket_key = self._get_bucket_key(item)
        if bucket_key not in self.buckets:
            raise ValueError(f"无效的16进制字符: {bucket_key}")
        self.buckets[bucket_key].add(item)

    def contains(self, item):
        """
        检查元素是否存在
        :param item: 要检查的元素（16进制字符串）
        :return: (bool, bool) - (布隆过滤器结果, 精确匹配结果)
        """
        if len(item) < 2:
            return False, False

        # 转换为小写
        item = item.lower()

        # 首先检查布隆过滤器
        bloom_result = True
        for i in range(self.hash_count):
            digest = mmh3.hash(item, i) % self.size
            if not self.bit_array[digest]:
                bloom_result = False
                break

        # 如果布隆过滤器返回False，项目必定不存在
        if not bloom_result:
            return False, False

        # 检查对应的桶
        bucket_key = self._get_bucket_key(item)
        if bucket_key not in self.buckets:
            return False, False
        exact_result = item in self.buckets[bucket_key]
        return bloom_result, exact_result

    def save_to_file(self, file_path):
        """
        将布隆过滤器保存到文件
        :param file_path: 保存路径
        """
        with open(file_path, 'wb') as file:
            pickle.dump({
                'size': self.size,
                'hash_count': self.hash_count,
                'bit_array': self.bit_array,
                'buckets': self.buckets
            }, file)

    @classmethod
    def load_from_file(cls, file_path):
        """
        从文件加载布隆过滤器
        :param file_path: 文件路径
        :return: BloomFilterWithMap实例
        """
        with open(file_path, 'rb') as file:
            data = pickle.load(file)
            bloom_filter = cls(1, 0.01)  # 临时参数，将被覆盖
            bloom_filter.size = data['size']
            bloom_filter.hash_count = data['hash_count']
            bloom_filter.bit_array = data['bit_array']
            bloom_filter.buckets = data['buckets']
            return bloom_filter

    def get_stats(self):
        """
        获取布隆过滤器的统计信息
        :return: dict 包含统计信息
        """
        stats = {
            'total_size': self.size,
            'hash_functions': self.hash_count,
            'bucket_sizes': {k: len(v) for k, v in self.buckets.items()},
            'total_items': sum(len(v) for v in self.buckets.values())
        }
        return stats

    def load_from_csv(self, file_path, batch_size=5000):
        """
        从CSV文件中加载数据，假设地址在第一列
        :param file_path: CSV文件路径
        :param batch_size: 批处理大小
        :return: 处理的数据数量
        """
        try:
            import pandas as pd
            print(f"开始从CSV文件 {file_path} 加载数据...")
            
            # 使用分块读取CSV文件，不使用header
            count = 0
            for chunk in pd.read_csv(file_path, header=None, chunksize=batch_size):
                addresses = chunk[0].dropna().tolist()  # 使用第一列（索引0）
                # 对每个地址单独调用add方法，转换为小写
                for address in addresses:
                    address = str(address).strip().lower()  # 确保移除空白字符并转换为小写
                    if address:  # 确保地址不为空
                        self.add(address)
                count += len(addresses)
                # print(f"已处理 {count} 条数据...")
            
            print(f"数据加载完成，共处理 {count} 条数据")
            return count
            
        except Exception as e:
            print(f"加载CSV文件时出错: {str(e)}")
            return 0

# 示例用法
if __name__ == "__main__":
    # 创建数据结构实例：2亿个元素，1%错误率
    n = 200_000_000
    fp_rate = 0.01
    bloom_filter = BloomFilterWithMap(n, fp_rate)

    # 从文件加载数据的示例
    csv_file = "etherscan_data/test.csv"  # CSV文件路径
    count = bloom_filter.load_from_csv(csv_file)
    print(f"\n成功加载 {count} 个地址")

    # 测试查询
    test_address = "0xbe0eb53f46cd790cd13851d5eff43d12404d33e8"
    bloom_filter.add(test_address)  # 先添加测试地址
    
    bloom_result, exact_result = bloom_filter.contains(test_address)
    print(f"\n测试地址: {test_address}")
    print(f"布隆过滤器结果: {'可能存在' if bloom_result else '一定不存在'}")
    print(f"精确匹配结果: {'存在' if exact_result else '不存在'}")

    # 测试一个不存在的地址
    test_address = "0xbe0eb53f4611cd790cd13851d5eff43d12404d33e8"
    bloom_result, exact_result = bloom_filter.contains(test_address)
    print(f"\n测试地址: {test_address}")
    print(f"布隆过滤器结果: {'可能存在' if bloom_result else '一定不存在'}")
    print(f"精确匹配结果: {'存在' if exact_result else '不存在'}")

    # 保存到文件
    bloom_filter.save_to_file("bloom_with_map.pkl")

    # 从文件加载
    loaded_filter = BloomFilterWithMap.load_from_file("bloom_with_map.pkl")

    # 测试已保存的过滤器
    test_address = "0xbe0eb53f46cd790cd13851d5eff43d12404d33e8"
    bloom_result, exact_result = loaded_filter.contains(test_address)
    print(f"\n已保存的过滤器测试地址: {test_address}")
    print(f"布隆过滤器结果: {'可能存在' if bloom_result else '一定不存在'}")
    print(f"精确匹配结果: {'存在' if exact_result else '不存在'}")

    # 测试不存在的地址
    test_address = "0xbe0eb53f4611cd790cd13851d5eff43d12404d33e8"
    bloom_result, exact_result = loaded_filter.contains(test_address)
    print(f"\n已保存的过滤器测试不存在的地址: {test_address}")
    print(f"布隆过滤器结果: {'可能存在' if bloom_result else '一定不存在'}")
    print(f"精确匹配结果: {'存在' if exact_result else '不存在'}")
