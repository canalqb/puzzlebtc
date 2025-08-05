n = 19

inicio = 2 ** n
fim = (2 ** (n + 1)) - 1
alvo = 863317

for x in range(inicio, fim + 1):
    print(f"Testando x = {x}")
    if x == alvo:
        print(f"Encontrado o valor alvo {alvo}!",end="\r")
        break
