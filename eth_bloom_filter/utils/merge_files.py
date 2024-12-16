import pandas as pd
import os
from datetime import datetime

def merge_and_deduplicate(directory):
    # 获取目录下的所有CSV文件
    csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]
    print(f"找到 {len(csv_files)} 个CSV文件:")
    for file in csv_files:
        print(f"- {file}")

    # 读取所有CSV文件
    all_data = []
    for file in csv_files:
        file_path = os.path.join(directory, file)
        try:
            df = pd.read_csv(file_path)
            print(f"\n处理文件: {file}")
            print(f"读取到 {len(df)} 行数据")
            all_data.append(df)
        except Exception as e:
            print(f"读取文件 {file} 时出错: {str(e)}")
            continue

    if not all_data:
        print("没有成功读取任何文件")
        return

    # 合并所有数据
    merged_df = pd.concat(all_data, ignore_index=True)
    print(f"\n合并后共有 {len(merged_df)} 行数据")

    # 去重
    deduplicated_df = merged_df.drop_duplicates(subset=['address'])
    print(f"去重后剩余 {len(deduplicated_df)} 行数据")

    # 保存结果
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = os.path.join(directory, f'merged_addresses_{timestamp}.csv')
    deduplicated_df.to_csv(output_file, index=False)
    print(f"\n结果已保存到: {output_file}")

if __name__ == "__main__":
    directory = "/Users/gtja/Desktop/github/btc-minner/eth_bloom_filter/etherscan_data"
    merge_and_deduplicate(directory)
