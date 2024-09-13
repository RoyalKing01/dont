from coincurve import PrivateKey
from bitcoin import pubtoaddr
import ecdsa


def derive_compressed_address(hex_value):
    private_key = PrivateKey.from_hex(hex_value)
    
    
    compressed_public_key = private_key.public_key.format(compressed=True)
    compressed_address = pubtoaddr(compressed_public_key, magicbyte=0)

    return hex_value, compressed_address

def search_in_chunk(target_address, start_chunk, end_chunk):
    for value in range(start_chunk, end_chunk):
        hex_value, compressed_address = derive_compressed_address(format(value, 'x').zfill(64))
        
        if compressed_address == target_address:
            return hex_value, compressed_address

    return None, None

def iterate_values():
    target_addresses = [
"1BY8GQbnueYofwSuFAT3USAhGjPrkxDdW9",
"1MVDYgVaSN6iKKEsbzRUAYFrYJadLYZvvZ",
"19vkiEajfhuZ8bs8Zu2jgmC6oqZbWqhxhG",
"19YZECXj3SxEZMoUeJ1yiPsw8xANe7M7QR",
    ]
    
    start_value = int("0000000000000000000000000000000000000000000000040000000000000000", 16)
    end_value = int("  0000000000000000000000000000000000000000000000080000000000000000", 16)
    chunk_size = 1000000000000000000

    for target_address in target_addresses:
        for start_chunk in range(start_value, end_value, chunk_size):
            end_chunk = min(start_chunk + chunk_size, end_value)
            print(f"Searching for {target_address} in chunk {start_chunk} to {end_chunk}", end="\r")
            
            hex_value, compressed_address = search_in_chunk(target_address, start_chunk, end_chunk)
            if compressed_address:
                with open("matches.txt", "a") as file:
                    file.write(f"Hex Value: {hex_value}\nCompressed Address: {compressed_address}\n")
                print(f"Match found! Hex Value: {hex_value}, Compressed Address: {compressed_address}")
                break

    print("\nSearch complete.")


iterate_values()
