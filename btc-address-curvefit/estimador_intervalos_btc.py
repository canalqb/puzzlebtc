import numpy as np
from scipy.optimize import curve_fit

# Dados fornecidos
intervalos = [
    (1073741824, 2102388551, 2147483647),
    (2147483648, 3093472814, 4294967295),
    (4294967296, 7137437912, 8589934591),
    (8589934592, 14133072157, 17179869183),
    (17179869184, None, 34359738367)
]

# Preparar dados
x_vals = []
y_vals = []
x_missing = None

for x1, y, x2 in intervalos:
    xm = (x1 + x2) / 2
    if y is not None:
        x_vals.append(xm)
        y_vals.append(y)
    else:
        x_missing = xm

x_vals = np.array(x_vals, dtype=np.float64)
y_vals = np.array(y_vals, dtype=np.float64)

# Definir a função para ajuste
def func(x, A, B, C, D):
    return A * np.log(B * x + C) + D

# Valores iniciais para A, B, C, D
initial_guess = [1e10, 1e-10, 1, 1e10]

# Ajustar curva usando curve_fit
params, covariance = curve_fit(func, x_vals, y_vals, p0=initial_guess, maxfev=10000)

A, B, C, D = params

print(f"Parâmetros ajustados: A={A}, B={B}, C={C}, D={D}")

# Estimar valor para x_missing
y_estimado = func(x_missing, *params)

print(f"Valor estimado para 'None': {int(y_estimado)}")
