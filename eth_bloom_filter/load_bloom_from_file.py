import math
import mmh3
from bitarray import bitarray
import pickle
from collections import defaultdict
import threading
from bloom_with_map import BloomFilterWithMap

# 示例用法
if __name__ == "__main__":

    # 从文件加载
    loaded_filter = BloomFilterWithMap.load_from_file("/Users/gtja/Desktop/eth_pkl/all/6.pkl")

    print(loaded_filter.get_stats())

    # 测试已保存的过滤器
    test_address = "686b323b49bDFb57574469c872C471C316e3a405"
    bloom_result, exact_result = loaded_filter.contains(test_address)
    print(f"\n已保存的过滤器测试地址: {test_address}")
    print(f"布隆过滤器结果: {'可能存在' if bloom_result else '一定不存在'}")
    print(f"精确匹配结果: {'存在' if exact_result else '不存在'}")

    # 测试不存在的地址
    test_address = "686b323b49bDF1b57574469c872C471C316e3a405"
    bloom_result, exact_result = loaded_filter.contains(test_address)
    print(f"\n已保存的过滤器测试不存在的地址: {test_address}")
    print(f"布隆过滤器结果: {'可能存在' if bloom_result else '一定不存在'}")
    print(f"精确匹配结果: {'存在' if exact_result else '不存在'}")