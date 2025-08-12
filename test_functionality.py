#!/usr/bin/env python3
"""
基本功能测试脚本
Tests basic functionality of the btc-minner codebase
"""

import sys
import traceback
from utils.private_key_gen import gen_private_key_wif
from utils.wallet_generator import generate_bitcoin_address
from utils.wallet_gen_bit import gen_addresses
from btc_cpu import generate_single_address
from btc_cuda import generate_single_address_fast

def test_private_key_generation():
    """测试私钥生成"""
    print("🔑 测试私钥生成...")
    try:
        # 测试网络私钥
        test_key = gen_private_key_wif('test')
        assert 'private_key_wif' in test_key
        assert 'private_key_bytes' in test_key
        assert len(test_key['private_key_bytes']) == 32
        print("✅ 测试网络私钥生成成功")
        
        # 主网私钥
        main_key = gen_private_key_wif('main')
        assert 'private_key_wif' in main_key
        assert 'private_key_bytes' in main_key
        assert len(main_key['private_key_bytes']) == 32
        print("✅ 主网私钥生成成功")
        
        return True
    except Exception as e:
        print(f"❌ 私钥生成测试失败: {e}")
        traceback.print_exc()
        return False

def test_address_generation():
    """测试地址生成"""
    print("\n🏠 测试地址生成...")
    try:
        # 生成私钥
        private_key = gen_private_key_wif('test')
        
        # 测试自定义地址生成
        wallet = generate_bitcoin_address(private_key['private_key_bytes'], 'test')
        assert 'address_map' in wallet
        assert 'public_key' in wallet
        assert 'legacy' in wallet['address_map']
        print("✅ 自定义地址生成成功")
        
        # 测试bit库地址生成
        bit_wallet = gen_addresses(private_key['private_key_wif'], 'test')
        assert 'address' in bit_wallet
        assert 'private_key' in bit_wallet
        assert 'public_key' in bit_wallet
        print("✅ Bit库地址生成成功")
        
        return True
    except Exception as e:
        print(f"❌ 地址生成测试失败: {e}")
        traceback.print_exc()
        return False

def test_cpu_mining():
    """测试CPU挖掘功能"""
    print("\n💻 测试CPU挖掘功能...")
    try:
        address = generate_single_address()
        assert address is not None
        assert 'address' in address
        assert 'private_key' in address
        assert 'public_key' in address
        print("✅ CPU单地址生成成功")
        
        return True
    except Exception as e:
        print(f"❌ CPU挖掘测试失败: {e}")
        traceback.print_exc()
        return False

def test_gpu_simulation():
    """测试GPU模拟功能"""
    print("\n🚀 测试GPU模拟功能...")
    try:
        address = generate_single_address_fast()
        assert address is not None
        assert 'address' in address
        assert 'private_key' in address
        assert 'public_key' in address
        print("✅ GPU模拟单地址生成成功")
        
        return True
    except Exception as e:
        print(f"❌ GPU模拟测试失败: {e}")
        traceback.print_exc()
        return False

def test_imports():
    """测试所有重要模块的导入"""
    print("\n📦 测试模块导入...")
    try:
        # 测试所有重要模块能否正常导入
        import hashlib
        import ecdsa
        import base58
        import requests
        import bech32
        import bit
        import bitcoinlib
        
        print("✅ 所有依赖模块导入成功")
        return True
    except Exception as e:
        print(f"❌ 模块导入测试失败: {e}")
        traceback.print_exc()
        return False

def main():
    """运行所有测试"""
    print("🧪 开始运行基本功能测试")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_private_key_generation,
        test_address_generation,
        test_cpu_mining,
        test_gpu_simulation
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ 测试运行出错: {e}")
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 测试结果: {passed} 通过, {failed} 失败")
    
    if failed == 0:
        print("🎉 所有测试通过！代码基本功能正常。")
        return 0
    else:
        print("⚠️ 有测试失败，请检查错误信息。")
        return 1

if __name__ == "__main__":
    sys.exit(main())