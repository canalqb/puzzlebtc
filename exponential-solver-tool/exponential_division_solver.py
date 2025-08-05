def encontrar_exp_por_x(N, alvo_x):
    from decimal import Decimal, getcontext
    getcontext().prec = 100

    alvo_x = int(alvo_x)
    base = 2 ** (N + 1)
    
    for i in range(256, -1, -1):
        EXP = 2 ** i
        produto = alvo_x * EXP

        if produto % base == 0:
            L = produto // base
            print(f"Encontrado: EXP={EXP} (2^{i}), L={L}, X={alvo_x}")
            return

    print("Nenhum EXP encontrado que satisfaça a condição.")

# Exemplo
encontrar_exp_por_x(12, 5216)


print('------------')
from decimal import Decimal, getcontext

def encontrar_X_por_exp_e_l(N):
    getcontext().prec = 50
    base = 2 ** N
    limite_inferior = Decimal(base)
    limite_superior = Decimal(2 * base - 1)

    potencias_exp = [2**i for i in range(257)]  # EXP = 2^0 até 2^256

    for EXP in potencias_exp:
        # Vamos variar L de 0 até 2^{N+1} (ou outro limite razoável)
        limite_L = 2 * base  # ou outro valor, conforme necessário
        for L in range(limite_L + 1):
            X = (Decimal(base) * Decimal(L) * 2) / Decimal(EXP)
            if limite_inferior <= X <= limite_superior:
                print(f"N={N}, EXP=2^{EXP.bit_length()-1}={EXP}, L={L}, X={X}")

# Exemplo para N=8
encontrar_X_por_exp_e_l(8)
