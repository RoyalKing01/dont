import hashlib
import ecdsa
import os
import time
from multiprocessing import Pool, cpu_count

# Replace with your target Bitcoin address
target_address = '4iXhn8bGajVWegZHJ18vJLHhntcpL4dex'
save_file = 'private_key.txt'
state_file = 'state.txt'

def generate_address(private_key_bytes):
    private_key = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1)
    public_key = private_key.get_verifying_key().to_string()
    compressed_public_key = (b'\x02' + public_key[:32]) if public_key[-1] % 2 == 0 else (b'\x03' + public_key[:32])
    public_key_hash = hashlib.sha256(compressed_public_key).digest()
    public_key_hash = hashlib.new('ripemd160', public_key_hash).digest()
    address_bytes = b'\x00' + public_key_hash
    checksum = hashlib.sha256(hashlib.sha256(address_bytes).digest()).digest()[:4]
    address = base58encode(int.from_bytes(address_bytes + checksum, 'big'))
    return address

def base58encode(n):
    alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    result = ''
    while n > 0:
        n, remainder = divmod(n, 58)
        result = alphabet[remainder] + result
    return result

def save_state(last_checked_key):
    with open(state_file, 'w') as f:
        f.write(str(last_checked_key))

def load_state():
    if os.path.exists(state_file):
        with open(state_file, 'r') as f:
            return int(f.read().strip())
    else:
        return None

def check_private_key(private_key):
    private_key_bytes = private_key.to_bytes(32, byteorder='big')
    address = generate_address(private_key_bytes)

    # Occasionally print progress
    if private_key % 1000000 == 0:
        print(f"Checking private key: {hex(private_key)[2:].rjust(64, '0')} - Address: {address}")

    if address == target_address:
        print(f"Private Key Found: {hex(private_key)[2:].rjust(64, '0')}")
        with open(save_file, 'w') as f:
            f.write(hex(private_key)[2:].rjust(64, '0'))
        return private_key

    return None

def run_key_search(start, end, batch_size):
    last_checked_key = load_state() or start

    with Pool(processes=cpu_count()) as pool:
        for i in range(last_checked_key, end - 1, -batch_size):
            private_keys = range(i, max(i - batch_size, end), -1)
            results = pool.map(check_private_key, private_keys)
            found_keys = [key for key in results if key is not None]
            if found_keys:
                break
            save_state(i)

if __name__ == "__main__":
    start = int("7fffffff", 16)  # 4194304 (400000 in hex)
    end = int("400000", 16)      # Smaller range to avoid overflow
    batch_size = 10000           # Adjust batch size for optimal performance

    print("Starting sequential key search...")
    run_key_search(start, end, batch_size)
