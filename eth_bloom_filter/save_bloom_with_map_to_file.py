import os
import glob
from bloom_with_map import BloomFilterWithMap
import sys

def process_directory(data_dir, save_path, bloom_filter):
    """
    处理目录中的所有CSV文件
    :param data_dir: CSV文件所在目录
    :param save_path: PKL文件保存目录
    :return: 总共处理的地址数量
    :param bloom_filter: 期望的假阳性率
    """
    # 确保保存目录存在
    os.makedirs(save_path, exist_ok=True)
    
    # 获取所有CSV文件
    csv_files = glob.glob(os.path.join(data_dir, "*.csv"))
    if not csv_files:
        print(f"警告：在目录 {data_dir} 中没有找到CSV文件")
        return 0
    
    print(f"找到 {len(csv_files)} 个CSV文件")
    
    # 处理每个CSV文件
    total_count = 0
    for csv_file in csv_files:
        print(f"\n处理文件: {os.path.basename(csv_file)}")
        # 加载CSV文件
        count = bloom_filter.load_from_csv(csv_file)
        print(f"从文件 {os.path.basename(csv_file)} 中加载了 {count} 个地址")
        if count > 0:
            total_count += count
    
    print(f"\n总共成功处理 {total_count} 个地址")
    # 保存布隆过滤器
    bloom_filter.save_to_file(save_path)
    print(f"布隆过滤器已保存到: {save_path}")

    # 输出统计信息
    stats = bloom_filter.get_stats()
    print(f"统计信息: {stats}")

    return total_count

"""
python save_bloom_with_map_to_file.py 20000 /Users/lantian/Desktop/all /Users/lantian/Desktop/all.pkl
python save_bloom_with_map_to_file.py 12000000 /Users/lantian/Desktop/all /Users/lantian/Desktop/all.pkl
"""
if __name__ == "__main__":
    fp_rate = 0.0001
    n = sys.argv[1]
    data_dir = sys.argv[2]
    save_dir = sys.argv[3]
    # 创建布隆过滤器实例
    bloom_filter = BloomFilterWithMap(n, fp_rate)
    process_directory(data_dir, save_dir, bloom_filter)
