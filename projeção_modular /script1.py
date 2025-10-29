# Tabela fornecida: (2^n, valor, mersenne)
dados = [
    (2, 3, 3),
    (4, 7, 7),
    (8, 8, 15),
    (16, 21, 31),
    (32, 49, 63),
    (64, 76, 127),
    (128, 224, 255),
    (256, 467, 511),
    (512, 514, 1023),
    (1024, 1155, 2047),
    (2048, 2683, 4095),
    (4096, 5216, 8191),
    (8192, 10544, 16383),
    (16384, 26867, 32767),
    (32768, 51510, 65535),
    (65536, 95823, 131071),
    (131072, 198669, 262143),
    (262144, 357535, 524287),
    (524288, 863317, 1048575),
    (1048576, 1811764, 2097151),
    (2097152, 3007503, 4194303),
    (4194304, 5598802, 8388607),
    (8388608, 14428676, 16777215),
    (16777216, 33185509, 33554431),
    (33554432, 54538862, 67108863),
    (67108864, 111949941, 134217727),
    (134217728, 227634408, 268435455),
    (268435456, 400708894, 536870911),
    (536870912, 1033162084, 1073741823)
]

# Cabeçalho da tabela
print(f"{'2^n':>12} | {'valor':>15} | {'mersenne':>15} | {'predição':>15} | {'Δ':>10} | {'Curva (%)':>12}")
print("-" * 90)

# Loop para calcular predição, diferença e curva percentual
for i in range(1, len(dados)):
    pot, valor, mersenne = dados[i]
    pot_ant, valor_ant, _ = dados[i - 1]

    # cálculo modular teórico
    pred = pot + (valor_ant % pot)
    diff = valor - pred
    curva = (diff / valor) * 100

    print(f"{pot:>12} | {valor:>15} | {mersenne:>15} | {pred:>15} | {diff:>10} | {curva:>11.2f}%")

# prever o próximo valor (2^31)
ultimo_pot, ultimo_valor, _ = dados[-1]
proximo_pot = ultimo_pot * 2
pred_proximo = proximo_pot + (ultimo_valor % proximo_pot)

print("\nPróximo valor previsto:")
print(f"2^31 = {proximo_pot:,} → previsão ≈ {pred_proximo:,}")
