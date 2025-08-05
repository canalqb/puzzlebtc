import csv
import math
import time

# Lista de valores
meio_values = [
    '1', '3', '7', '8', '21', '49', '76', '224', '467', '514',
    '1155', '2683', '5216', '10544', '26867', '51510', '95823',
    '198669', '357535', '863317', '1811764', '3007503', '5598802',
    '14428676', '33185509', '54538862', '111949941', '227634408',
    '400708894', '1033162084', '2102388551', '3093472814',
    '7137437912', '14133072157', '20112871792', '42387769980',
    '100251560595', '146971536592', '323724968937',
    '1003651412950', '1458252205147', '2895374552463',
    '7409811047825', '15404761757071', '19996463086597',
    '51408670348612', '119666659114170', '191206974700443',
    '409118905032525', '611140496167764', '2058769515153876',
    '4216495639600700', '6763683971478124', '9974455244496707',
    '30045390491869460', '44218742292676575', '138245758910846492',
    '199976667976342049', '525070384258266191', '1135041350219496382',
    '1425787542618654982', '3908372542507822062', '8993229949524469768',
    '17799667357578236628', '30568377312064202855', '46346217550346335726',
    '132656943602386256302', '219898266213316039825', '297274491920375905804',
    '970436974005023690481', None, None, None, None,
    '22538323240989823823367', None, None, None, None,
    '1105520030589234487939456', None, None, None, None,
    '21090315766411506144426920', None, None, None, None,
    '868012190417726402719548863', None, None, None, None,
    '25525831956644113617013748212', None, None, None, None,
    '868221233689326498340379183142', None, None, None, None,
    '29083230144918045706788529192435', None, None, None, None,
    '1090246098153987172547740458951748', None, None, None, None,
    '31464123230573852164273674364426950', None, None, None, None,
    '919343500840980333540511050618764323', None, None, None, None,
    '37650549717742544505774009877315221420', None, None, None, None,
    '1103873984953507439627945351144005829577',
]
 
def is_prime_optimized(n):
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    for i in range(5, int(n ** 0.5) + 1, 6):
        if n % i == 0 or n % (i + 2) == 0:
            return False
    return True

def find_min_max_with_k_bits_ultra_fast(base, upper, k):
    """
    Versão ultra otimizada usando fórmulas matemáticas diretas.
    Calcula o menor e maior número com k bits ativos no intervalo [base, upper].
    """
    if k == 0:
        return (0 if base <= 0 <= upper else '', 0 if base <= 0 <= upper else '')
    
    # Número total de bits necessários para representar upper
    n_bits = upper.bit_length()
    
    if k > n_bits:
        return ('', '')
    
    # MENOR número com k bits ativos:
    # O menor número possível com k bits ativos é (2^k - 1)
    menor = (1 << k) - 1
    
    # Se menor < base, precisamos encontrar o próximo número >= base com k bits
    if menor < base:
        # Estratégia: usar a representação binária de base para construir
        # o menor número >= base com k bits ativos
        
        # Contar quantos bits base já tem
        base_bits = bin(base).count('1')
        
        if base_bits == k:
            menor = base
        elif base_bits < k:
            # Precisamos adicionar (k - base_bits) bits
            # Estratégia: adicionar bits nas posições menos significativas disponíveis
            temp = base
            bits_to_add = k - base_bits
            pos = 0
            while bits_to_add > 0 and temp <= upper:
                if not (temp & (1 << pos)):  # Se o bit na posição pos não está setado
                    temp |= (1 << pos)
                    bits_to_add -= 1
                pos += 1
            menor = temp if temp <= upper and bin(temp).count('1') == k else ''
        else:
            # base_bits > k, precisamos remover bits
            # Estratégia: remover bits menos significativos
            temp = base
            bits_to_remove = base_bits - k
            pos = 0
            while bits_to_remove > 0 and temp >= base:
                if temp & (1 << pos):  # Se o bit na posição pos está setado
                    temp &= ~(1 << pos)
                    bits_to_remove -= 1
                pos += 1
            
            # Se temp < base após remoção, precisamos de uma abordagem diferente
            if temp < base:
                # Buscar o próximo número >= base com k bits
                # Para simplificar, usar busca limitada
                menor = ''
                for candidate in range(base, min(upper + 1, base + 100000)):
                    if bin(candidate).count('1') == k:
                        menor = candidate
                        break
            else:
                menor = temp if bin(temp).count('1') == k else ''
    
    if menor > upper:
        menor = ''
    
    # MAIOR número com k bits ativos:
    # Estratégia: colocar k bits nas posições mais significativas possíveis
    # dentro do limite upper
    
    # Começar com os k bits mais significativos
    maior = sum(1 << (n_bits - 1 - i) for i in range(k))
    
    # Se maior > upper, precisamos ajustar
    if maior > upper:
        # Estratégia: usar a representação binária de upper para construir
        # o maior número <= upper com k bits ativos
        
        upper_bits = bin(upper).count('1')
        
        if upper_bits == k:
            maior = upper
        elif upper_bits > k:
            # Precisamos remover (upper_bits - k) bits
            # Estratégia: remover bits menos significativos
            temp = upper
            bits_to_remove = upper_bits - k
            pos = 0
            while bits_to_remove > 0:
                if temp & (1 << pos):  # Se o bit na posição pos está setado
                    temp &= ~(1 << pos)
                    bits_to_remove -= 1
                pos += 1
            maior = temp if temp >= base and bin(temp).count('1') == k else ''
        else:
            # upper_bits < k, precisamos adicionar bits
            # Mas não podemos ultrapassar upper, então buscar o maior possível
            maior = ''
            for candidate in range(upper, max(base - 1, upper - 100000), -1):
                if bin(candidate).count('1') == k:
                    maior = candidate
                    break
    
    if maior < base:
        maior = ''
    
    return (menor if menor != '' else '', maior if maior != '' else '')

