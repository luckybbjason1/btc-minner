from get_wallet import get_wallet
import time  # 添加 time 模块导入

if __name__ == "__main__":
    for i in range(10):
        wallet = get_wallet('main')
        print(wallet)
        time.sleep(1)  # 每次请求后暂停 1 秒