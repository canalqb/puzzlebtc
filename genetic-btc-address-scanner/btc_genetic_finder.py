import sqlite3
import random
import time
from deap import base, creator, tools
from bit import Key
from multiprocessing import Pool
import psutil
import os
import platform

if platform.system() == "Windows":
    p = psutil.Process(os.getpid())
    p.nice(psutil.IDLE_PRIORITY_CLASS)
    print("[*] Prioridade do processo definida como BAIXA.")

# Configurações
POPULATION_SIZE = 3000
P_CROSSOVER = 0.5
P_MUTATION = 0.9
INDPB = 0.2
MAX_GENERATIONS = 140
TOUR_SIZE = 4

DB_PATH = r"D:\Rodrigo\20052025\blockchair\banco.db"

conn = None
cursor = None

def init_db():
    global conn, cursor
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.execute('PRAGMA query_only = ON')
    cursor = conn.cursor()

def close_db():
    global conn, cursor
    if cursor:
        cursor.close()
    if conn:
        conn.close()

def address_exists(addr: str) -> bool:
    global cursor
    cursor.execute("SELECT 1 FROM enderecos WHERE address = ? LIMIT 1", (addr,))
    return cursor.fetchone() is not None

def get_random_address_by_length(length: int) -> str:
    global cursor
    cursor.execute("SELECT address FROM enderecos WHERE LENGTH(address) = ? ORDER BY RANDOM() LIMIT 1", (length,))
    result = cursor.fetchone()
    return result[0] if result else None

def fitness_function(individual):
    secret = "".join(map(str, individual))
    if not secret:
        return (0,)
    number = int(secret, 2)
    if number <= 0:
        return (0,)
    try:
        key_comp = Key(secret_exponent=number, compressed=True)
        key_uncomp = Key(secret_exponent=number, compressed=False)
        addrs = [
            key_comp.address,
            key_uncomp.address,
            key_comp.segwit_address,
            key_uncomp.segwit_address,
            key_comp.segwit_address.replace('3', 'bc1', 1),
            key_uncomp.segwit_address.replace('3', 'bc1', 1),
        ]
        for addr in addrs:
            if address_exists(addr):
                return (1,)
    except Exception:
        return (0,)
    return (0,)

def get_best_info(ind, target):
    secret = "".join(map(str, ind))
    if not secret:
        return (0, "", "", "")
    try:
        number = int(secret, 2)
        if number <= 0:
            return (0, "", "", "")
    except ValueError:
        return (0, "", "", "")
    try:
        key_comp = Key(secret_exponent=number, compressed=True)
        key_uncomp = Key(secret_exponent=number, compressed=False)
    except Exception:
        return (0, "", "", "")
    wif_comp = key_comp.to_wif()
    wif_uncomp = key_uncomp.to_wif()
    addr_p2pkh_comp = key_comp.address
    addr_p2pkh_uncomp = key_uncomp.address
    addr_p2sh_comp = key_comp.segwit_address
    addr_p2sh_uncomp = key_uncomp.segwit_address
    addr_bech32_comp = addr_p2sh_comp.replace('3', 'bc1', 1)
    addr_bech32_uncomp = addr_p2sh_uncomp.replace('3', 'bc1', 1)
    candidates = [
        (addr_p2pkh_comp, wif_comp),
        (addr_p2pkh_uncomp, wif_uncomp),
        (addr_p2sh_comp, wif_comp),
        (addr_p2sh_uncomp, wif_uncomp),
        (addr_bech32_comp, wif_comp),
        (addr_bech32_uncomp, wif_uncomp),
    ]
    best_score = 0
    best_addr = ""
    best_wif = ""
    for addr, wif in candidates:
        score = sum(a == b for a, b in zip(target, addr))
        if score > best_score:
            best_score = score
            best_addr = addr
            best_wif = wif
    return (best_score, best_addr, secret, best_wif)

