def gerar_sequencia(sementes, coef, tamanho):
    k = len(coef)
    seq = sementes[:]
    for i in range(len(sementes), tamanho):
        val = sum(coef[j] * seq[i - j - 1] for j in range(k))
        seq.append(val)
    return seq

def testar_modelos(indices_meio, coef_range=5, seed_range=10, max_k=4):
    for k in range(2, max_k + 1):  # número de coeficientes / sementes
        for c in range(coef_range ** k):
            coef = []
            x = c
            for _ in range(k):
                coef.append(x % coef_range)
                x //= coef_range
            if all(v == 0 for v in coef):  # pular vetor de coeficientes zerado
                continue

            for s in range(seed_range ** k):
                sementes = []
                y = s
                for _ in range(k):
                    sementes.append(y % seed_range)
                    y //= seed_range

                maior_indice = max(i for i, _ in indices_meio)
                seq = gerar_sequencia(sementes, coef, maior_indice + 1)

                if all(seq[i] == val for i, val in indices_meio):
                    return {
                        "k": k,
                        "coef": coef,
                        "sementes": sementes,
                        "sequencia": seq
                    }
    return None

# Dados fornecidos (início, meio, fim)
dados = [
    (1, 1, 1),
    (2, 3, 3),
    (4, 7, 7),
    (8, 8, 15),
    (16, 21, 31),
    (32, 49, 63),
]

# Índices e valores do meio
indices_meio = [(ini if ini == fim else (ini + fim) // 2, meio) for ini, meio, fim in dados]

# Rodar o algoritmo
resultado = testar_modelos(indices_meio, coef_range=6, seed_range=10, max_k=3)

# Previsão para linha 6 (índice 95)
if resultado:
    seq = gerar_sequencia(resultado['sementes'], resultado['coef'], 128)
    print("Coeficientes encontrados:", resultado['coef'])
    print("Sementes encontradas:", resultado['sementes'])
    print("Valor previsto para índice 95 (linha 6 - Meio):", seq[95])
else:
    print("Nenhum modelo válido encontrado.")
