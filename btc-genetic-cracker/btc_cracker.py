Dêe um nome de pasta, e para o script.
Crie um readme.md para github  já renderizado, não quero ver a estrutura markdown, explicando para que serve o script 
Deixe bem explicado e bem formatado, com icones e textos com formatações, de negrito, italico, listas de passo a passo, entre outros

## 📬 Contato

Feito por [CanalQb no GitHub](https://github.com/canalqb)
Visite o blog: [canalqb.blogspot.com](https://canalqb.blogspot.com/)
💸 Apoie o projeto via Bitcoin: `13Ve1k5ivByaCQ5yer6GoV84wAtf3kNava`




# --- Constantes de Configuração ---
DATA_ADDRESS = [
"122AJhKLEfkFBaGAd84pLp1kfE7xK3GdT8","128z5d7nN7PkCuX5qoA4Ys6pmxUYnEy86k","12CiUhYVTTH33w3SPUBqcpMoqnApAV4WCF","12jbtzBb54r97TCwW3G1gCFoumpckRAPdY","12JzYkkN76xkwvcPT6AWKZtGX6w2LAgsJg",
"12VVRNPi4SJqUTsp6FmqDqY5sGosDtysn4","13A3JrvXmvg5w9XGvyyR4JEJqiLz8ZySY3","13N66gCzWWHEZBxhVxG18P8wyjEWF9Yoi1","13Q84TNNvgcL3HJiqQPvyBb9m4hxjS3jkV","13zb1hQbWVsc2S7ZTZnP2G4undNNpdh5so","13zYrYhhJxp6Ui1VV7pqa5WDhNWM45ARAC",
"14iXhn8bGajVWegZHJ18vJLHhntcpL4dex","14JHoRAdmJg3XR4RjMDh6Wed6ft6hzbQe9","14MdEb4eFcT3MVG5sPFG4jGLuHJSnt1Dk2","14oFNXucftsHiUMY8uctg6N487riuyXs4h",
"14u4nA5sugaswb6SZgn5av2vuChdMnD9E5","15ANYzzCp5BFHcCnVFzXqyibpzgPLWaD8b","15c9mPGLku1HuW9LRtBf4jcHVpBUt8txKz","15EJFC5ZTs9nhsdvSUeBXjLAuYq3SWaxTc",
"15JhYXn6Mx3oF4Y7PcTAv2wVVAuCFFQNiP","15K1YKJMiJ4fpesTVUcByoz334rHmknxmT","15MnK2jXPqTMURX4xC3h4mAZxyCcaWWEDD","15nf31J46iLuK1ZkTnqHo7WgN5cARFK3RA",
"15qF6X51huDjqTmF9BJgxXdt1xcj46Jmhb","15qsCm78whspNQFydGJQk5rexzxTQopnHZ","15z9c9sVpu6fwNiK7dMAFgMYSK4GqsGZim","16AbnZjZZipwHMkYKBSfswGWKDmXHjEpSf",
"16jY7qLJnxb7CHZyqBP8qca9d51gAjyXQN","16RGFo6hjq9ym6Pj7N5H7L1NR1rVPJyw2v","16zRPnT8znwq42q7XeMkZUhb1bKqgRogyy","174SNxfqpdMGYy5YQcfLbSTK3MRNZEePoy",
"17aPYR1m6pVAacXg1PTDDU7XafvK1dxvhi","17Q7tuG2JwFFU9rXVj3uZqRtioH3mx2Jad","17s2b9ksz5y7abUm92cHwG8jEPCzK3dLnT","17uDfp5r4n441xkgLFmhNoSW1KWp6xVLD","18192XpzzdDi2K11QVHR7td2HcPS6Qs5vg","1824ZJQ7nKJ9QFTRBqn7z7dHV5EGpzUpH3",
"187swFMjz1G54ycVU56B7jZFHFTNVQFDiu","18A7NA9FTsnJxWgkoFfPAFbQzuQxpRtCos","18aNhurEAJsw6BAgtANpexk5ob1aGTwSeL","18KsfuHuzQaBTNLASyj15hy4LuqPUo1FNB",
"18ywPwj39nGjqBrQJSzZVq2izR12MDpDr8","18ZMbwUFLMHoZBbfpCjUJQTCMCbktshgpe","19EEC52krRUK1RkUAEZmQdjTyHT7Gp1TYT","19eVSDuizydXxhohGh8Ki9WY9KsHdSwoQC",
"19GpszRNUej5yYqxXoLnbZWKew3KdVLkXg","19QciEHbGVNY4hrhfKXmcBBCrJSBZ6TaVt","19vkiEajfhuZ8bs8Zu2jgmC6oqZbWqhxhG","19YZECXj3SxEZMoUeJ1yiPsw8xANe7M7QR",
"19z6waranEf8CcP8FqNgdwUe1QRxvUNKBG","19ZewH8Kk1PDbSNdJ97FP4EiCjTRaZMZQA","1Ab4vzG6wEQBDNQM1B2bvUz4fqXXdFk2WT","1AcAmB6jmtU6AiEcXkmiNE9TNVPsj9DULf",
"1AE8NzzgKE7Yhz7BWtAcAAxiFMbPo82NB5","1AoeP37TmHdFh8uN72fu9AqgtLrUwcv2wJ","1ARk8HWJMn8js8tQmGUJeQHjSE7KRkn2t8","1AVJKwzs9AskraJLGHAZPiaZcrpDr1U6AB",
"1AWCLZAjKbV1P7AHvaPNCKiB7ZWVDMxFiz","1BCf6rHUW6m3iH2ptsvnjgLruAiPQQepLe","1BDyrQ6WoF8VN3g9SAS1iKZcPzFfnDVieY","1Be2UF9NLfyLFbtm3TCbmuocc9N1Kduci1",
"1BgGZ9tcN4rm9KBzDn7KprQz87SZ26SAMH","1BkkGsX9ZM6iwL3zbqs7HWBV7SvosR6m8N","1Bxk4CQdqL9p22JEtDfdXMsng1XacifUtE","1BY8GQbnueYofwSuFAT3USAhGjPrkxDdW9",
"1CaBVPrwUxbQYYswu32w7Mj4HR4maNoJSX","1CD91Vm97mLQvXhrnoMChhJx4TP9MaQkJo","1CdufMQL892A69KXgv6UNBD17ywWqYpKut","1CfZWK1QTQE3eS9qn61dQjV89KDjZzfNcv",
"1CKCVdbDJasYmhswB6HKZHEAnNaDpK7W4n","1CkR2uS7LmFwc3T2jV8C1BhWb5mQaoxedF","1CMjscKB3QW7SDyQ4c3C3DEUHiHRhiZVib","1CMq3SvFcVEcpLMuuH8PUcNiqsK1oicG2D",
"1CQFwcjw1dwhtkVWBttNLDtqL7ivBonGPV","1CUNEBjYrCn2y1SdiUMohaKUi4wpP326Lb","1CXvTzR6qv8wJ7eprzUKeWxyGcHwDYP1i2","1DBaumZxUkM4qMQRt2LVWyFJq5kDtSZQot",
"1DFYhaB2J9q1LLZJWKTnscPWos9VBqDHzv","1DJh2eHFYQfACPmrvpyWc8MSTYKh7w9eRF","1Dn8NF8qDyyfHMktmuoQLGyjWmZXgvosXf","1E32GPWgDyeyQac4aJxm9HVoLrrEYPnM4N",
"1E6NuFjCi27W5zoXg8TRdcSRq84zJeBW3k","1EeAxcprB2PpCnr34VfZdFrkUWuxyiNEFv","1EhqbyUMvvs7BfL8goY6qcPbD6YKfPqb7e","1EQJvpsmhazYCcKX5Au6AZmZKRnzarMVZu",
"1ErZWg5cFCe4Vw5BzgfzB74VNLaXEiEkhk","1EzVHtmbN4fs4MiNk3ppEnKKhsmXYJ4s74","1F3JRMWudBaj48EhwcHDdpeuy2jwACNxjP","1Fo65aKq8s8iquMt6weF1rku1moWVEd5Ua",
"1FRoHA9xewq7DjrZ1psWJVeTer8gHRqEvR","1FTpAbQa4h8trvhQXjXnmNhqdiGBd1oraE","1FWGcVDK3JGzCC3WtkYetULPszMaK2Jksv","1FwZXt6EpRT7Fkndzv6K4b4DFoT4trbMrV",
"1Fz63c775VV9fNyj25d9Xfw3YHE6sKCxbt","1G6EFyBRU86sThN3SSt3GrHu1sA7w7nzi4","1GDSuiThEV64c166LUFC9uDcVdGjqkxKyh","1GnNTmTVLZiqQfLbAdp9DVdicEnB5GoERE",
"1GuBBhf61rnvRe4K8zu8vdQB3kHzwFqSy7","1GvgAXVCbA8FBjXfWiAms4ytFeJcKsoyhL","1HAX2n9Uruu9YDt4cqRgYcvtGvZj1rbUyt","1HB1iKUqeffnVsvQsbpC6dNi1XKbyNuqao",
"1HBtApAFA9B2YZw3G2YKSMCtb3dVnjuNe2","1HduPEXZRdG26SUT5Yk83mLkPyjnZuJ7Bm","1HsMJxNiV7TLxmoF6uJNkydxPFDog4NQum","1Hz3uv3nNZzBVMXLGadCucgjiCs5W9vaGz",
"1J36UjUByGroXcCvmj13U6uwaVv9caEeAt","1JTK7s9YVYywfm5XUH7RNhHJH1LshCaRFR","1JVnST957hGztonaWK6FougdtjxzHzRMMg","1JWnE6p6UN7ZJBN7TtcbNDoRcjFtuDWoNL",
"1K3x5L6G57Y494fDqBfrojD28UJv4s5JcK","1K6xGMUbs6ZTXBnhw1pippqwK6wjBWtNpL","1KCgMv8fo2TPBpddVi9jqmMmcne9uSNJ5F","1Kh22PvXERd2xpTQk3ur6pPEqFeckCJfAr",
"1Kn5h2qpgw9mWE5jKpk8PP4qvvJ1QVy8su","1KNRfGWw7Q9Rmwsc6NT5zsdvEb9M2Wkj5Z","1KrU4dHE5WrW8rhWDsTRjR21r8t3dsrS3R","1KYUv7nSvXx4642TKeuC2SNdTk326uUpFy",
"1L12FHH2FHjvTviyanuiFVfmzCy46RRATU","1L2GM8eE7mJWLdo3HZS6su1832NX2txaac","1L5sU9qvJeuwQUdt4y1eiLmquFxKjtHr3E","1LeBZP5QCwwgXRtmVUvTVrraqPUokyLHqe",
"1LhE6sCTuGae42Axu1L1ZB7L96yi9irEBE","1LHtnpd8nU5VHEMkG2TMYYNUjjLc992bps","1LuUHyrQr8PKSvbcY1v1PiuGuqFjWpDumN","1LzhS3k3e9Ub8i2W1V8xQFdB8n2MYCHPCa",
"1M7ipcdYHey2Y5RZM34MBbpugghmjaV89P","1M92tSqNmQLYw33fuBvjmeadirh1ysMBxK","1McVt1vMtCC7yn5b9wgX1833yCcLXzueeC","1Me3ASYt5JCTAK2XaC32RMeH34PdprrfDx",
"1Me6EfpwZK5kQziBwBfvLiHjaPGxCKLoJi","1MEzite4ReNuWaL5Ds17ePKt2dCxWEofwk","1MnJ6hdhvK37VLmqcdEwqC3iFxyWH2PHUV","1MUJSJYtGPVGkBCTqGspnxyHahpt5Te8jy",
"1MVDYgVaSN6iKKEsbzRUAYFrYJadLYZvvZ","1MZ2L1gFrCtkkn6DnTT2e4PFUTHw9gNwaj","1NBC8uXJy1GiJ6drkiZa1WuKn51ps7EPTv","1NeGn21dUDDeqFQ63xb2SpgUuXuBLA4WT4",
"1NevxKDYuDcCh1ZMMi6ftmWwGrZKC6j7Ux","1NgVmsCCJaKLzGyKLFJfVequnFW9ZvnMLN","1NLbHuJebVwUZ1XqDjsAyfTRUPwDQbemfv","1NpnQyZ7x24ud82b7WiRNvPm6N8bqGQnaS",
"1NpYjtLira16LfGbGwZJ5JbDPh3ai9bjf4","1NtiLNGegHWE3Mp9g2JPkgx6wUg4TW7bbk","1NWmZRpHH4XSPwsW6dsS3nrNWfL1yrJj4w","1Pd8VvT49sHKsmqrQiP61RsVwmXCZ6ay7Z",
"1PgQVLmst3Z314JrQn5TNiys8Hc38TcXJu","1Pie8JkxBT6MGPz9Nvi3fsPkr2D8q3GBc1","1PiFuqGpG8yGM5v6rNHWS3TjsG6awgEGA1","1PitScNLyp2HCygzadCh7FveTnfmpPbfp8",
"1PJZPzvGX19a7twf5HyD2VvNiPdHLzm9F6","1PWABE7oUahG2AFFQhhvViQovnCr4rEv7Q","1PWCx5fovoEaoBowAvF5k91m2Xat9bMgwb","1PWo3JeB9jrGwfHDNpdGK54CRas7fsVzXU",
"1PXAyUB8ZoH3WD8n5zoAthYjN15yN5CVq5","1PxH3K1Shdjb7gSEoTX7UPDZ6SH4qGPrvq","1PXv28YxmYMaB8zxrKeZBW8dt2HK7RkRPX","1QCbW9HWnwQWiQqVo5exhAnmfqKRrCRsvW",
"1QKBaU6WAeycb3DbKbLBkX7vJiaS8r42Xo","1rSnXMr63jdCuegJFuidJqWxUPV7AtUf7","1UDHPdovvR985NrWSkdWQDEQ1xuRiTALq",

]
  
import re
import random
import time
import logging
from typing import List, Tuple, Union1
from deap import base, creator, tools
from bit import Key
from multiprocessing import Pool, freeze_support

# --- Configuração de logging ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
 

def salvar_wif_e_btc(texto, arquivo='carteiras.txt'):
    regex_wif = r'\b[5KL][1-9A-HJ-NP-Za-km-z]{50,51}\b'
    regex_btc = r'\b(?:1|3|bc1)[a-zA-HJ-NP-Z0-9]{25,39}\b'

    wifs = re.findall(regex_wif, texto)
    btc_addresses = re.findall(regex_btc, texto)

    with open(arquivo, 'a') as f:
        for wif in wifs:
            for btc in btc_addresses:
                linha = f"WIF: {wif} | BTC: {btc}\n"
                f.write(linha)
                print(linha.strip())

def get_config_by_length_improved(length):
    configs = [
        (8,   dict(pop_size=100, max_gen=50, p_mut=0.10, indpb=0.05, p_cx=0.9, tourn=3)),
        (16,  dict(pop_size=200, max_gen=150, p_mut=0.15, indpb=0.07, p_cx=0.9, tourn=3)),
        (32,  dict(pop_size=300, max_gen=300, p_mut=0.20, indpb=0.10, p_cx=0.85, tourn=4)),
        (48,  dict(pop_size=400, max_gen=600, p_mut=0.25, indpb=0.10, p_cx=0.8, tourn=4)),
        (64,  dict(pop_size=500, max_gen=1000, p_mut=0.25, indpb=0.10, p_cx=0.8, tourn=4)),
        (80,  dict(pop_size=600, max_gen=1500, p_mut=0.30, indpb=0.12, p_cx=0.75, tourn=5)),
        (96,  dict(pop_size=700, max_gen=2000, p_mut=0.30, indpb=0.15, p_cx=0.75, tourn=5)),
        (128, dict(pop_size=800, max_gen=3000, p_mut=0.35, indpb=0.18, p_cx=0.7, tourn=5)),
        (160, dict(pop_size=900, max_gen=4000, p_mut=0.40, indpb=0.20, p_cx=0.7, tourn=5)),
        (192, dict(pop_size=1000, max_gen=5000, p_mut=0.45, indpb=0.22, p_cx=0.7, tourn=6)),
        (224, dict(pop_size=1100, max_gen=6000, p_mut=0.50, indpb=0.25, p_cx=0.65, tourn=6)),
        (256, dict(pop_size=1200, max_gen=7000, p_mut=0.55, indpb=0.30, p_cx=0.6, tourn=6)),
    ]
    for max_len, config in configs:
        if length <= max_len:
            return config
    return configs[-1][1]

def _get_key_from_individual(individual: List[int]) -> Tuple[Union[Key,None], str]:
    binary_secret = ''.join(map(str, individual))
    try:
        number = int(binary_secret, 2)
        if number <= 0:
            return None, binary_secret
        key = Key.from_int(number)
        return key, binary_secret
    except Exception as e:
        logging.debug(f"Erro ao criar Key: {e}")
        return None, binary_secret

def evaluate_individual(individual: List[int]) -> Tuple[int]:
    key, _ = _get_key_from_individual(individual)
    if key and key.address in DATA_ADDRESS:
        return (1,)
    return (0,)

def get_individual_details(individual: List[int]) -> Tuple[int, str, str, str]:
    key, binary_secret = _get_key_from_individual(individual)
    if not key:
        return 0, "", binary_secret, ""
    return 1, key.address, binary_secret, key.to_wif()

def apply_crossover_and_mutation(offspring, toolbox, p_crossover, p_mutation):
    for child1, child2 in zip(offspring[::2], offspring[1::2]):
        if random.random() < p_crossover:
            toolbox.mate(child1, child2)
            del child1.fitness.values
            del child2.fitness.values
    for mutant in offspring:
        if random.random() < p_mutation:
            toolbox.mutate(mutant)
            del mutant.fitness.values

def run_genetic_algorithm(target_length):
    config = get_config_by_length_improved(target_length)

    POP_SIZE = config['pop_size']
    MAX_GEN = config['max_gen']
    P_MUT = config['p_mut']
    IND_PB = config['indpb']
    P_CX = config['p_cx']
    TOURN = config['tourn']
    random.seed(8)
    # Configuração do Algoritmo Genético
    POPULATION_SIZE = 400
    P_CROSSOVER = 0.1
    P_MUTATION = 0.8
    MAX_GENERATIONS = 400
    TOUR_SIZE = 6
    INDPB = 0.1
    RANDOM_SEED = 9

    if not hasattr(creator, "FitnessMax"):
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    if not hasattr(creator, "Individual"):
        creator.create("Individual", list, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()
    toolbox.register("zeroOrOne", random.randint, 0, 1)
    toolbox.register("individualCreator", tools.initRepeat, creator.Individual, toolbox.zeroOrOne, target_length)
    toolbox.register("populationCreator", tools.initRepeat, list, toolbox.individualCreator)
    toolbox.register("select", tools.selTournament, tournsize=TOURN)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutFlipBit, indpb=IND_PB)
    toolbox.register("evaluate", evaluate_individual)

    p_crossover_current = P_CX
    found = False

    while not found:
        logging.info(f"Iniciando AG com {target_length} bits | Crossover: {p_crossover_current:.4f}")

        population = toolbox.populationCreator(n=POP_SIZE)

        with Pool() as pool:
            toolbox.register("map", pool.map)

            fitnesses = toolbox.map(toolbox.evaluate, population)
            for ind, fit in zip(population, fitnesses):
                ind.fitness.values = fit

            best = max(population, key=lambda ind: ind.fitness.values[0])
            generation = 0
            start_time = time.time()

            while best.fitness.values[0] < 1 and generation < MAX_GEN:
                generation += 1
                offspring = list(map(toolbox.clone, toolbox.select(population, len(population))))
                apply_crossover_and_mutation(offspring, toolbox, p_crossover_current, P_MUT)

                invalid = [ind for ind in offspring if not ind.fitness.valid]
                fitnesses = toolbox.map(toolbox.evaluate, invalid)
                for ind, fit in zip(invalid, fitnesses):
                    ind.fitness.values = fit

                population[:] = offspring
                best = max(population, key=lambda ind: ind.fitness.values[0])

                if generation % 10 == 0 or best.fitness.values[0] == 1:
                    elapsed = time.time() - start_time
                    if best.fitness.values[0] == 1:
                        score, addr, secret, wif = get_individual_details(best)
                        logging.info(f"[✔] Geração {generation}: WIF={wif} Endereço={addr} Tempo={elapsed:.2f}s")
                        salvar_wif_e_btc(f"WIF: {wif} {addr}")
                        found = True
                    else:
                        print(f"[ ] Geração {generation}: Nenhum endereço válido. Tempo: {elapsed:.2f}s", end='\r')

        if not found:
            p_crossover_current = min(p_crossover_current + 0.001, 1.0)
            logging.info(f"Nenhum endereço encontrado. Novo P_CROSSOVER: {p_crossover_current:.4f}")

def solicitar_target_sequence_length() -> int:
    while True:
        try:
            valor = int(input("Informe o valor de TARGET_SEQUENCE_LENGTH (1 a 256): "))
            if 1 <= valor <= 256:
                print(f"TARGET_SEQUENCE_LENGTH definido como {valor}")
                return valor
            else:
                print("Por favor, insira um número entre 1 e 256.")
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")

if __name__ == "__main__":
    freeze_support()  # Necessário para Windows com multiprocessing
    TARGET_SEQUENCE_LENGTH = solicitar_target_sequence_length()
    run_genetic_algorithm(TARGET_SEQUENCE_LENGTH)
