import hashlib
import ecdsa
import os
from multiprocessing import Pool

target_address = '3zb1hQbWVsc2S7ZTZnP2G4undNNpdh5so'
save_file = 'private_key.txt'
state_file = 'state.txt'

def generate_address(private_key_bytes):
    private_key = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1)
    public_key = private_key.get_verifying_key().to_string()
    compressed_public_key = b'\x02' + public_key[:32] if public_key[-1] % 2 == 0 else b'\x03' + public_key[:32]
    public_key_hash = hashlib.sha256(compressed_public_key).digest()
    public_key_hash = hashlib.new('ripemd160', public_key_hash).digest()
    address_bytes = b'\x00' + public_key_hash
    checksum = hashlib.sha256(hashlib.sha256(address_bytes).digest()).digest()[:4]
    address = '1' * address_bytes[:0].count(b'\x00') + base58encode(int.from_bytes(address_bytes + checksum, 'big'))
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
    print(f"Checking private key: {hex(private_key)[2:].rjust(64, '0')} - Address: {address}")

    if address == target_address:
        print(f"Private Key Found: {hex(private_key)[2:].rjust(64, '0')}")
        with open(save_file, 'w') as f:
            f.write(hex(private_key)[2:].rjust(64, '0'))
        print("Private key saved to private_key.txt.")
        return private_key

    return None

if __name__ == "__main__":
    start = int("3ffffffffffffffff", 16)
    end = int("20000000000000000", 16)
    batch_size = 10000

    last_checked_key = load_state()
    if last_checked_key is None:
        last_checked_key = start

    with Pool() as pool:
        for i in range(last_checked_key, end - 1, -batch_size):
            private_keys = range(i, max(i - batch_size, end), -1)
            results = pool.map(check_private_key, private_keys)
            found_keys = [key for key in results if key is not None]
            if found_keys:
                break
            save_state(i)

    if not found_keys:
        print("Private key not found within the specified range.")
