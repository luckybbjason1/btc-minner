import pickle
import os
import glob

def load_pkl_file(file_path):
    """
    从 .pkl 文件加载数据
    :param file_path: .pkl 文件路径
    :return: 反序列化后的对象
    """
    with open(file_path, 'rb') as file:
        data = pickle.load(file)
    return data

def get_prefix_from_filename(file_path):
    """
    从文件名中获取前缀
    :param file_path: 文件路径
    :return: 文件名前缀
    """
    # 获取文件名（不含路径和扩展名）
    filename = os.path.splitext(os.path.basename(file_path))[0]
    # 提取前缀（假设文件名格式为 'dataXX.pkl'）
    prefix = filename.replace('data', '')
    return prefix

def split_and_save_by_prefix(data, output_dir, file_prefix):
    """
    将数据按照前两位分片写入不同的文件
    :param data: 原始数据
    :param output_dir: 输出目录
    :param file_prefix: 文件前缀
    :return: 返回每个前缀的数据统计
    """
    # 创建输出目录（如果不存在）
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 用于存储统计信息
    stats = {'count': 0}
    
    # 准备输出文件
    output_file = os.path.join(output_dir, f'{file_prefix}.txt')
    mode = 'a' if os.path.exists(output_file) else 'w'
    
    # 写入数据
    with open(output_file, mode) as f:
        for item in data:
            if isinstance(item, str):
                f.write(f'{item}\n')
                stats['count'] += 1
    
    return stats

def process_all_pkl_files(input_dir, output_dir):
    """
    处理指定目录下的所有pkl文件
    :param input_dir: 输入目录
    :param output_dir: 输出目录
    """
    # 获取所有的pkl文件
    pkl_files = glob.glob(os.path.join(input_dir, '*.pkl'))
    pkl_files.sort()  # 确保文件按顺序处理
    
    # 用于存储总体统计信息
    total_stats = {}
    total_files = len(pkl_files)
    processed_files = 0
    
    for pkl_file in pkl_files:
        processed_files += 1
        file_prefix = get_prefix_from_filename(pkl_file)
        print(f"\n处理文件 [{processed_files}/{total_files}]: {pkl_file}")
        
        try:
            # 加载数据
            data = load_pkl_file(pkl_file)
            
            # 分片并保存，获取统计信息
            file_stats = split_and_save_by_prefix(data, output_dir, file_prefix)
            
            # 更新总体统计信息
            total_stats[file_prefix] = file_stats['count']
            
            print(f"文件 {pkl_file} 处理完成，写入 {file_stats['count']:,} 条数据")
            
        except Exception as e:
            print(f"处理文件 {pkl_file} 时出错: {str(e)}")
    
    # 打印总体统计信息
    print("\n=== 总体统计信息 ===")
    total_entries = sum(total_stats.values())
    for prefix, count in sorted(total_stats.items()):
        print(f"前缀 {prefix}: {count:,} 条数据")
    print(f"总计: {total_entries:,} 条数据")

# 示例用法
if __name__ == "__main__":
    input_dir = '/Users/gtja/Desktop/databases32G'  # pkl文件所在目录
    output_dir = '/Users/gtja/Desktop/databases32G/split_output'  # 输出目录
    
    # 处理所有pkl文件
    process_all_pkl_files(input_dir, output_dir)
    print("\n处理完成！")