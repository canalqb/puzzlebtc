def find_mid_value(start, end):
    n = end + 1
    # Tentar t de 0 até 15 (você pode aumentar esse limite)
    for t in range(16):
        val = pow(2, 2**t, n)
        if start < val < end:  # meio deve estar dentro do intervalo
            return val, t
    return None, None

def parse_and_compute(lines):
    for line in lines:
        parts = line.strip().split(',')
        if len(parts) != 3:
            continue
        
        start_str, mid_str, end_str = parts
        start = int(start_str.strip())
        end = int(end_str.strip())
        
        # Se meio já está dado, apenas printar
        if mid_str.strip() != '?':
            mid = int(mid_str.strip())
            print(f"Intervalo: {start}, {mid}, {end}")
            print("Meio informado, sem cálculo.")
            print("---")
        else:
            mid_calc, t = find_mid_value(start, end)
            if mid_calc is not None:
                print(f"Intervalo: {start}, ?, {end}")
                print(f"Meio calculado: {mid_calc} (para t={t})")
                print("---")
            else:
                print(f"Intervalo: {start}, ?, {end}")
                print("Não foi possível encontrar um meio com a fórmula para t <= 15")
                print("---")

# Dados de entrada, com o '?' na linha que você quer calcular
linhas = [
    "1, 1, 1",
    "2, 3, 3",
    "4, 7, 7",
    "8, 8, 15",
    "16, 21, 31",
    "32, 49, 63",
    "64, 76, 127",
    "128, ?, 255",
    "256, 467, 511",
    "512, 514, 1023",
    "1024, 1155, 2047",
    "2048, 2683, 4095",
    "4096, 5216, 8191",
    "8192, 10544, 16383",
    "16384, 26867, 32767",
    "32768, 51510, 65535",
    "65536, 95823, 131071",
    "131072, 198669, 262143",
    "262144, 357535, 524287",
    "524288, 863317, 1048575",
    "1048576, 1811764, 2097151",
    "2097152, 3007503, 4194303"
]

parse_and_compute(linhas)
