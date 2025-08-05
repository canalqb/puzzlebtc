import csv
from decimal import Decimal, getcontext

# Alta precisão
getcontext().prec = 50

# Abrir o arquivo
with open("decimais.txt", "r") as f:
    linhas = f.readlines()

# Lista para os resultados
resultados = []

for linha in linhas:
    linha = linha.strip()
    if not linha:
        continue

    partes = [p.strip() for p in linha.split(",")]

    # Checar se algum valor é 'None'
    if 'None' in partes:
        resultados.append([
            f"'{partes[0] if partes[0] != 'None' else 'None'}",
            f"'{partes[2] if len(partes) > 2 and partes[2] != 'None' else 'None'}",
            f"'{partes[1] if partes[1] != 'None' else 'None'}",
            "'None",  # Intervalo
            "'None",  # Blocos_255
            "'None"   # Proporcao
        ])
        continue

    # Caso não tenha 'None', processa normalmente
    start = int(partes[0])
    steps = int(partes[1])
    end = int(partes[2])

    intervalo = end - start + 1
    blocos_255 = intervalo / 255
    proporcao = Decimal(steps) / Decimal(intervalo)

    resultados.append([
        f"'{start}",
        f"'{end}",
        f"'{steps}",
        f"'{intervalo}",
        f"'{blocos_255}",
        f"'{proporcao}"
    ])

# Escrever CSV
with open("saida.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile, delimiter=';')
    writer.writerow(["'Inicio", "'Fim", "'Passos", "'Intervalo", "'Blocos_255", "'Proporcao"])
    writer.writerows(resultados)

print("✅ Arquivo 'saida.csv' gerado com sucesso, incluindo linhas com 'None'.")
