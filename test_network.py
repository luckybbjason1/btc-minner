from bitcoinlib.wallets import Wallet
from bitcoinlib.transactions import Transaction
from bitcoinlib.keys import Key
import requests

def create_test_transaction(from_wif, from_address, to_address, amount_btc, address_type='legacy'):
    """
    创建测试网络比特币转账交易
    
    参数:
    - from_wif: 发送方私钥（WIF格式）
    - from_address: 发送方地址
    - to_address: 接收方地址
    - amount_btc: 发送金额（BTC）
    - address_type: 地址类型 ('legacy', 'p2sh-segwit', 'bech32')
    """
    try:
        # 创建钱包
        key = Key(from_wif, network='testnet')
        wallet = Wallet.create('test_wallet', keys=key, network='testnet')
        
        # 获取UTXO
        url = f"https://api.blockcypher.com/v1/btc/test3/addrs/{from_address}?unspentOnly=true"
        response = requests.get(url)
        utxos = response.json().get('txrefs', [])
        
        if not utxos:
            raise Exception("没有可用的UTXO")
            
        # 创建交易
        amount_satoshi = int(amount_btc * 100000000)  # 转换为聪
        tx = Transaction(network='testnet')
        
        # 添加输入
        for utxo in utxos:
            tx.add_input(
                prev_hash=utxo['tx_hash'],
                output_n=utxo['tx_output_n'],
                keys=key,
                value=utxo['value']
            )
            
        # 添加输出
        tx.add_output(to_address, amount_satoshi)
        
        # 计算并添加找零
        total_input = sum(utxo['value'] for utxo in utxos)
        fee = 1000  # 设置手续费（聪）
        change = total_input - amount_satoshi - fee
        if change > 0:
            tx.add_output(from_address, change)
            
        # 签名交易
        tx.sign()
        
        # 广播交易
        raw_tx = tx.raw_hex()
        url = "https://api.blockcypher.com/v1/btc/test3/txs/push"
        response = requests.post(url, json={"tx": raw_tx})
        
        if response.status_code == 200:
            tx_hash = response.json().get('tx', {}).get('hash')
            return True, f"交易成功，交易哈希: {tx_hash}"
        else:
            return False, f"广播交易失败: {response.text}"
            
    except Exception as e:
        return False, f"创建交易失败: {str(e)}"

def get_test_coins(address):
    """
    从测试网水龙头获取测试币
    """
    faucets = [
        "https://testnet-faucet.mempool.co/api/faucet",
        "https://coinfaucet.eu/en/btc-testnet/"
    ]
    
    print("请从以下水龙头获取测试币：")
    for faucet in faucets:
        print(f"- {faucet}")
    print(f"\n您的测试网地址: {address}")

# 测试代码
if __name__ == "__main__":
    # 生成新钱包
    wallet = generate_bitcoin_address(network='test')
    
    print("\n=== 测试网络比特币钱包 ===")
    print("\n私钥(WIF格式):", wallet['private_key'])
    print("\n地址:")
    for addr_type, address in wallet['address_map'].items():
        print(f"{addr_type}: {address}")
    
    # 获取测试币
    print("\n=== 获取测试币 ===")
    get_test_coins(wallet['address_map']['bech32'])  # 使用bech32地址
    
    # 等待用户确认收到测试币
    input("\n请在获取测试币后按回车继续...")
    
    # 查询余额
    for addr_type, address in wallet['address_map'].items():
        try:
            balance = get_balance(address, network='test')
            print(f"\n{addr_type}地址余额: {balance} tBTC")
        except Exception as e:
            print(f"查询{addr_type}地址余额失败: {str(e)}")
    
    # 测试转账
    to_address = input("\n请输入接收地址: ")
    amount = float(input("请输入转账金额(BTC): "))
    
    # 选择发送地址类型
    print("\n请选择发送地址类型:")
    for i, addr_type in enumerate(wallet['address_map'].keys()):
        print(f"{i+1}. {addr_type}")
    choice = int(input("请选择(1-3): ")) - 1
    from_type = list(wallet['address_map'].keys())[choice]
    
    # 执行转账
    success, message = create_test_transaction(
        wallet['private_key'],
        wallet['address_map'][from_type],
        to_address,
        amount,
        from_type
    )
    
    print(f"\n转账结果: {message}")