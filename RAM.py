import hashlib
import ecdsa
import os
import time
import random
from multiprocessing import Pool, cpu_count

# Replace with your target Bitcoin address
target_address = '98aMn6ZYAczwrE5NvNTUMyJ5qkfy4g3Hi'
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

def check_private_key(private_key):
    private_key_bytes = private_key.to_bytes(32, byteorder='big')
    address = generate_address(private_key_bytes)

    # Display the private key and generated address
    if random.random() < 0.001:  # Print occasionally to show progress
        print(f"Checking private key: {hex(private_key)[2:].rjust(64, '0')} - Address: {address}")

    if address == target_address:
        print(f"Private Key Found: {hex(private_key)[2:].rjust(64, '0')}")
        with open(save_file, 'w') as f:
            f.write(hex(private_key)[2:].rjust(64, '0'))
        return private_key

    return None

def run_key_search(total_keys):
    start_time = time.time()

    with Pool(processes=cpu_count()) as pool:
        while total_keys > 0:
            random_keys = [random.getrandbits(256) for _ in range(min(10000, total_keys))]
            results = pool.map(check_private_key, random_keys)
            found_keys = [key for key in results if key is not None]

            total_keys -= len(random_keys)
            if found_keys:
                break

    elapsed_time = time.time() - start_time
    keys_per_second = (total_keys - len(random_keys)) / elapsed_time if elapsed_time > 0 else 0
    print(f"Total keys checked: {total_keys}")
    print(f"Time taken: {elapsed_time:.2f} seconds")
    print(f"Keys per second: {keys_per_second:.2f}")

if __name__ == "__main__":
    total_keys_to_check = 100000000  # Example: 100 million keys
    print("Starting random key search...")
    run_key_search(total_keys_to_check)
