import sqlite3
import gc
import math
from mpmath import mp, findroot, zeta
from bit import Key

def set_dynamic_precision(valor):
    digits = int(math.floor(valor * math.log10(2))) + 1
    mp.dps = 15 + digits
    print(f"🔧 Ajustando mp.dps para {mp.dps} (valor={valor})")

def sample_and_find_zeros(t_start, t_end, step=10000, window=0.2):
    zeros = []
    t = t_start
    while t < t_end - window:
        f1 = zeta(0.5 + 1j * t).real
        f2 = zeta(0.5 + 1j * (t + window)).real 
        if f1 * f2 < 0 and abs(f1) < 0.05 and abs(f2) < 0.05:  # restrição mais rigorosa
            try:
                zero_t = findroot(
                    lambda x: zeta(0.5 + 1j * x).real,
                    (t, t + window),
                    solver='bisect',   # alternativo ao 'muller'
                    tol=1e-18,         # tolerância relaxada
                    maxsteps=100
                )
                zero = 0.5 + 1j * zero_t
                if not zeros or abs(zero.imag - zeros[-1].imag) > 1e-6:
                    zeros.append(zero)
            except Exception as e: 
                original = int(t)
                anterior = original - 1
                posterior = original + 1

                try:
                    key_ant = Key.from_int(anterior).to_wif()
                    key_orig = Key.from_int(original).to_wif()
                    key_pos = Key.from_int(posterior).to_wif()

                    print(f"🔍 Erro durante o processamento da janela [{t}, {t + window}].")
                    print(f"Chaves ao redor do erro:")
                    print(f"p2wpkh:{key_ant}")
                    print(f"p2wpkh:{key_orig}")
                    print(f"p2wpkh:{key_pos}")
                    print(f"p2pkh:{key_ant}")
                    print(f"p2pkh:{key_orig}")
                    print(f"p2pkh:{key_pos}")
                    print(f"p2wpkh-p2sh:{key_ant}")
                    print(f"p2wpkh-p2sh:{key_orig}")
                    print(f"p2wpkh-p2sh:{key_pos}")

                except Exception as e:
                    print(f"Erro ao gerar chaves para {original}: {e}")

        t += step
    return zeros

def create_db_connection(db_file="zerosdeRiemann.db"):
    return sqlite3.connect(db_file)

def create_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS zeros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            valor INTEGER NOT NULL,
            wif TEXT NOT NULL
        )
    ''')
    conn.commit()

def insert_zero(conn, valor, wif):
    cursor = conn.cursor()
    cursor.execute('INSERT INTO zeros (valor, wif) VALUES (?, ?)', (valor, wif))
    conn.commit()

def process_with_sampling(conn, valor, t_start, t_end, step=10000):
    print(f"🔍 Amostrando intervalo para valor={valor} [{t_start}, {t_end}] com step={step}...")
    zeros = sample_and_find_zeros(t_start, t_end, step=step)
    for zero in zeros:
        key = Key.from_int(int(zero.imag))
        wif = key.to_wif()
        print(f"p2wpkh:{wif}")
        print(f"p2pkh:{wif}")
        print(f"p2wpkh-p2sh:{wif}")
        insert_zero(conn, valor, wif)
    del zeros
    gc.collect()

def main():
    conn = create_db_connection()
    create_table(conn)

    for valor in range(70, 71):
        set_dynamic_precision(valor)
        t_start = 2 ** valor
        t_end = 2 ** (valor + 1) - 1
        process_with_sampling(conn, valor, t_start, t_end, step=10000)  # Pode ajustar step aqui

    conn.close()

if __name__ == "__main__":
    main()
