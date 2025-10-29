import csv
import hashlib
from ecdsa import SigningKey, SECP256k1
from Crypto.Hash import RIPEMD160
from base58 import b58encode

# Funções auxiliares
def pubkey_to_hash160(pubkey_hex):
    pk_bytes = bytes.fromhex(pubkey_hex)
    sha256 = hashlib.sha256(pk_bytes).digest()
    ripemd160 = RIPEMD160.new()
    ripemd160.update(sha256)
    return ripemd160.hexdigest()

def hash160_to_address(hash160_hex, version=0x00):
    hash160_bytes = bytes.fromhex(hash160_hex)
    versioned_payload = bytes([version]) + hash160_bytes
    checksum = hashlib.sha256(hashlib.sha256(versioned_payload).digest()).digest()[:4]
    return b58encode(versioned_payload + checksum).decode('utf-8')

def private_key_to_wif(d_n, compressed=True, version=0x80):
    key_bytes = d_n.to_bytes(32, byteorder='big')
    if compressed:
        key_bytes += b'\x01'
    payload = bytes([version]) + key_bytes
    checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    return b58encode(payload + checksum).decode('utf-8')

def derive_private_key(low_anchor, delta_low, use_even_delta=True):
    d_n = low_anchor + delta_low
    # Corrige paridade
    if use_even_delta and d_n % 2 != 0:
        d_n += 1
    elif not use_even_delta and d_n % 2 == 0:
        d_n += 1
    return d_n % SECP256k1.order

# Lê CSV
puzzles = []
with open("puzzles.csv", newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        puzzles.append({
            "n": int(row["n"]),
            "low_anchor": int(row["low_anchor"]),
            "delta_low": int(row["delta_low"]),
            "delta_even": row["delta_even"].strip().lower() == "true"
        })

# Gerar todas as 160 carteiras
for p in puzzles:
    d_n = derive_private_key(p["low_anchor"], p["delta_low"], use_even_delta=p["delta_even"])
    sk = SigningKey.from_secret_exponent(d_n, curve=SECP256k1)
    pk = sk.verifying_key.to_string("compressed").hex()
    hash160 = pubkey_to_hash160(pk)
    address = hash160_to_address(hash160)
    wif_compressed = private_key_to_wif(d_n, compressed=True)
    wif_uncompressed = private_key_to_wif(d_n, compressed=False)

    print(f"\nPuzzle #{p['n']} (delta {'even' if p['delta_even'] else 'odd'})")
    print(f"Private key: {hex(d_n)}")
    print(f"WIF compressed: {wif_compressed}")
    print(f"WIF uncompressed: {wif_uncompressed}")
    print(f"Public key: {pk}")
    print(f"hash160: {hash160}")
    print(f"Bitcoin Address (P2PKH): {address}")
