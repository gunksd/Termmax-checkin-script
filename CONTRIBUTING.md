# 复用指南：如何改成其他合约的签到脚本

本指南教你如何将这个脚本改成适用于**任何链上合约**的自动签到工具。

---

## 你需要准备什么

| 信息 | 在哪找 | 示例 |
|------|--------|------|
| 合约地址 | 项目官方文档 / 区块链浏览器 | `0x007200C66bd2a5BD7c744b90dF8eCBEB34fd26d4` |
| 方法选择器 | 见下方「如何获取方法选择器」 | `0x183ff085` |
| 链 ID | 见下方「常见链 ID 表」 | `56` |
| RPC 地址 | 见下方「常见 RPC 表」 | `https://bsc-dataseed.binance.org/` |

---

## 第一步：获取方法选择器

方法选择器是函数签名的 keccak256 哈希前 4 字节（8 个十六进制字符）。

### 方法 A：从区块链浏览器复制（最简单）

1. 打开对应链的区块链浏览器（如 bscscan.com）
2. 搜索合约地址
3. 点击「Contract」→「Read/Write Contract」
4. 找到你要调用的方法
5. 或者找一笔别人成功调用的交易，查看 Input Data 开头的 `0x________`（前 10 个字符，包含 0x）

### 方法 B：用 Python 计算

```python
from web3 import Web3
selector = Web3.keccak(text="checkIn()")[:4].hex()
print(f"0x{selector}")  # 输出: 0x183ff085
```

注意：括号里要写完整参数类型，无参数就写 `()`，例如：
- `checkIn()` → 无参数
- `claim(address)` → 有一个 address 参数
- `deposit(uint256,address)` → 有两个参数

---

## 第二步：修改 checkin.py

打开 `checkin.py`，修改文件顶部的配置区：

```python
# ============================================================
# Configuration - modify these for different contracts/methods
# ============================================================
CONTRACT_ADDRESS = "0x..."       # ← 改成新合约地址
METHOD_SELECTOR = "0x..."        # ← 改成新方法选择器
CHAIN_ID = 56                    # ← 改成目标链 ID
DEFAULT_RPC = "https://..."      # ← 改成对应链的 RPC
DELAY_RANGE = (2, 5)             # ← 钱包间隔秒数，可按需调整
GAS_MULTIPLIER = 1.2             # ← Gas 估算倍数，一般不用改
```

只需要改前 4 行，其他代码不需要动。

---

## 第三步：配置私钥和 RPC

### keys.txt — 私钥文件

从示例复制再编辑：

```bash
cp keys.example.txt keys.txt
```

一行一个私钥，直接粘贴，数量不限，支持 `#` 注释：

```
0xaabbccdd...
0xeeff0011...
0x22334455...
# 这行是注释，会被忽略
```

### .env — RPC 配置（可选）

```env
BSC_RPC=https://对应链的RPC地址/
```

注意：`.env` 里的 `BSC_RPC` 这个变量名可以不改，脚本只是读取这个值作为 RPC 地址。

---

## 常见链 ID 表

| 链 | Chain ID | 典型 Gas 费 |
|----|----------|-------------|
| Ethereum | 1 | 高 |
| BSC | 56 | 低 |
| Polygon | 137 | 极低 |
| Arbitrum One | 42161 | 低 |
| Optimism | 10 | 低 |
| Base | 8453 | 低 |
| Avalanche C-Chain | 43114 | 中 |
| zkSync Era | 324 | 低 |
| Linea | 59144 | 低 |
| Scroll | 534352 | 低 |

---

## 常见 RPC 表

| 链 | 公共 RPC |
|----|----------|
| Ethereum | `https://eth.llamarpc.com` |
| BSC | `https://bsc-dataseed.binance.org/` |
| Polygon | `https://polygon-rpc.com/` |
| Arbitrum | `https://arb1.arbitrum.io/rpc` |
| Optimism | `https://mainnet.optimism.io` |
| Base | `https://mainnet.base.org` |
| Avalanche | `https://api.avax.network/ext/bc/C/rpc` |

更多 RPC 可查询 https://chainlist.org

---

## 完整改造示例

假设你要改成 Arbitrum 上的某个 `claim()` 合约：

**1. checkin.py 顶部改成：**

```python
CONTRACT_ADDRESS = "0x1234567890abcdef1234567890abcdef12345678"
METHOD_SELECTOR = "0x4e71d92d"  # claim()
CHAIN_ID = 42161
DEFAULT_RPC = "https://arb1.arbitrum.io/rpc"
```

**2. keys.txt 填入私钥（一行一个）：**

```
0xaaaa...
0xbbbb...
```

**3. .env 改 RPC（可选）：**

```env
BSC_RPC=https://arb1.arbitrum.io/rpc
```

**4. 运行：**

```bash
python checkin.py
```

---

## 注意事项

- **带参数的方法**：本脚本只支持无参数方法（如 `checkIn()`、`claim()`）。如果方法需要传参，需要额外编码 ABI 参数，那就不是简单改配置能解决的了
- **Gas 不足**：确保钱包里有该链的原生代币用于支付 Gas（BSC=BNB, ETH=ETH, Arbitrum=ETH）
- **交易失败**：可能是已经签到过了、不在签到时间窗口、或合约有其他前置条件
- **RPC 限流**：如果钱包很多（>10个），建议用付费 RPC 或者把 `DELAY_RANGE` 调大
