import random
from bit import Key

def to_base(n, base, symbols):
    if n == 0:
        return symbols[0]
    digits = []
    while n > 0:
        digits.append(symbols[n % base])
        n //= base
    return ''.join(reversed(digits))

base2_symbols = '01'
base16_symbols = '0123456789ABCDEF'
base32_symbols = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567'
base58_symbols = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
base62_symbols = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
base85_symbols = ''.join(chr(i) for i in range(33, 118))

bases = [
    ("Base 2", 2, base2_symbols),
    ("Base 16", 16, base16_symbols),
    ("Base 32", 32, base32_symbols),
    ("Base 58", 58, base58_symbols),
    ("Base 62", 62, base62_symbols),
    ("Base 85", 85, base85_symbols),
]

for n in range(50, 162):
    inicio = 2**n
    fim = 2**(n+1) - 1
    numero_aleatorio = random.randint(inicio, fim)
    key = Key.from_int(numero_aleatorio)
    wif = key.to_wif()

    def converter_todas_bases(valor):
        return ', '.join(to_base(valor, base, symbols) for _, base, symbols in bases)

    print(f"intervalo {n}") 
    print(f"numeroaleatorio {wif} - {converter_todas_bases(numero_aleatorio)}") 

#0000000000000000000000000000000000000000000000000000000000000001