def run_genetic(TARGET_LEN):
    if TARGET_LEN < 2:
        print(f"[!] TARGET_LEN={TARGET_LEN} é muito pequeno para cruzamento genético. Use pelo menos 2.")
        return

    target = get_random_address_by_length(TARGET_LEN)
    print(f"\n== Iniciado TARGET_LEN={TARGET_LEN} – Target: {target if target else '[inválido]'}")

    if not target:
        print(f"[!] Nenhum endereço válido com TARGET_LEN = {TARGET_LEN}. Pulando...")
        return

    if not hasattr(creator, "FitnessMax"):
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    if not hasattr(creator, "Individual"):
        creator.create("Individual", list, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()
    toolbox.register("attr_bool", random.randint, 0, 1)
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, TARGET_LEN)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", fitness_function)
    toolbox.register("select", tools.selTournament, tournsize=TOUR_SIZE)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutFlipBit, indpb=INDPB)

    population = toolbox.population(n=POPULATION_SIZE)

    with Pool() as pool:
        toolbox.register("map", pool.map)
        fitnesses = toolbox.map(toolbox.evaluate, population)
        for ind, fit in zip(population, fitnesses):
            ind.fitness.values = fit

        best = max(population, key=lambda ind: ind.fitness.values[0])
        max_fit = best.fitness.values[0]
        last_addr = None

        for gen in range(1, MAX_GENERATIONS + 1):
            offspring = toolbox.select(population, len(population))
            offspring = list(map(toolbox.clone, offspring))

            for c1, c2 in zip(offspring[::2], offspring[1::2]):
                if random.random() < P_CROSSOVER:
                    toolbox.mate(c1, c2)
                    del c1.fitness.values, c2.fitness.values

            for mutant in offspring:
                if random.random() < P_MUTATION:
                    toolbox.mutate(mutant)
                    del mutant.fitness.values

            invalid = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = toolbox.map(toolbox.evaluate, invalid)
            for ind, fit in zip(invalid, fitnesses):
                ind.fitness.values = fit

            population[:] = offspring
            current_max = max(ind.fitness.values[0] for ind in population)

            if current_max > max_fit:
                max_fit = current_max
                best = max(population, key=lambda ind: ind.fitness.values[0])

            score, addr, secret, wif = get_best_info(best, target)

            if addr == last_addr:
                number = int(secret, 2)
                interval_start = 2 ** (TARGET_LEN - 1)
                interval_end = 2 ** TARGET_LEN - 1

                max_attempts = 10
                attempts = 0
                new_addr = addr

                while new_addr == last_addr and attempts < max_attempts:
                    percentual_de_pulo = round(random.uniform(1, 99), 6)
                    step = max(int((interval_end - interval_start) * percentual_de_pulo / 100), 1)

                    if number + step <= interval_end:
                        new_number = number + step
                    else:
                        new_number = max(number - step, interval_start)

                    bitstr = bin(new_number)[2:].zfill(TARGET_LEN)

                    if len(bitstr) != TARGET_LEN:
                        attempts += 1
                        continue

                    try:
                        key_comp = Key(secret_exponent=new_number, compressed=True)
                        key_uncomp = Key(secret_exponent=new_number, compressed=False)

                        candidates = [
                            (key_comp.address, key_comp.to_wif()),
                            (key_uncomp.address, key_uncomp.to_wif()),
                            (key_comp.segwit_address, key_comp.to_wif()),
                            (key_uncomp.segwit_address, key_uncomp.to_wif()),
                            (key_comp.segwit_address.replace('3', 'bc1', 1), key_comp.to_wif()),
                            (key_uncomp.segwit_address.replace('3', 'bc1', 1), key_uncomp.to_wif()),
                        ]

                        found_new = False
                        for new_addr_candidate, new_wif in candidates:
                            if new_addr_candidate != last_addr:
                                new_addr = new_addr_candidate
                                wif = new_wif
                                best = creator.Individual(list(map(int, bitstr)))
                                best.fitness.values = toolbox.evaluate(best)
                                print(f"WIF: {wif} | Address: {new_addr}", end="\r")
                                last_addr = new_addr
                                found_new = True
                                break

                        if not found_new:
                            attempts += 1

                    except Exception as e:
                        attempts += 1
            else:
                print(f"WIF: {wif} | Address: {addr}")
                last_addr = addr

            if address_exists(addr):
                with open("enderecos_encontrados.txt", "a") as f:
                    f.write(f"WIF: {wif} | Address: {addr}\n")
                print(f"\n>>> Endereço {addr} encontrado em gen {gen}!\n")

        score, addr, secret, wif = get_best_info(best, target)
        print(f"-> Final: Generation={gen}, Score={score}, Addr={addr}, WIF={wif}")

if __name__ == "__main__":
    init_db()
    try:
        for TARGET_LEN in range(2, 257):
            run_genetic(TARGET_LEN)
    finally:
        close_db()
