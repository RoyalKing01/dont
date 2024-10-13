from coincurve import PrivateKey
from bitcoin import pubtoaddr
from multiprocessing import Pool, cpu_count
import os

def derive_compressed_address(hex_value):
    """ Generate compressed address from private key """
    private_key = PrivateKey.from_hex(hex_value)
    compressed_public_key = private_key.public_key.format(compressed=True)
    
    try:
        compressed_address = pubtoaddr(compressed_public_key, magicbyte=0)
    except Exception as e:
        print(f"Error generating address for key {hex_value}: {e}")
        compressed_address = None

    return hex_value, compressed_address

def search_in_chunk(args):
    """ Searches for the target address in a chunk of values """
    target_address, start_chunk, end_chunk = args
    for value in range(start_chunk, end_chunk):
        hex_value = format(value, 'x').zfill(64)
        hex_value, compressed_address = derive_compressed_address(hex_value)

        if compressed_address:
            # Print the private key and the generated compressed address
            print(f"Generated Address: {compressed_address} | Private Key: {hex_value}")
        
        # Check if the address matches the target
        if compressed_address == target_address:
            return hex_value, compressed_address

    return None, None

def iterate_values():
    target_addresses = [
        "1BY8GQbnueYofwSuFAT3USAhGjPrkxDdW9",  # Target address without extra space
    ]
    
    start_value = int("40000000000000000", 16)
    end_value = int("7ffffffffffffffff", 16)
    chunk_size = 10000000  # Smaller chunk size to distribute work across processes

    # Get the number of CPU cores
    num_cores = cpu_count()
    print(f"Using {num_cores} cores")

    for target_address in target_addresses:
        with Pool(num_cores) as pool:
            # Prepare the tasks for each chunk of the range
            tasks = [(target_address, start_chunk, min(start_chunk + chunk_size, end_value))
                     for start_chunk in range(start_value, end_value, chunk_size)]
            
            # Distribute the work across the cores and get the results
            for result in pool.imap_unordered(search_in_chunk, tasks):
                hex_value, compressed_address = result
                if compressed_address:
                    with open("matches.txt", "a") as file:
                        file.write(f"Hex Value: {hex_value}\nCompressed Address: {compressed_address}\n")
                    print(f"\nMatch found! Hex Value: {hex_value}, Compressed Address: {compressed_address}")
                    break

    print("\nSearch complete.")

# Run the search
if __name__ == '__main__':
    iterate_values()
