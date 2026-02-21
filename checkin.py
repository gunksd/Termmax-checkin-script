import os
import sys
import time
import random
from dotenv import load_dotenv
from web3 import Web3

# ============================================================
# Configuration - modify these for different contracts/methods
# ============================================================
CONTRACT_ADDRESS = "0x007200C66bd2a5BD7c744b90dF8eCBEB34fd26d4"
METHOD_SELECTOR = "0x183ff085"  # checkIn()
CHAIN_ID = 56  # BSC Mainnet
DEFAULT_RPC = "https://bsc-dataseed.binance.org/"
DELAY_RANGE = (2, 5)  # random delay between wallets (seconds)
GAS_MULTIPLIER = 1.2  # buffer for gas estimation


def load_private_keys():
    keys_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "keys.txt")
    if not os.path.exists(keys_file):
        print(f"[ERROR] keys.txt not found")
        print(f"[INFO]  Create keys.txt with one private key per line")
        sys.exit(1)
    with open(keys_file, "r") as f:
        keys = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    if not keys:
        print("[ERROR] No private keys found in keys.txt")
        sys.exit(1)
    return keys


def checkin(w3, private_key, contract_address, method_selector):
    account = w3.eth.account.from_key(private_key)
    address = account.address
    nonce = w3.eth.get_transaction_count(address)

    tx = {
        "to": Web3.to_checksum_address(contract_address),
        "data": method_selector,
        "chainId": CHAIN_ID,
        "nonce": nonce,
        "gasPrice": w3.eth.gas_price,
    }

    try:
        gas_estimate = w3.eth.estimate_gas({"from": address, **tx})
        tx["gas"] = int(gas_estimate * GAS_MULTIPLIER)
    except Exception as e:
        print(f"  [WARN] Gas estimation failed: {e}, using default 200000")
        tx["gas"] = 200000

    signed = w3.eth.account.sign_transaction(tx, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
    return tx_hash.hex(), receipt["status"]


def main():
    load_dotenv()
    rpc_url = os.getenv("BSC_RPC", DEFAULT_RPC)
    w3 = Web3(Web3.HTTPProvider(rpc_url))

    if not w3.is_connected():
        print(f"[ERROR] Cannot connect to RPC: {rpc_url}")
        sys.exit(1)

    print(f"[INFO] Connected to chain ID {w3.eth.chain_id}")
    print(f"[INFO] Contract: {CONTRACT_ADDRESS}")
    print(f"[INFO] Method:   {METHOD_SELECTOR} (checkIn)")
    print()

    keys = load_private_keys()
    print(f"[INFO] Loaded {len(keys)} wallet(s)\n")

    success_count = 0
    fail_count = 0

    for i, key in enumerate(keys, 1):
        account = w3.eth.account.from_key(key)
        address = account.address
        print(f"[{i}/{len(keys)}] {address}")

        try:
            tx_hash, status = checkin(w3, key, CONTRACT_ADDRESS, METHOD_SELECTOR)
            if status == 1:
                print(f"  ✅ Success | TX: {tx_hash}")
                success_count += 1
            else:
                print(f"  ❌ Reverted | TX: {tx_hash}")
                fail_count += 1
        except Exception as e:
            print(f"  ❌ Failed  | Error: {e}")
            fail_count += 1

        if i < len(keys):
            delay = random.uniform(*DELAY_RANGE)
            print(f"  ⏳ Waiting {delay:.1f}s...")
            time.sleep(delay)

        print()

    print("=" * 50)
    print(f"[DONE] Success: {success_count} | Failed: {fail_count} | Total: {len(keys)}")


if __name__ == "__main__":
    main()
