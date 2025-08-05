import hashlib
import random

BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

def base58_encode(b):
    n = 0
    for byte in b:
        n = n * 256 + byte
    
    result = ''
    while n > 0:
        n, r = divmod(n, 58)
        result = BASE58_ALPHABET[r] + result
    
    for byte in b:
        if byte == 0:
            result = '1' + result
        else:
            break
    return result

def int_to_32bytes(n):
    b = [0]*32
    i = 31
    while n > 0 and i >= 0:
        b[i] = n & 0xFF
        n = n >> 8
        i -= 1
    return bytes(b)

def wif_compressed(priv_int):
    priv_bytes = int_to_32bytes(priv_int)
    extended = b'\x80' + priv_bytes + b'\x01'
    first_hash = hashlib.sha256(extended).digest()
    second_hash = hashlib.sha256(first_hash).digest()
    checksum = second_hash[:4]
    full = extended + checksum
    return base58_encode(full)

def main():
    start = 2**71
    end = 2**72 - 1
    N = 1000  # quantas chaves aleatórias gerar

    for _ in range(N):
        priv = random.randint(start, end)
        wif = wif_compressed(priv)
        print(f"{priv}: {wif}")

if __name__ == "__main__":
    main()
