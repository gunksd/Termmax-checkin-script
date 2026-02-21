# Termmax Auto Check-in Script

BSC 链上 Termmax 合约自动签到脚本，支持多钱包批量签到。

## 合约信息

| 项目 | 值 |
|------|-----|
| 合约地址 | `0x007200C66bd2a5BD7c744b90dF8eCBEB34fd26d4` |
| 方法 | `checkIn()` |
| 选择器 | `0x183ff085` |
| 网络 | BSC Mainnet (Chain ID: 56) |

## 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置私钥
cp .env.example .env
# 编辑 .env，填入私钥（多个用逗号分隔）

# 3. 运行
python checkin.py
```

## 配置说明

编辑 `.env` 文件：

```env
# 私钥，多个用逗号分隔（不要带 0x 前缀也行，脚本会自动处理）
PRIVATE_KEYS=aabbcc...,ddeeff...

# RPC 节点（可选，默认使用 BSC 公共节点）
BSC_RPC=https://bsc-dataseed.binance.org/
```

## 运行效果

```
[INFO] Connected to chain ID 56
[INFO] Contract: 0x007200C66bd2a5BD7c744b90dF8eCBEB34fd26d4
[INFO] Method:   0x183ff085 (checkIn)

[INFO] Loaded 3 wallet(s)

[1/3] 0xAbCd...1234
  ✅ Success | TX: 0x...
  ⏳ Waiting 3.2s...

[2/3] 0xEfGh...5678
  ✅ Success | TX: 0x...
  ⏳ Waiting 4.1s...

[3/3] 0xIjKl...9012
  ✅ Success | TX: 0x...

==================================================
[DONE] Success: 3 | Failed: 0 | Total: 3
```

## 复用到其他合约

修改 `checkin.py` 顶部的常量即可：

```python
CONTRACT_ADDRESS = "0x..."       # 合约地址
METHOD_SELECTOR = "0x..."        # 方法选择器（4 字节）
CHAIN_ID = 56                    # 链 ID
DEFAULT_RPC = "https://..."      # RPC 节点
```

常见链 ID：ETH=1 | BSC=56 | Arbitrum=42161 | Base=8453

## 安全提醒

- `.env` 已被 `.gitignore` 排除，不会被提交到 git
- 私钥仅在本地使用，不会上传到任何服务器
- 请勿在公共环境运行此脚本
