import base58
import hashlib
import math
from collections import Counter
from bech32 import bech32_encode, convertbits
from ecdsa import SigningKey, SECP256k1

# --- Funções auxiliares ---

def calculate_entropy(byte_vector): 
    total = len(byte_vector)
    counter = Counter(byte_vector)
    entropy = -sum((count / total) * math.log2(count / total) for count in counter.values())
    return entropy, entropy * total

def normalizar_array(array, target_length):
    carry = 0
    for i in range(len(array) - 1, 0, -1):
        array[i] += carry
        if array[i] > 255:
            excess = array[i] - 255
            array[i] = 255
            carry = excess
        else:
            carry = 0
    if array[0] > 255:
        excess = array[0] - 255
        array[0] = 255
        if len(array) > 1:
            array[1] += excess
    while len(array) < target_length:
        array.insert(0, 0)
    return array

def array_to_private_key(array):
    return bytes(array)

def private_key_compressed(private_key_bytes):
    return private_key_bytes[:32]

def private_key_to_wif_compressed(private_key_bytes):
    prefix = b'\x80'
    extended_key = prefix + private_key_bytes + b'\x01'
    checksum = hashlib.sha256(hashlib.sha256(extended_key).digest()).digest()[:4]
    wif_key = extended_key + checksum
    return base58.b58encode(wif_key).decode('utf-8')

def private_key_to_public_key(private_key_bytes):
    sk = SigningKey.from_string(private_key_bytes, curve=SECP256k1)
    vk = sk.get_verifying_key()
    x = vk.to_string()[:32]
    prefix = b'\x02' if vk.to_string()[32] % 2 == 0 else b'\x03'
    return prefix + x

def public_key_to_address(public_key):
    hash160 = hashlib.new('ripemd160', hashlib.sha256(public_key).digest()).digest()
    address = b'\x00' + hash160
    checksum = hashlib.sha256(hashlib.sha256(address).digest()).digest()[:4]
    return base58.b58encode(address + checksum).decode('utf-8')

def public_key_to_bech32_address(public_key):
    pubkey_hash = hashlib.new('ripemd160', hashlib.sha256(public_key).digest()).digest()
    words = convertbits(pubkey_hash, 8, 5)
    return bech32_encode("bc", words)

def public_key_to_p2sh_address(public_key):
    pubkey_hash = hashlib.new('ripemd160', hashlib.sha256(public_key).digest()).digest()
    redeem_script = b'\x00\x14' + pubkey_hash
    redeem_hash = hashlib.new('ripemd160', hashlib.sha256(redeem_script).digest()).digest()
    address = b'\x05' + redeem_hash
    checksum = hashlib.sha256(hashlib.sha256(address).digest()).digest()[:4]
    return base58.b58encode(address + checksum).decode('utf-8')

# --- Execução principal ---

if __name__ == "__main__":
    # Exemplo de lista de endereços
    addresses = [
        "1BoatSLRHtKNngkdXEeobR76b53LETtpyT",
        "3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy",
        "bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kygt080"
    ]

    max_consultas = 10000
    target_length = 32
    contador = 0
    i = 0

    while i < len(addresses) and contador < max_consultas:
        address = addresses[i]
        try:
            decoded = base58.b58decode_check(address)
            byte_vector = list(decoded)

            byte_vector = normalizar_array(byte_vector.copy(), target_length)

            entropy_avg, entropy_total = calculate_entropy(byte_vector)

            normalized_array = [x if x < 256 else 255 for x in byte_vector]

            private_key = array_to_private_key(normalized_array)
            compressed_private_key = private_key_compressed(private_key)
            wif_compressed = private_key_to_wif_compressed(compressed_private_key)
            public_key = private_key_to_public_key(compressed_private_key)

            btc_address = public_key_to_address(public_key)
            bech32_address = public_key_to_bech32_address(public_key)
            p2sh_address = public_key_to_p2sh_address(public_key)

            print(f"{wif_compressed} - {btc_address} - {p2sh_address} - {bech32_address}")

            addresses.pop(i)
            addresses.append(btc_address)
            contador += 1

        except Exception as e:
            print(f"Erro ao processar {address}: {e}")
            i += 1

    print(f"\nProcessamento concluído. {contador} endereços convertidos.")
