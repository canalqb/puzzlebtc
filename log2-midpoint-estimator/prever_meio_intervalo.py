import numpy as np
import pandas as pd

# Dados fornecidos: (inicio, meio_esperado, fim)
dados = [
    (64, 76, 127),
    (128, 224, 255),
    (256, 467, 511),
    (512, 514, 1023),
    (1024, 1155, 2047),
]

# Tentar relacionar o valor do meio com os logaritmos dos limites
resultados = []
for inicio, meio, fim in dados:
    intervalo = fim - inicio
    meio_rel = (meio - inicio) / intervalo  # valor normalizado
    log2_inicio = np.log2(inicio)
    log2_fim = np.log2(fim)
    log2_range = log2_fim - log2_inicio
    log256_inicio = np.log(inicio) / np.log(256)
    log256_fim = np.log(fim) / np.log(256)
    log256_range = log256_fim - log256_inicio

    resultados.append({
        'inicio': inicio,
        'fim': fim,
        'meio': meio,
        'meio_rel': meio_rel,
        'log2_inicio': log2_inicio,
        'log2_fim': log2_fim,
        'log2_range': log2_range,
        'log256_inicio': log256_inicio,
        'log256_fim': log256_fim,
        'log256_range': log256_range,
    })

df = pd.DataFrame(resultados)
print(df)

import numpy as np

X = np.array([
    [row['log2_inicio'], row['log2_fim'], 1] 
    for row in resultados
])
y = np.array([row['meio_rel'] for row in resultados])

# Usar numpy.linalg.lstsq para regressão linear
coef, _, _, _ = np.linalg.lstsq(X, y, rcond=None)

print(f"\nCoeficientes: a={coef[0]:.4f}, b={coef[1]:.4f}, c={coef[2]:.4f}")

# Testar previsão para os dados originais
y_pred = X @ coef

for i, (real, pred) in enumerate(zip(y, y_pred)):
    print(f"Intervalo {dados[i][0]}-{dados[i][2]}: real={real:.4f}, previsto={pred:.4f}, erro={pred-real:+.4f}")


import numpy as np

X_poly = []
for row in resultados:
    lstart = row['log2_inicio']
    lfin = row['log2_fim']
    X_poly.append([
        lstart,
        lfin,
        lstart**2,
        lfin**2,
        lstart * lfin,
        1,
    ])

X_poly = np.array(X_poly)
y = np.array([row['meio_rel'] for row in resultados])

coef, _, _, _ = np.linalg.lstsq(X_poly, y, rcond=None)

print(f"\nCoeficientes polinomiais: {coef}")

y_pred = X_poly @ coef

for i, (real, pred) in enumerate(zip(y, y_pred)):
    print(f"Intervalo {dados[i][0]}-{dados[i][2]}: real={real:.4f}, previsto={pred:.4f}, erro={pred-real:+.4f}")

import numpy as np

def prever_meio(inicio, fim):
    """
    Estima o valor do 'meio' com base nos limites 'inicio' e 'fim',
    utilizando uma regressão polinomial de 2ª ordem sobre log2 dos limites.
    """
    # Evita divisão por zero ou logaritmo inválido
    if inicio <= 0 or fim <= 0 or fim <= inicio:
        raise ValueError("Os valores devem ser positivos e 'fim' deve ser maior que 'inicio'.")

    # Calcula log2 dos limites
    log2_inicio = np.log2(inicio)
    log2_fim = np.log2(fim)

    # Vetor de entrada com termos polinomiais
    x = np.array([
        log2_inicio,
        log2_fim,
        log2_inicio ** 2,
        log2_fim ** 2,
        log2_inicio * log2_fim,
        1
    ])

    # Coeficientes do modelo polinomial (obtidos via lstsq)
    coef = np.array([
        2225.1803876,
       -5257.94133239,
       -4978.05209981,
       -2024.46846494,
        7005.97964757,
        7708.0908043
    ])

    # Estimar meio_rel
    meio_rel = x @ coef

    # Convertendo para posição absoluta
    meio = inicio + meio_rel * (fim - inicio)
    return meio
# Exemplo: prever meio para o intervalo [2048, 4095]
inicio = 2048
fim = 4095
meio_estimado = prever_meio(inicio, fim)
print(f"Meio estimado para o intervalo {inicio}-{fim}: {meio_estimado:.2f}")
