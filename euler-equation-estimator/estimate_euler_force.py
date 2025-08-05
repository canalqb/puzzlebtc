import math

numeros = [1, 3, 7, 8, 21, 50, 76, 224, 467, 514, 1155, 2683, 5216, 10544, 26867, 51510]

def euler_equation_simples(rho, u, p):
    # Simplificação ilustrativa:
    # Força estimada = rho * u^2 + p
    return rho * (u ** 2) + p

print("Estimativa simples das Equações de Euler usando combinações dos seus valores:\n")

for n in numeros:
    N = math.floor(math.log2(n))
    val1 = n
    val2 = 2 ** N
    val3 = 2 ** (N + 1) - 1

    combinacoes = [
        ("(rho=n, u=2^N, p=2^(N+1)-1)", val1, val2, val3),
        ("(rho=n, u=2^(N+1)-1, p=2^N)", val1, val3, val2),
        ("(rho=2^N, u=n, p=2^(N+1)-1)", val2, val1, val3),
        ("(rho=2^N, u=2^(N+1)-1, p=n)", val2, val3, val1),
        ("(rho=2^(N+1)-1, u=n, p=2^N)", val3, val1, val2),
        ("(rho=2^(N+1)-1, u=2^N, p=n)", val3, val2, val1)
    ]

    print(f"Para n = {n}, valores base: [{val1}, {val2}, {val3}]")
    for nome, rho, u, p in combinacoes:
        resultado = euler_equation_simples(rho, u, p)
        print(f"  Combinação {nome}: rho = {rho}, u = {u}, p = {p} -> Força estimada = {resultado:.4f}")
    print()
