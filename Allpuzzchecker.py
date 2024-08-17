from coincurve import PrivateKey
from bitcoin import pubtoaddr
import ecdsa
from multiprocessing import Pool

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
"1BgGZ9tcN4rm9KBzDn7KprQz87SZ26SAMH",
"1CUNEBjYrCn2y1SdiUMohaKUi4wpP326Lb",
"19ZewH8Kk1PDbSNdJ97FP4EiCjTRaZMZQA",
"1EhqbyUMvvs7BfL8goY6qcPbD6YKfPqb7e",
"1E6NuFjCi27W5zoXg8TRdcSRq84zJeBW3k",
"1PitScNLyp2HCygzadCh7FveTnfmpPbfp8",
"1McVt1vMtCC7yn5b9wgX1833yCcLXzueeC",
"1M92tSqNmQLYw33fuBvjmeadirh1ysMBxK",
"1CQFwcjw1dwhtkVWBttNLDtqL7ivBonGPV",
"1LeBZP5QCwwgXRtmVUvTVrraqPUokyLHqe",
"1PgQVLmst3Z314JrQn5TNiys8Hc38TcXJu",
"1DBaumZxUkM4qMQRt2LVWyFJq5kDtSZQot",
"1Pie8JkxBT6MGPz9Nvi3fsPkr2D8q3GBc1",
"1ErZWg5cFCe4Vw5BzgfzB74VNLaXEiEkhk",
"1QCbW9HWnwQWiQqVo5exhAnmfqKRrCRsvW",
"1BDyrQ6WoF8VN3g9SAS1iKZcPzFfnDVieY",
"1HduPEXZRdG26SUT5Yk83mLkPyjnZuJ7Bm",
"1GnNTmTVLZiqQfLbAdp9DVdicEnB5GoERE",
"1NWmZRpHH4XSPwsW6dsS3nrNWfL1yrJj4w",
"1HsMJxNiV7TLxmoF6uJNkydxPFDog4NQum",
"14oFNXucftsHiUMY8uctg6N487riuyXs4h",
"1CfZWK1QTQE3eS9qn61dQjV89KDjZzfNcv",
"1L2GM8eE7mJWLdo3HZS6su1832NX2txaac",
"1rSnXMr63jdCuegJFuidJqWxUPV7AtUf7",
"15JhYXn6Mx3oF4Y7PcTAv2wVVAuCFFQNiP",
"1JVnST957hGztonaWK6FougdtjxzHzRMMg",
"128z5d7nN7PkCuX5qoA4Ys6pmxUYnEy86k",
"12jbtzBb54r97TCwW3G1gCFoumpckRAPdY",
"19EEC52krRUK1RkUAEZmQdjTyHT7Gp1TYT",
"1LHtnpd8nU5VHEMkG2TMYYNUjjLc992bps",
"1LhE6sCTuGae42Axu1L1ZB7L96yi9irEBE",
"1FRoHA9xewq7DjrZ1psWJVeTer8gHRqEvR",
"187swFMjz1G54ycVU56B7jZFHFTNVQFDiu",
"1PWABE7oUahG2AFFQhhvViQovnCr4rEv7Q",
"1Be2UF9NLfyLFbtm3TCbmuocc9N1Kduci1",
"14iXhn8bGajVWegZHJ18vJLHhntcpL4dex",
"1HBtApAFA9B2YZw3G2YKSMCtb3dVnjuNe2",
"122AJhKLEfkFBaGAd84pLp1kfE7xK3GdT8",
"1EeAxcprB2PpCnr34VfZdFrkUWuxyiNEFv",
"1L5sU9qvJeuwQUdt4y1eiLmquFxKjtHr3E",
"1E32GPWgDyeyQac4aJxm9HVoLrrEYPnM4N",
"1PiFuqGpG8yGM5v6rNHWS3TjsG6awgEGA1",
"1CkR2uS7LmFwc3T2jV8C1BhWb5mQaoxedF",
"1NtiLNGegHWE3Mp9g2JPkgx6wUg4TW7bbk",
"1F3JRMWudBaj48EhwcHDdpeuy2jwACNxjP",
"1Pd8VvT49sHKsmqrQiP61RsVwmXCZ6ay7Z",
"1DFYhaB2J9q1LLZJWKTnscPWos9VBqDHzv",
"12CiUhYVTTH33w3SPUBqcpMoqnApAV4WCF",
"1MEzite4ReNuWaL5Ds17ePKt2dCxWEofwk",
"1NpnQyZ7x24ud82b7WiRNvPm6N8bqGQnaS",
"15z9c9sVpu6fwNiK7dMAFgMYSK4GqsGZim",
"15K1YKJMiJ4fpesTVUcByoz334rHmknxmT",
"1KYUv7nSvXx4642TKeuC2SNdTk326uUpFy",
"1LzhS3k3e9Ub8i2W1V8xQFdB8n2MYCHPCa",
"17aPYR1m6pVAacXg1PTDDU7XafvK1dxvhi",
"15c9mPGLku1HuW9LRtBf4jcHVpBUt8txKz",
"1Dn8NF8qDyyfHMktmuoQLGyjWmZXgvosXf",
"1HAX2n9Uruu9YDt4cqRgYcvtGvZj1rbUyt",
"1Kn5h2qpgw9mWE5jKpk8PP4qvvJ1QVy8su",
"1AVJKwzs9AskraJLGHAZPiaZcrpDr1U6AB",
"1Me6EfpwZK5kQziBwBfvLiHjaPGxCKLoJi",
"1NpYjtLira16LfGbGwZJ5JbDPh3ai9bjf4",
"16jY7qLJnxb7CHZyqBP8qca9d51gAjyXQN",
"18ZMbwUFLMHoZBbfpCjUJQTCMCbktshgpe",
"13zb1hQbWVsc2S7ZTZnP2G4undNNpdh5so",
"1BY8GQbnueYofwSuFAT3USAhGjPrkxDdW9",
"1MVDYgVaSN6iKKEsbzRUAYFrYJadLYZvvZ",
"19vkiEajfhuZ8bs8Zu2jgmC6oqZbWqhxhG",
"19YZECXj3SxEZMoUeJ1yiPsw8xANe7M7QR",
    ]
    
    start_value = int("0000000000000000000000000000000000000000000000000000000000000001", 16)
    end_value = int("0000000000000000000000000000000000000000000000040000000000000000", 16)
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
