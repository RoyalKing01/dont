import hashlib
import ecdsa
import os
import random
from multiprocessing import Pool

# Target addresses and save file
target_addresses = '9vkiEajfhuZ8bs8Zu2jgmC6oqZbWqhxhG'
save_file = 'private_key.txt'

# Generate Bitcoin address from private key bytes
def generate_address(private_key_bytes):
    # Generate the signing key
    private_key = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1)
    
    # Get the public key in bytes
    public_key = private_key.get_verifying_key().to_string()
    
    # Compress the public key
    if public_key[-1] % 2 == 0:
        compressed_public_key = b'\x02' + public_key[:32]
    else:
        compressed_public_key = b'\x03' + public_key[:32]
    
    # SHA256 hash of the compressed public key
    sha256_public_key = hashlib.sha256(compressed_public_key).digest()
    
    # RIPEMD160 hash of the SHA256 hash
    ripemd160_hash = hashlib.new('ripemd160', sha256_public_key).digest()
    
    # Add network byte (0x00 for Bitcoin mainnet)
    address_bytes = b'\x00' + ripemd160_hash
    
    # Perform SHA256(SHA256(address_bytes)) to get the checksum
    checksum = hashlib.sha256(hashlib.sha256(address_bytes).digest()).digest()[:4]
    
    # Final Bitcoin address is base58 encoded
    final_address = base58encode(int.from_bytes(address_bytes + checksum, 'big'))
    
    return final_address

# Base58 encoding
def base58encode(n):
    alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    result = ''
    while n > 0:
        n, remainder = divmod(n, 58)
        result = alphabet[remainder] + result
    return result

# Check if the private key matches any target address
def check_private_key(private_key):
    private_key_bytes = private_key.to_bytes(32, byteorder='big')
    address = generate_address(private_key_bytes)
    
    # Show the running private key and address being checked
    print(f"Checking key: {hex(private_key)[2:].rjust(64, '0')}, Address: {address}")
    
    if address in target_addresses:
        print(f"Private Key Found for {address}: {hex(private_key)[2:].rjust(64, '0')}")
        with open(save_file, 'w') as f:
            f.write(f"Address: {address}\nPrivate Key: {hex(private_key)[2:].rjust(64, '0')}\n")
        print(f"Private key saved to {save_file}.")
        return private_key
    return None

# Main logic with multiprocessing
if __name__ == "__main__":
    start = int("1fffffffffffffffff", 16)
    end = int("100000000000000000", 16)
    batch_size = 10000  # Adjust batch size as needed
    
    with Pool() as pool:
        while True:
            # Generate random keys to check in the given range
            keys_to_check = (random.randint(end, start) for _ in range(batch_size))
            
            # Check the keys in parallel
            results = pool.map(check_private_key, keys_to_check)
            found_keys = [key for key in results if key is not None]
            
            if found_keys:
                break  # Exit if a private key was found
