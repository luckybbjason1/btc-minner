import requests

address_types = ['legacy', 'p2sh-segwit', 'bech32']

def satoshi_to_btc(satoshi):
    # return satoshi / 100000000
    return satoshi

def get_balance(address, network='test'):
    """
    查询比特币地址余额
    支持测试网络和主网络
    返回余额（单位：BTC）
    """

    # 尝试多个API源
    apis = {
        'test': [
            {
                'url': f"https://api.blockcypher.com/v1/btc/test3/addrs/{address}/balance",
                'parser': lambda r: satoshi_to_btc(r.json().get('balance', 0))
            },
            # {
            #     'url': f"https://blockstream.info/testnet/api/address/{address}",
            #     'parser': lambda r: satoshi_to_btc(
            #         sum([tx.get('value', 0) for tx in r.json().get('chain_stats', {}).get('funded_txo_sum', [])])
            #     )
            # },
            # {
            #     'url': f"https://api.bitaps.com/btc/testnet/v1/blockchain/address/state/{address}",
            #     'parser': lambda r: satoshi_to_btc(r.json().get('data', {}).get('balance', 0))
            # }
        ],
        'main': [
            {
                'url': f"https://api.blockcypher.com/v1/btc/main/addrs/{address}/balance",
                'parser': lambda r: satoshi_to_btc(r.json().get('balance', 0))
            },
            # {
            #     'url': f"https://blockstream.info/api/address/{address}",
            #     'parser': lambda r: satoshi_to_btc(r.json().get('chain_stats', {}).get('funded_txo_sum', 0))
            # },
            # {
            #     'url': f"https://blockchain.info/balance?active={address}",
            #     'parser': lambda r: satoshi_to_btc(r.json().get(address, {}).get('final_balance', 0))
            # }
        ]
    }

    errors = []
    for api in apis[network]:
        try:
            response = requests.get(api['url'], timeout=10)
            # print(response)
            if response.status_code == 200:
                balance = api['parser'](response)
                return balance
        except Exception as e:
            errors.append(f"API错误 ({api['url']}): {str(e)}")
            continue

    raise Exception(f"所有API都失败了。错误: {'; '.join(errors)}")


if __name__ == "__main__":
    balance = get_balance('tb1qk2l86e8hmw6pu388wvxhaas3javp5c755fhg73', 'test')
    print(balance)