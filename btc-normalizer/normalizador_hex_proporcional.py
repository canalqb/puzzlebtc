import pandas as pd
from decimal import Decimal, getcontext

# Configurar a precisão global
getcontext().prec = 50

# Ajuste aqui a precisão das casas decimais
precisao_decimal = Decimal('1.0000000')  # 6 casas decimais, altere para '1.000000000000' se quiser 12, etc.

# Lista fornecida (adicione a sua lista completa aqui)
hex_list = [
    '1', '3', '7', '8', '15', '31', '4c', 'e0', '1d3', '202', '483', 'a7b', '1460', '2930', '68f3', 'c936',
    '1764f', '3080d', '5749f', 'd2c55', '1ba534', '2de40f', '556e52', 'dc2a04', '1fa5ee5', '340326e',
    '6ac3875', 'd916ce8', '17e2551e', '3d94cd64', '7d4fe747', 'b862a62e', '1a96ca8d8', '34a65911d',
    '4aed21170', '9de820a7c', '1757756a93', '22382facd0', '4b5f8303e9', 'e9ae4933d6', '153869acc5b',
    '2a221c58d8f', '6bd3b27c591', 'e02b35a358f', '122fca143c05', '2ec18388d544', '6cd610b53cba',
    'ade6d7ce3b9b', '174176b015f4d', '22bd43c2e9354', '75070a1a009d4', 'efae164cb9e3c',
    '180788e47e326c', '236fb6d5ad1f43', '6abe1f9b67e114', '9d18b63ac4ffdf', '1eb25c90795d61c',
    '2c675b852189a21', '7496cbb87cab44f', 'fc07a1825367bbe', '13c96a3742f64906', '363d541eb611abee',
    '7cce5efdaccf6808', 'f7051f27b09112d4', '1a838b13505b26867', '2832ed74f2b5e35ee', '730fc235c1942c1ae',
    'bebb3940cd0fc1491', '101d83275fb2bc7e0c', '349b84b6431a6c4ef1',
    None, None, None, None, '4c5ce114686a1336e07',
    None, None, None, None, 'ea1a5c66dcc11b5ad180',
    None, None, None, None, '11720c4f018d51b8cebba8',
    None, None, None, None, '2ce00bb2136a445c71e85bf',
    None, None, None, None, '527a792b183c7f64a0e8b1f4',
    None, None, None, None, 'af55fc59c335c8ec67ed24826',
    None, None, None, None, '16f14fc2054cd87ee6396b33df3',
    None, None, None, None, '35c0d7234df7deb0f20cf7062444',
    None, None, None, None, '60f4d11574f5deee49961d9609ac6',
    None, None, None, None, 'b10f22572c497a836ea187f2e1fc23',
    None, None, None, None, '1c533b6bb7f0804e09960225e44877ac',
    None, None, None, None, '33e7665705359f04f28b88cf897c603c9'
]

# Processar os dados
rows = []

for i, h in enumerate(hex_list):
    ID = i
    inicio = Decimal(2) ** ID
    fim = (Decimal(2) ** (ID + 1)) - 1
    intervalo = fim - inicio

    if h is not None:
        decimal_val = Decimal(int(h, 16))

        try:
            # Calcular proporção com precisão controlada
            proporcao = (decimal_val - inicio) * Decimal(255) / intervalo
            proporcao_formatada = proporcao.quantize(precisao_decimal)
            proporcao_str = f"'{proporcao_formatada}'"
            proporcao_rounded = round(proporcao)
            proporcao_rounded_str = f"'{proporcao_rounded}'"

            # Reverter a proporção para encontrar o decimal novamente
            proporcao_decimal = Decimal(proporcao_str.strip("'"))
            decimal_inverso = inicio + (proporcao_decimal * intervalo / Decimal(255))
            decimal_inverso_str = f"'{decimal_inverso.quantize(precisao_decimal)}'"

            # Calcular diferença entre valor real e o reconstituído
            diferenca = decimal_inverso - decimal_val
            diferenca_str = f"'{diferenca.quantize(precisao_decimal)}'"

            decimal_str = f"'{decimal_val}'"

        except Exception:
            proporcao_str = proporcao_rounded_str = decimal_inverso_str = diferenca_str = decimal_str = "''"
    else:
        decimal_str = proporcao_str = proporcao_rounded_str = decimal_inverso_str = diferenca_str = "''"

    row = {
        "ID": f"'{ID}'",
        "2^ID": f"'{int(inicio)}'",
        "decimal": decimal_str,
        "2^(ID+1)-1": f"'{int(fim)}'",
        "proporcao": proporcao_str,
        "proporcao_arredondada": proporcao_rounded_str,
        "decimal_inverso": decimal_inverso_str,
        "diferenca": diferenca_str
    }
    rows.append(row)

# Criar e exportar DataFrame
df = pd.DataFrame(rows)
df.to_csv("hex_intervalo_normalizado.csv", sep=';', index=False)

print("✅ Arquivo 'hex_intervalo_normalizado.csv' criado com sucesso!")

  
