import csv

def count_bits(x):
    return bin(x).count('1')

max_k_global = 0
tabela = []

for n in range(1, 10):
    base = 2 ** n
    upper = 2 ** (n + 1) - 1
    intervalo = range(base, upper + 1)

    bits_info = {}  # k: [count, menor, maior]

    for num in intervalo:
        k = count_bits(num)
        if k not in bits_info:
            bits_info[k] = [1, num, num]
        else:
            bits_info[k][0] += 1
            bits_info[k][1] = min(bits_info[k][1], num)
            bits_info[k][2] = max(bits_info[k][2], num)

    max_k = max(bits_info.keys())
    max_k_global = max(max_k_global, max_k)

    # Soma dos mínimos, máximos e diferenças
    soma_minimos = sum(info[1] for info in bits_info.values())
    soma_maximos = sum(info[2] for info in bits_info.values())
    soma_diferencas = sum(info[2] - info[1] for info in bits_info.values())

    # Linha com ID, base, upper + as 3 novas colunas
    row = [
        f"{n}", f"{base}", f"{upper}",
        f"{soma_minimos}", f"{soma_maximos}", f"{soma_diferencas}"
    ]

    for k in range(max_k_global + 1):
        if k in bits_info:
            total, menor, maior = bits_info[k]
            diff = maior - menor
            row.extend([f"{total}", f"{menor}", f"{maior}", f"{diff}"])
        else:
            row.extend(["", "", "", ""])

    tabela.append(row)

# Cabeçalho
header = ["ID", "Início", "Fim", "Soma dos Mínimos", "Soma dos Máximos", "Soma das Diferenças"]
for k in range(max_k_global + 1):
    header.extend([
        f"{k} Total de Bits",
        f"{k} Bits Menor",
        f"{k} Bits Maior",
        f"{k} Bits Diferença"
    ])

# Salvar CSV
with open('tabela_bits_com_somas.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, delimiter=';')
    writer.writerow(header)
    writer.writerows(tabela)

print("✅ Arquivo 'tabela_bits_com_somas.csv' gerado com sucesso!")
