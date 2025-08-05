import hashlib
import base58
import ecdsa

def sha256(data):
    return hashlib.sha256(data).digest()

def ripemd160(data):
    h = hashlib.new('ripemd160')
    h.update(data)
    return h.digest()

def private_key_from_string(data_str):
    return sha256(data_str.encode('utf-8'))

def private_key_to_wif(private_key_bytes, compressed=True):
    prefix = b'\x80'
    extended_key = prefix + private_key_bytes
    if compressed:
        extended_key += b'\x01'
    checksum = sha256(sha256(extended_key))[:4]
    wif = base58.b58encode(extended_key + checksum)
    return wif.decode()

def pubkey_from_private(private_key_bytes, compressed=True):
    sk = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1)
    vk = sk.verifying_key

    if compressed:
        px = vk.to_string()[:32]
        py = vk.to_string()[32:]
        if py[-1] % 2 == 0:
            return b'\x02' + px
        else:
            return b'\x03' + px
    else:
        return b'\x04' + vk.to_string()

def hash160(data):
    return ripemd160(sha256(data))

def encode_base58_checksum(b):
    checksum = sha256(sha256(b))[:4]
    return base58.b58encode(b + checksum).decode()

def create_p2sh_address(redeem_script_hash160):
    prefix = b'\x05'  # P2SH mainnet
    payload = prefix + redeem_script_hash160
    return encode_base58_checksum(payload)

def create_redeem_script(pubkey_hash160):
    # Script: OP_DUP OP_HASH160 <pubkey_hash160> OP_EQUALVERIFY OP_CHECKSIG
    return b'\x76\xa9\x14' + pubkey_hash160 + b'\x88\xac'

if __name__ == "__main__":
    entrada = input("Digite a string para gerar o endereço e chave: ")

    # Deriva chave privada da string
    private_key = private_key_from_string(entrada)

    # WIF da chave privada
    wif = private_key_to_wif(private_key)

    # Gera chave pública comprimida
    pubkey = pubkey_from_private(private_key)

    # HASH160 da chave pública (pubkey hash)
    pubkey_hash160 = hash160(pubkey)

    # Redeem script (P2PKH script)
    redeem_script = create_redeem_script(pubkey_hash160)

    # HASH160 do redeem script
    redeem_script_hash160 = hash160(redeem_script)

    # Endereço P2SH
    endereco = create_p2sh_address(redeem_script_hash160)

    print(f"\nPara a string '{entrada}':")
    print(f"Chave privada (hex): {private_key.hex()}")
    print(f"WIF: {wif}")
    print(f"Endereço P2SH válido: {endereco}")
