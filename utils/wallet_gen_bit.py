from bit import PrivateKeyTestnet
import hashlib
import base58
from bit import Key
from bit.format import verify_sig
import hashlib

def gen_addresses(private_key_wif, network='test'):
    """
    使用 bit 库生成钱包
    """
    key = Key(private_key_wif) if network == 'main' else PrivateKeyTestnet(private_key_wif)
    
    # bit 库生成的地址
    addresses_map = {
        'legacy': key.address,                    # 1开头
        # 'p2sh-segwit': key.segwit_address,       # 3开头
        # 'bech32': key.segwit_address             # bc1开头
    }

    res = {
        'address' : addresses_map,
        'private_key' : key.to_wif(),
        'public_key' : key.public_key.hex()
    }

    return res