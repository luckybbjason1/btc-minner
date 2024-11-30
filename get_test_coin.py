from utils.balance_check import get_balance

if __name__ == "__main__":
    address = 'tb1q5sps94sk52lf4ysck50vktnkzqdwagqujn68d7'
    balance = get_balance(address)
    print(f"地址 {address} 的余额为: {balance} tBTC")