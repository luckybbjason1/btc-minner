import requests

address_types = ['legacy', 'p2sh-segwit', 'bech32']

def satoshi_to_btc(satoshi):
    # return satoshi / 100000000
    return satoshi

def get_balance(address, network='test'):
    """
    查询比特币地址余额
    支持测试网络和主网络
    返回余额（单位：聪）
    """
    if not address:
        raise ValueError("地址不能为空")

    # 尝试多个API源
    apis = {
        'test': [
            {
                'url': f"https://api.blockcypher.com/v1/btc/test3/addrs/{address}/balance",
                'parser': lambda r: satoshi_to_btc(r.json().get('balance', 0))
            },
            # 备用API可以在这里添加
        ],
        'main': [
            {
                'url': f"https://api.blockcypher.com/v1/btc/main/addrs/{address}/balance",
                'parser': lambda r: satoshi_to_btc(r.json().get('balance', 0))
            },
            # 备用API可以在这里添加
        ]
    }

    if network not in apis:
        raise ValueError(f"不支持的网络类型: {network}")

    errors = []
    for api in apis[network]:
        try:
            response = requests.get(api['url'], timeout=30)  # 增加超时时间
            if response.status_code == 200:
                balance = api['parser'](response)
                return balance
            else:
                errors.append(f"HTTP错误 {response.status_code}: {response.text[:100]}")
        except requests.exceptions.RequestException as e:
            errors.append(f"网络请求错误 ({api['url']}): {str(e)}")
        except Exception as e:
            errors.append(f"解析错误 ({api['url']}): {str(e)}")
            continue

    # 如果所有API都失败，抛出详细错误信息
    error_message = f"所有API都失败了。网络: {network}, 地址: {address}\n错误详情: {'; '.join(errors)}"
    raise Exception(error_message)


if __name__ == "__main__":
    balance = get_balance('tb1qk2l86e8hmw6pu388wvxhaas3javp5c755fhg73', 'test')
    print(balance)