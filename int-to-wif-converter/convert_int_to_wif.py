import hashlib
import base58

def int_to_wif(n, compressed=True, mainnet=True):
    # 1. Converte para 32 bytes (big endian)
    private_key_bytes = n.to_bytes(32, byteorder='big')

    # 2. Adiciona prefixo (mainnet = 0x80)
    prefix = b'\x80' if mainnet else b'\xef'
    extended_key = prefix + private_key_bytes

    # 3. Adiciona sufixo (compressed = 0x01)
    if compressed:
        extended_key += b'\x01'

    # 4. SHA256 duas vezes para o checksum
    checksum = hashlib.sha256(hashlib.sha256(extended_key).digest()).digest()[:4]

    # 5. Concatena chave + checksum
    final_key = extended_key + checksum

    # 6. Codifica em Base58
    wif = base58.b58encode(final_key).decode()
    return wif

# Exemplo com o inteiro 83
wif_key = int_to_wif(83)
print(wif_key)
