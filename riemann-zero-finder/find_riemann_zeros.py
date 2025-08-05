import sqlite3
import gc
import math
from mpmath import mp, findroot, zeta
from bit import Key

def set_dynamic_precision(valor):
    # Define mp.dps com base em 2^valor
    digits = int(math.floor(valor * math.log10(2))) + 1
    mp.dps = 15 + digits
    print(f"🔧 Ajustando mp.dps para {mp.dps} (valor={valor})")

def find_zeros_in_interval(t_start, t_end, step=0.5):
    zeros = []
    t = t_start
    while t < t_end:
        f1 = zeta(0.5 + 1j * t).real
        f2 = zeta(0.5 + 1j * (t + step)).real
        print(f"{f1} - {f2}")
        if f1 * f2 < 0 and abs(f1) < 0.1 and abs(f2) < 0.1:
            try:
                zero_t = findroot(
                    lambda x: zeta(0.5 + 1j * x).real,
                    (t, t + step),
                    solver='muller',
                    tol=1e-12,
                    maxsteps=50
                )
                zero = 0.5 + 1j * zero_t
                if not zeros or abs(zero.imag - zeros[-1].imag) > 1e-6:
                    zeros.append(zero)
            except Exception as e:
                print(f"❌ Erro no intervalo [{t}, {t + step}]: {e}")
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

def process_in_batches(conn, valor, t_start, t_end, step=0.5, batch_size=100000):
    current = t_start
    while current < t_end:
        batch_end = min(current + batch_size, t_end)
        print(f"🔄 Processando valor={valor} lote {current} até {batch_end}...")
        zeros = find_zeros_in_interval(current, batch_end, step)
        for zero in zeros:
            key = Key.from_int(int(zero.imag))
            wif = key.to_wif()
            print(f"➕ {valor} - {wif}")
            insert_zero(conn, valor, wif)
        del zeros
        gc.collect()
        current = batch_end

def main():
    conn = create_db_connection()
    create_table(conn)

    for valor in range(40, 50):  # ou qualquer outro intervalo
        set_dynamic_precision(valor)  # ⬅️ Define mp.dps dinamicamente
        t_start = 2 ** valor
        t_end = 2 ** (valor + 1) - 1
        process_in_batches(conn, valor, t_start, t_end)

    conn.close()

if __name__ == "__main__":
    main()
