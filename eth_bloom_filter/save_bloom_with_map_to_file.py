import os
import glob
from bloom_with_map import BloomFilterWithMap

def process_single_csv(csv_file, n, fp_rate, save_dir):
    """
    处理单个CSV文件并保存为对应的PKL文件
    :param csv_file: CSV文件路径
    :param n: 预期元素数量
    :param fp_rate: 期望的假阳性率
    :param save_dir: PKL文件保存目录
    :return: 处理的地址数量
    """
    print(f"\n处理文件: {os.path.basename(csv_file)}")
    
    # 创建布隆过滤器实例
    bloom_filter = BloomFilterWithMap(n, fp_rate)
    
    # 加载CSV文件
    count = bloom_filter.load_from_csv(csv_file)
    
    if count > 0:
        # 生成保存路径：使用CSV文件名，但改为.pkl扩展名
        save_name = os.path.splitext(os.path.basename(csv_file))[0] + '.pkl'
        save_path = os.path.join(save_dir, save_name)
        
        # 保存布隆过滤器
        bloom_filter.save_to_file(save_path)
        print(f"从文件 {os.path.basename(csv_file)} 中加载了 {count} 个地址")
        print(f"布隆过滤器已保存到: {save_path}")
        
        # 输出统计信息
        stats = bloom_filter.get_stats()
        print(f"统计信息: {stats}")
    else:
        print(f"警告：文件 {os.path.basename(csv_file)} 处理失败或没有有效数据")
    
    # 释放内存
    del bloom_filter
    return count

def process_directory(data_dir, save_dir, n, fp_rate):
    """
    处理目录中的所有CSV文件
    :param data_dir: CSV文件所在目录
    :param save_dir: PKL文件保存目录
    :param n: 每个布隆过滤器的预期元素数量
    :param fp_rate: 期望的假阳性率
    :return: 总共处理的地址数量
    """
    # 确保保存目录存在
    os.makedirs(save_dir, exist_ok=True)
    
    # 获取所有CSV文件
    csv_files = glob.glob(os.path.join(data_dir, "*.csv"))
    if not csv_files:
        print(f"警告：在目录 {data_dir} 中没有找到CSV文件")
        return 0
    
    print(f"找到 {len(csv_files)} 个CSV文件")
    
    # 处理每个CSV文件
    total_count = 0
    for csv_file in csv_files:
        count = process_single_csv(csv_file, n, fp_rate, save_dir)
        if count > 0:
            total_count += count
    
    print(f"\n总共成功处理 {total_count} 个地址")
    return total_count

def main():
    # 设置参数
    n = 20_000  # 每个文件的预期元素数量
    fp_rate = 0.01
    
    # 处理big目录
    data_dir = "/Users/gtja/Desktop/etherscan_data/big"
    save_dir = "/Users/gtja/Desktop/eth_pkl/big"
    process_directory(data_dir, save_dir, n, fp_rate)
    
    n = 12000000  # 每个文件的预期元素数量
    # 处理all目录
    data_dir = "/Users/gtja/Desktop/etherscan_data/all"
    save_dir = "/Users/gtja/Desktop/eth_pkl/all"
    process_directory(data_dir, save_dir, n, fp_rate)

if __name__ == "__main__":
    main()