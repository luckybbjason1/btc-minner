import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from datetime import datetime
import os

class EtherscanCrawler:
    def __init__(self):
        self.base_url = "https://etherscan.io/accounts"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive'
        }
        self.output_dir = 'etherscan_data'
        self.ensure_output_dir()
        self.session = requests.Session()
        # 创建输出文件名
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.output_file = f"{self.output_dir}/eth_addresses_{timestamp}.csv"
        # 创建文件并写入表头
        with open(self.output_file, 'w') as f:
            f.write('address,page\n')

    def ensure_output_dir(self):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def get_page(self, page=1, max_retries=3):
        """获取指定页面的数据，支持重试"""
        url = f"{self.base_url}/{page}?ps=100"  # 每页显示100条数据
        
        for attempt in range(max_retries):
            try:
                response = self.session.get(url, headers=self.headers, timeout=10)
                response.raise_for_status()
                
                # 检查是否被重定向到验证页面
                if "Checking your browser" in response.text:
                    print(f"被检测到爬虫行为，等待后重试...")
                    time.sleep(10 + random.uniform(1, 5))
                    continue
                    
                return response.text
            except requests.RequestException as e:
                print(f"获取页面 {page} 时出错 (尝试 {attempt + 1}/{max_retries}): {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(5 + random.uniform(1, 5))
                continue
        return None

    def parse_page(self, html):
        """解析页面内容，提取所有钱包地址"""
        if not html:
            return []

        soup = BeautifulSoup(html, 'html.parser')
        addresses = set()  # 使用集合去重
        
        # 找到所有的链接
        for link in soup.find_all('a'):
            href = link.get('href', '')
            if href.startswith('/address/'):
                # 提取地址（移除 '/address/' 前缀）
                address = href[9:]
                addresses.add(address)
        
        # 将地址转换为列表并排序
        addresses = sorted(list(addresses))
        
        # 为每个地址创建一条记录
        records = []
        for address in addresses:
            records.append({
                'address': address
            })
            print(f"找到地址: {address}")
        
        if not records:
            print("本页未找到任何地址")
        else:
            print(f"本页共找到 {len(records)} 个唯一地址")
        
        return records

    def save_to_csv(self, data):
        """保存数据到CSV文件"""
        if not data:
            return
        
        df = pd.DataFrame(data)
        # 追加模式写入数据
        df.to_csv(self.output_file, mode='a', header=False, index=False)
        print(f"数据已追加到: {self.output_file}")
        print(f"本页保存 {len(data)} 条数据")

    def crawl(self, start_page=1, end_page=1, delay=3):
        """爬取指定范围的页面"""
        total_addresses = 0
        self.current_page = start_page
        
        for page in range(start_page, end_page + 1):
            self.current_page = page
            print(f"\n正在爬取第 {page} 页...")
            
            # 获取页面内容
            html = self.get_page(page)
            if not html:
                print(f"页面 {page} 获取失败，跳过")
                continue

            # 解析数据并立即保存
            addresses = self.parse_page(html)
            if addresses:
                self.save_to_csv(addresses)
                total_addresses += len(addresses)

            # 随机延迟
            if page < end_page:
                sleep_time = delay + random.uniform(1, 3)
                print(f"等待 {sleep_time:.1f} 秒后继续...")
                time.sleep(sleep_time)

        print(f"\n爬取完成！共获取 {total_addresses} 个地址")
        print(f"所有数据已保存到: {self.output_file}")

def main():
    crawler = EtherscanCrawler()
    
    # 设置爬取参数
    start_page = 22
    end_page = 400  # 可以根据需要修改页数
    delay = 3  # 每页之间的基础延迟时间（秒）

    print(f"开始爬取 Etherscan 账户地址 (页面 {start_page} 到 {end_page})...")
    crawler.crawl(start_page, end_page, delay)

if __name__ == "__main__":
    main()
