# 比特币钱包生成器 / Bitcoin Wallet Generator

一个用于生成比特币钱包、检查余额和测试网络功能的Python工具集。

## ⚠️ 重要安全提示

- **本工具仅供学习和测试用途**
- **私钥是您比特币资产的唯一凭证，请务必安全保存**
- **不要在不安全的环境中使用主网功能**
- **建议在离线环境中生成私钥**

## 系统要求

- Python 3.8+
- 网络连接（用于余额查询）

## 安装依赖

```bash
pip install -r requirements.txt
```

## 功能说明

### 1. 基本钱包生成 (`get_btc.py`)
生成比特币钱包并持续检查余额：
```bash
python get_btc.py
```

### 2. 单次钱包生成 (`get_wallet.py`)
生成单个钱包并检查余额：
```bash
python get_wallet.py
```

### 3. CPU并行挖掘 (`btc_cpu.py`)
使用多核CPU并行生成大量地址：
```bash
python btc_cpu.py
```

### 4. GPU模拟挖掘 (`btc_cuda.py`)
高性能地址生成（模拟GPU批处理）：
```bash
python btc_cuda.py
```

### 5. 测试网络功能 (`test_network.py`)
测试比特币测试网络功能：
```bash
python test_network.py
```

### 6. 功能测试 (`test_functionality.py`)
验证所有核心功能是否正常工作：
```bash
python test_functionality.py
```

## 支持的地址类型

- **Legacy (P2PKH)**: 以 `1` 开头的传统地址
- **P2SH-SegWit**: 以 `3` 开头的兼容隔离见证地址  
- **Native SegWit (Bech32)**: 以 `bc1` 开头的原生隔离见证地址

## 网络支持

- **测试网络 (testnet)**: 用于开发和测试
- **主网络 (mainnet)**: 真实的比特币网络

## 项目结构

```
btc-minner/
├── get_btc.py              # 持续钱包生成
├── get_wallet.py           # 单次钱包生成  
├── btc_cpu.py             # CPU并行挖掘
├── btc_cuda.py            # GPU模拟挖掘
├── test_network.py        # 测试网络功能
├── test_functionality.py  # 功能测试脚本
├── utils/                 # 工具库
│   ├── balance_check.py   # 余额查询
│   ├── private_key_gen.py # 私钥生成
│   ├── wallet_generator.py # 钱包生成器
│   └── wallet_gen_bit.py  # Bit库钱包生成
└── requirements.txt       # 依赖列表
```

## 开发状态

### ✅ 已完成
- [x] 基本钱包生成功能
- [x] 多种地址类型支持
- [x] 测试网络和主网络支持
- [x] CPU多核并行处理
- [x] 余额查询功能
- [x] 安全的私钥生成
- [x] 基本功能测试

### 🚧 进行中
- [ ] GPU CUDA加速（当前为高性能CPU模拟）
- [ ] 更多API源支持
- [ ] 批量余额查询优化

### 📋 计划中
- [ ] 图形用户界面
- [ ] 钱包文件导入/导出
- [ ] 助记词支持
- [ ] 更多加密货币支持

## 使用示例

### 生成测试网络钱包
```python
from get_wallet import get_wallet

# 生成测试网络钱包
wallet = get_wallet('test')
print(f"地址: {wallet['addresses']}")
print(f"私钥: {wallet['private_key']}")
```

### 批量生成地址
```python
from btc_cpu import generate_addresses_multicore

# 生成100个地址
wallets = generate_addresses_multicore(100)
print(f"生成了 {len(wallets)} 个钱包")
```

## 注意事项

1. **私钥安全**: 永远不要与他人分享您的私钥
2. **网络连接**: 余额查询需要互联网连接
3. **API限制**: 频繁的API请求可能被限制
4. **测试环境**: 建议先在测试网络上熟悉功能

## 许可证

本项目仅供教育和研究目的使用。使用者需自行承担使用风险。

## 贡献

欢迎提交 Issue 和 Pull Request 来改进本项目。