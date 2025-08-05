import hashlib
import base58
from ecdsa import SigningKey, SECP256k1
from bit.format import bytes_to_wif

# --- Funções Bech32 (BIP173) ---

CHARSET = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"

def bech32_polymod(values):
    GENERATORS = [0x3b6a57b2, 0x26508e6d,
                  0x1ea119fa, 0x3d4233dd, 0x2a1462b3]
    chk = 1
    for v in values:
        b = (chk >> 25)
        chk = ((chk & 0x1ffffff) << 5) ^ v
        for i in range(5):
            if ((b >> i) & 1):
                chk ^= GENERATORS[i]
    return chk

def bech32_hrp_expand(hrp):
    return [ord(x) >> 5 for x in hrp] + [0] + [ord(x) & 31 for x in hrp]

def bech32_create_checksum(hrp, data):
    values = bech32_hrp_expand(hrp) + data
    polymod = bech32_polymod(values + [0,0,0,0,0,0]) ^ 1
    return [(polymod >> 5 * (5 - i)) & 31 for i in range(6)]

def bech32_encode(hrp, data):
    combined = data + bech32_create_checksum(hrp, data)
    return hrp + '1' + ''.join([CHARSET[d] for d in combined])

def convertbits(data, frombits, tobits, pad=True):
    acc = 0
    bits = 0
    ret = []
    maxv = (1 << tobits) - 1
    for value in data:
        if value < 0 or (value >> frombits):
            return None
        acc = (acc << frombits) | value
        bits += frombits
        while bits >= tobits:
            bits -= tobits
            ret.append((acc >> bits) & maxv)
    if pad:
        if bits:
            ret.append((acc << (tobits - bits)) & maxv)
    elif bits >= frombits or ((acc << (tobits - bits)) & maxv):
        return None
    return ret

# --- Funções para gerar endereços ---

def p2wpkh_address(pubkey_bytes):
    pubkey_hash = hashlib.new('ripemd160', hashlib.sha256(pubkey_bytes).digest()).digest()
    data = [0] + convertbits(pubkey_hash, 8, 5)
    return bech32_encode('bc', data)

def p2sh_p2wpkh_address(pubkey_bytes):
    pubkey_hash = hashlib.new('ripemd160', hashlib.sha256(pubkey_bytes).digest()).digest()
    redeem_script = b'\x00\x14' + pubkey_hash
    redeem_script_hash = hashlib.new('ripemd160', hashlib.sha256(redeem_script).digest()).digest()
    prefix = b'\x05'  # P2SH mainnet prefix
    address_bytes = prefix + redeem_script_hash
    checksum = hashlib.sha256(hashlib.sha256(address_bytes).digest()).digest()[:4]
    return base58.b58encode(address_bytes + checksum).decode()

def pubkey_to_legacy_address(pubkey_bytes):
    pubkey_hash = hashlib.new('ripemd160', hashlib.sha256(pubkey_bytes).digest()).digest()
    prefix = b'\x00'  # P2PKH mainnet prefix
    payload = prefix + pubkey_hash
    checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    return base58.b58encode(payload + checksum).decode()

# --- Main script ---

# Ordem do grupo secp256k1
n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

# Sua private key decimal (exemplo)
privkey_int = 13407807929942597099574024998205846127479365820592393377723561443721764030073546976801874298166903427690031858186486050853753882811946569946433649006084095

# Reduz modulo n para garantir validade
privkey_int = privkey_int % n

# Converte para bytes (32 bytes big endian)
private_key_bytes = privkey_int.to_bytes(32, 'big')

print(f"🔐 Private key hex: {private_key_bytes.hex()}")

# Cria a chave ECDSA
sk = SigningKey.from_string(private_key_bytes, curve=SECP256k1)
vk = sk.verifying_key

x = vk.pubkey.point.x()
y = vk.pubkey.point.y()

# Public key comprimida
prefix = b'\x02' if y % 2 == 0 else b'\x03'
compressed_pubkey_bytes = prefix + x.to_bytes(32, 'big')

# Public key não comprimida
uncompressed_pubkey_bytes = b'\x04' + x.to_bytes(32, 'big') + y.to_bytes(32, 'big')

# WIF (Wallet Import Format)
wif_compressed = bytes_to_wif(private_key_bytes, compressed=True)
wif_uncompressed = bytes_to_wif(private_key_bytes, compressed=False)

# Endereços legacy
legacy_compressed = pubkey_to_legacy_address(compressed_pubkey_bytes)
legacy_uncompressed = pubkey_to_legacy_address(uncompressed_pubkey_bytes)

# Endereços SegWit
segwit_native = p2wpkh_address(compressed_pubkey_bytes)
segwit_compat = p2sh_p2wpkh_address(compressed_pubkey_bytes)

# Imprime resultados
print(f"🔐 WIF Compressed:     {wif_compressed}")
print(f"🔐 WIF Uncompressed:   {wif_uncompressed}")
print()
print(f"🏷️ Legacy (compressed):      {legacy_compressed}")
print(f"🏷️ Legacy (uncompressed):    {legacy_uncompressed}")
print(f"🏷️ P2WPKH-in-P2SH (compat):  {segwit_compat}")
print(f"🏷️ Native SegWit (P2WPKH):   {segwit_native}")
