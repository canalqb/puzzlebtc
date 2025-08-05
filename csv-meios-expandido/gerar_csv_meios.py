import csv

# Lista de valores
meio_values = ['1',
'3',
'7',
'8',
'21',
'49',
'76',
'224',
'467',
'514',
'1155',
'2683',
'5216',
'10544',
'26867',
'51510',
'95823',
'198669',
'357535',
'863317',
'1811764',
'3007503',
'5598802',
'14428676',
'33185509',
'54538862',
'111949941',
'227634408',
'400708894',
'1033162084',
'2102388551',
'3093472814',
'7137437912',
'14133072157',
'20112871792',
'42387769980',
'100251560595',
'146971536592',
'323724968937',
'1003651412950',
'1458252205147',
'2895374552463',
'7409811047825',
'15404761757071',
'19996463086597',
'51408670348612',
'119666659114170',
'191206974700443',
'409118905032525',
'611140496167764',
'2058769515153876',
'4216495639600700',
'6763683971478124',
'9974455244496707',
'30045390491869460',
'44218742292676575',
'138245758910846492',
'199976667976342049',
'525070384258266191',
'1135041350219496382',
'1425787542618654982',
'3908372542507822062',
'8993229949524469768',
'17799667357578236628',
'30568377312064202855',
'46346217550346335726',
'132656943602386256302',
'219898266213316039825',
'297274491920375905804',
'970436974005023690481',
None,
None,
None,
None,
'22538323240989823823367',
None,
None,
None,
None,
'1105520030589234487939456',
None,
None,
None,
None,
'21090315766411506144426920',
None,
None,
None,
None,
'868012190417726402719548863',
None,
None,
None,
None,
'25525831956644113617013748212',
None,
None,
None,
None,
'868221233689326498340379183142',
None,
None,
None,
None,
'29083230144918045706788529192435',
None,
None,
None,
None,
'1090246098153987172547740458951748',
None,
None,
None,
None,
'31464123230573852164273674364426950',
None,
None,
None,
None,
'919343500840980333540511050618764323',
None,
None,
None,
None,
'37650549717742544505774009877315221420',
None,
None,
None,
None,
'1103873984953507439627945351144005829577',
] 


 
rows = []

for val in meio_values:
    if val in (None, '', 'None'):
        rows.append(["''"] * 10)
        continue

    n = int(val)
    id_val = n.bit_length() - 1
    base = 2 ** id_val
    upper = (2 ** (id_val + 1)) - 1
    bit_count = bin(n).count('1')

    # Colunas anteriores
    col_a = n * bit_count
    col_b = bit_count / n if n != 0 else 0
    col_c = col_a / col_b if col_b != 0 else 0

    # Novas colunas
    col_d = 2 * n - 1
    col_e = bin(col_d).count('1')

    rows.append([
        f"'{id_val}",
        f"'{base}",
        f"'{n}",
        f"'{upper}",
        f"'{bit_count}",
        f"'{col_a}",
        f"'{col_b:.9f}".replace('.', ','),
        f"'{int(col_c)}",
        f"'{col_d}",
        f"'{col_e}"
    ])

# Cabeçalhos
headers = [
    'ID',
    '2^ID',
    'decimal',
    '2^(ID+1)-1',
    'Total de Bits',
    'A = decimal * bits',
    'B = bits / decimal',
    'A / B',
    'D = 2 * decimal - 1',
    'E = bits(D)'
]

# Salvar como CSV
with open('meios_expandido.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, delimiter=';')
    writer.writerow([f"'{h}" for h in headers])
    writer.writerows(rows)

print("✅ CSV 'meios_expandido.csv' gerado com sucesso com 10 colunas.")