headers = [
    'ID',
    '2^ID',
    'decimal',
    '2^(ID+1)-1',
    'Total de Bits',
    'A = decimal * bits',
    'B = bits / decimal',
    'A / B',
    'Potência de 2?',
    'Bit mais significativo (MSB)',
    'Bit menos significativo (LSB)',
    'n % 2^ID (mod rápido)',
    'Binário com padding',
    'Distância do início',
    'Distância do fim',
    '% entre início e fim',
    'Paridade de bits',
    'É primo?',
    'Meio aritmético',
    'Meio inferior',
    'Meio superior',
    'Média de bits no intervalo',
    'n & ex (AND)',
    'n | ex (OR)',
    'n ^ ex (XOR)',
    '~n (NOT)',
    'n << 1 (shift left)', 
    'n >> 1 (shift right)',
    'Menor com mesmo total de bits',
    'Maior com mesmo total de bits'
]

rows = []
start_time = time.time()

for val in meio_values:
    if val in (None, '', 'None'):
        rows.append(["''"] * len(headers))
        continue

    n = int(val)
    id_val = n.bit_length() - 1
    base = 2 ** id_val
    upper = (2 ** (id_val + 1)) - 1
    interval_size = upper - base + 1
    bit_count = bin(n).count('1')

    col_a = n * bit_count
    col_b = bit_count / n if n != 0 else 0
    col_c = col_a / col_b if col_b != 0 else 0
    is_pow2 = int(n > 0 and (n & (n - 1)) == 0)
    msb = id_val
    lsb = int(math.log2(n & -n)) if n != 0 else -1
    mod_pot = n & (2 ** id_val - 1)
    padded_bin = format(n, f'0{id_val + 1}b')
    dist_inicio = n - base
    dist_fim = upper - n
    pos_perc = (n - base) / (upper - base) if upper > base else 0
    bit_parity = 'par' if bit_count % 2 == 0 else 'ímpar'
    is_prime_flag = int(is_prime_optimized(n))

    meio_aritmetico = (base + upper) / 2
    meio_inferior = (base + upper) // 2
    meio_superior = (base + upper + 1) // 2

    total_bits_optimized = (id_val + 1) * (2 ** id_val)
    media_bits = total_bits_optimized / interval_size

    ex = (base + upper) // 2

    bit_and = n & ex
    bit_or = n | ex
    bit_xor = n ^ ex
    bit_not = ~n
    shift_left = n << 1
    shift_right = n >> 1

    # ULTRA OTIMIZAÇÃO: Fórmulas matemáticas diretas
    menor_mesmos_bits, maior_mesmos_bits = find_min_max_with_k_bits_ultra_fast(base, upper, bit_count)
    
    print(f'menor {menor_mesmos_bits} | {val} | maior {maior_mesmos_bits}')

    row = [
        id_val,
        base,
        n,
        upper,
        bit_count,
        col_a,
        f"{col_b:.9f}".replace('.', ','),
        int(col_c),
        is_pow2,
        msb,
        lsb,
        mod_pot,
        padded_bin,
        dist_inicio,
        dist_fim,
        f"{pos_perc:.5f}".replace('.', ','),
        bit_parity,
        is_prime_flag,
        f"{meio_aritmetico:.3f}".replace('.', ','),
        meio_inferior,
        meio_superior,
        f"{media_bits:.3f}".replace('.', ','),
        bit_and,
        bit_or,
        bit_xor,
        bit_not,
        shift_left,
        shift_right,
        menor_mesmos_bits,
        maior_mesmos_bits
    ]

    row_formatted = [f"'{str(col)}" for col in row]
    rows.append(row_formatted)

# Salvar CSV
with open('meios_completo_dinamico_ultra_otimizado.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, delimiter=';')
    writer.writerow([f"'{h}" for h in headers])
    writer.writerows(rows)

end_time = time.time()
print(f"⏱️ Tempo de execução: {end_time - start_time:.2f} segundos")
print("✅ CSV 'meios_completo_dinamico_ultra_otimizado.csv' gerado com sucesso!")

