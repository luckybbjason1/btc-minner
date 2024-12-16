import os
import glob
from bloom import BloomFilter

def process_directory(data_dir, save_dir, bloom_filter):
    """
    处理目录中的所有CSV文件
    :param data_dir: CSV文件所在目录
    :param save_dir: PKL文件保存目录
    :return: 总共处理的地址数量
    :param bloom_filter: 期望的假阳性率
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
        print(f"\n处理文件: {os.path.basename(csv_file)}")
        count = bloom_filter.load_from_csv(csv_file)
        if count > 0:
            total_count += count
    
    print(f"\n总共成功处理 {total_count} 个地址")

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

    return total_count

def main():
    # 设置参数
    n = 200000000  # 每个文件的预期元素数量
    fp_rate = 0.0001
    
    bloom_filter = BloomFilter(n, fp_rate)
    # 处理all目录
    data_dir = "/Users/gtja/Desktop/etherscan_data/all"
    save_dir = "/Users/gtja/Desktop/eth_pkl/all2"
    process_directory(data_dir, save_dir, bloom_filter)

if __name__ == "__main__":
    main()