import base58
import hashlib
from ecdsa import SECP256k1
from bit import Key
import os # Importar para verificar a existência do arquivo

# Lista de endereços alvo
data_address = [
    "122AJhKLEfkFBaGAd84pLp1kfE7xK3GdT8",
    "128z5d7nN7PkCuX5qoA4Ys6pmxUYnEy86k",
    "12CiUhYVTTH33w3SPUBqcpMoqnApAV4WCF",
    "12jbtzBb54r97TCwW3G1gCFoumpckRAPdY",
    "12JzYkkN76xkwvcPT6AWKZtGX6w2LAgsJg",
    "12VVRNPi4SJqUTsp6FmqDqY5sGosDtysn4",
    "13A3JrvMvg5w9XGvyyR4JEJqiLz8ZySY3",
    "13N66gCzWWHEZBxhVxG18P8wyjEWF9Yoi1",
    "13Q84TNNvgcL3HJiqQPvyBb9m4hxjS3jkV",
    "13zb1hQbWVsc2S7ZTZnP2G4undNNpdh5so",
    "13zYrYhhJxp6Ui1VV7pqa5WDhNWM45ARAC",
    "14iXhn8bGajVWegZHJ18vJLHhntcpL4dex",
    "14JHoRAdmJg3XR4RjMDh6Wed6ft6hzbQe9",
    "14MdEb4eFcT3MVG5sPFG4jGLuHJSnt1Dk2",
    "14oFNXucftsHiUMY8uctg6N487riuyXs4h",
    "14u4nA5sugaswb6SZgn5av2vuChdMnD9E5",
    "15ANYzzCp5BFHcCnVFzXqyibpzgPLWaD8b",
    "15c9mPGLku1HuW9LRtBf4jcHVpBUt8txKz",
    "15EJFC5ZTs9nhsdvSUeBXjLAuYq3SWaxTc",
    "15JhYXn6Mx3oF4Y7PcTAv2wVVAuCFFQNiP",
    "15K1YKJMiJ4fpesTVUcByoz334rHmknxmT",
    "15MnK2jXPqTMURX4xC3h4mAZxyCcaWWEDD",
    "15nf31J46iLuK1ZkTnqHo7WgN5cARFK3RA",
    "15qF6X51huDjqTmF9BJgxXdt1xcj46Jmhb",
    "15qsCm78whspNQFydGJQk5rexzxTQopnHZ",
    "15z9c9sVpu6fwNiK7dMAFgMYSK4GqsGZim",
    "16AbnZjZZipwHMkYKBSfswGWKDmXHjEpSf",
    "16jY7qLJnxb7CHZyqBP8qca9d51gAjyXQN",
    "16RGFo6hjq9ym6Pj7N5H7L1NR1rVPJyw2v",
    "16zRPnT8znwq42q7XeMkZUhb1bKqgRogyy",
    "174SNxfqpdMGYy5YQcfLbSTK3MRNZEePoy",
    "17aPYR1m6pVAacXg1PTDDU7XafvK1dxvhi",
    "17Q7tuG2JwFFU9rXVj3uZqRtioH3mx2Jad",
    "17s2b9ksz5y7abUm92cHwG8jEPCzK3dLnT",
    "17uDfp5r4n441xkgLFmhNoSW1KWp6xVLD",
    "18192XpzzdDi2K11QVHR7td2HcPS6Qs5vg",
    "1824ZJQ7nKJ9QFTRBqn7z7dHV5EGpzUpH3",
    "187swFMjz1G54ycVU56B7jZFHFTNVQFDiu",
    "18A7NA9FTsnJxWgkoFfPAFbQzuQxpRtCos",
    "18aNhurEAJsw6BAgtANpexk5ob1aGTwSeL",
    "18KsfuHuzQaBTNLASyj15hy4LuqPUo1FNB",
    "18ywPwj39nGjqBrQJSzZVq2izR12MDpDr8",
    "18ZMbwUFLMHoZBbfpCjUJQTCMCbktshgpe",
    "19EEC52krRUK1RkUAEZmQdjTyHT7Gp1TYT",
    "19eVSDuizydXxhohGh8Ki9WY9KsHdSwoQC",
    "19GpszRNUej5yYqxXoLnbZWKew3KdVLkXg",
    "19QciEHbGVNY4hrhfKXmcBBCrJSBZ6TaVt",
    "19vkiEajfhuZ8bs8Zu2jgmC6oqZbWqhxhG",
    "19YZECXj3SxEZMoUeJ1yiPsw8xANe7M7QR",
    "19z6waranEf8CcP8FqNgdwUe1QRxvUNKBG",
    "19ZewH8Kk1PDbSNdJ97FP4EiCjTRaZMZQA",
    "1Ab4vzG6wEQBDNQM1B2bvUz4fqXXdFk2WT",
    "1AcAmB6jmtU6AiEcXkmiNE9TNVPsj9DULf",
    "1AE8NzzgKE7Yhz7BWtAcAAxiFMbPo82NB5",
    "1AoeP37TmHdFh8uN72fu9AqgtLrUwcv2wJ",
    "1ARk8HWJMn8js8tQmGUJeQHjSE7KRkn2t8",
    "1AVJKwzs9AskraJLGHAZPiaZcrpDr1U6AB",
    "1AWCLZAjKbV1P7AHvaPNCKiB7ZWVDMxFiz",
    "1BCf6rHUW6m3iH2ptsvnjgLruAiPQQepLe",
    "1BDyrQ6WoF8VN3g9SAS1iKZcPzFfnDVieY",
    "1Be2UF9NLfyLFbtm3TCbmuocc9N1Kduci1",
    "1BgGZ9tcN4rm9KBzDn7KprQz87SZ26SAMH",
    "1BkkGsX9ZM6iwL3zbqs7HWBV7SvosR6m8N",
    "1Bxk4CQdqL9p22JEtDfdXMsng1XacifUtE",
    "1BY8GQbnueYofwSuFAT3USAhGjPrkxDdW9",
    "1CaBVPrwUxbQYYswu32w7Mj4HR4maNoJSX",
    "1CD91Vm97mLQvXhrnoMChhJx4TP9MaQkJo",
    "1CdufMQL892A69KXgv6UNBD17ywWqYpKut",
    "1CfZWK1QTQE3eS9qn61dQjV89KDjZzfNcv",
    "1CKCVdbDJasYmhswB6HKZHEAnNaDpK7W4n",
    "1CkR2uS7LmFwc3T2jV8C1BhWb5mQaoxedF",
    "1CMjscKB3QW7SDyQ4c3C3DEUHiHRhiZVib",
    "1CMq3SvFcVEcpLMuuH8PUcNiqsK1oicG2D",
    "1CQFwcjw1dwhtkVWBttNLDtqL7ivBonGPV",
    "1CUNEBjYrCn2y1SdiUMohaKUi4wpP326Lb",
    "1CXvTzR6qv8wJ7eprzUKeWxyGcHwDYP1i2",
    "1DBaumZxUkM4qMQRt2LVWyFJq5kDtSZQot",
    "1DFYhaB2J9q1LLZJWKTnscPWos9VBqDHzv",
    "1DJh2eHFYQfACPmrvpyWc8MSTYKh7w9eRF",
    "1Dn8NF8qDyyfHMktmuoQLGyjWmZXgvosXf",
    "1E32GPWgDyeyQac4aJxm9HVoLrrEYPnM4N",
    "1E6NuFjCi27W5zoXg8TRdcSRq84zJeBW3k",
    "1EeAxcprB2PpCnr34VfZdFrkUWuxyiNEFv",
    "1EhqbyUMvvs7BfL8goY6qcPbD6YKfPqb7e",
    "1EQJvpsmhazYCcKX5Au6AZmZKRnzarMVZu",
    "1ErZWg5cFCe4Vw5BzgfzB74VNLaXEiEkhk",
    "1EzVHtmbN4fs4MiNk3ppEnKKhsmXYJ4s74",
    "1F3JRMWudBaj48EhwcHDdpeuy2jwACNxjP",
    "1Fo65aKq8s8iquMt6weF1rku1moWVEd5Ua",
    "1FRoHA9xewq7DjrZ1psWJVeTer8gHRqEvR",
    "1FTpAbQa4h8trvhQXjXnmNhqdiGBd1oraE",
    "1FWGcVDK3JGzCC3WtkYetULPszMaK2Jksv",
    "1FwZXt6EpRT7Fkndzv6K4b4DFoT4trbMrV",
    "1Fz63c775VV9fNyj25d9Xfw3YHE6sKCxbt",
    "1G6EFyBRU86sThN3SSt3GrHu1sA7w7nzi4",
    "1GDSuiThEV64c166LUFC9uDcVdGjqkxKyh",
    "1GnNTmTVLZiqQfLbAdp9DVdicEnB5GoERE",
    "1GuBBhf61rnvRe4K8zu8vdQB3kHzwFqSy7",
    "1GvgAXVCbA8FBjXfWiAms4ytFeJcKsoyhL",
    "1HAX2n9Uruu9YDt4cqRgXcvtGvZj1rbUyt",
    "1HB1iKUqeffnVsvQsbpC6dNi1XKbyNuqao",
    "1HBtApAFA9B2YZw3G2YKSMCtb3dVnjuNe2",
    "1HduPEXZRdG26SUT5Yk83mLkPyjnZuJ7Bm",
    "1HsMJxNiV7TLxmoF6uJNkydxPFDog4NQum",
    "1Hz3uv3nNZzBVMXLGadCucgjiCs5W9vaGz",
    "1J36UjUByGroXcCvmj13U6uwaVv9caEeAt",
    "1JTK7s9YVYywfm5XUH7RNhHJH1LshCaRFR",
    "1JVnST957hGztonaWK6FougdtjxzHzRMMg",
    "1JWnE6p6UN7ZJBN7TtcbNDoRcjFtuDWoNL",
    "1K3x5L6G57Y494fDqBfrojD28UJv4s5JcK",
    "1K6xGMUbs6ZTXBnhw1pippqwK6wjBWtNpL",
    "1KCgMv8fo2TPBpddVi9jqmMmcne9uSNJ5F",
    "1Kh22PvXERd2xpTQk3ur6pPEqFeckCJfAr",
    "1Kn5h2qpgw9mWE5jKpk8PP4qvvJ1QVy8su",
    "1KNRfGWw7Q9Rmwsc6NT5zsdvEb9M2Wkj5Z",
    "1KrU4dHE5WrW8rhWDsTRjR21r8t3dsrS3R",
    "1KYUv7nSvXx4642TKeuC2SNdTk326uUpFy",
    "1L12FHH2FHjvTviyanuiFVfmzCy46RRATU",
    "1L2GM8eE7mJWLdo3HZS6su1832NX2txaac",
    "1L5sU9qvJeuwQUdt4y1eiLmquFxKjtHr3E",
    "1LeBZP5QCwwgXRtmVUvTVrraqPUokyLHqe",
    "1LhE6sCTuGae42Axu1L1ZB7L96yi9irEBE",
    "1LHtnpd8nU5VHEMkG2TMYYNUjjLc992bps",
    "1LuUHyrQr8PKSvbcY1v1PiuGuqFjWpDumN",
    "1LzhS3k3e9Ub8i2W1V8xQFdB8n2MYCHPCa",
    "1M7ipcdYHey2Y5RZM34MBbpugghmjaV89P",
    "1M92tSqNmQLYw33fuBvjmeadirh1ysMBxK",
    "1McVt1vMtCC7yn5b9wgX1833yCcLXzueeC",
    "1Me3ASYt5JCTAK2XaC32RMeH34PdprrfDx",
    "1Me6EfpwZK5kQziBwBfvLiHjaPGxCKLoJi",
    "1MEzite4ReNuWaL5Ds17ePKt2dCxWEofwk",
    "1MnJ6hdhvK37VLmqcdEwqC3iFxyWH2PHUV",
    "1MUJSJYtGPVGkBCTqGspnxyHahpt5Te8jy",
    "1MVDYgVaSN6iKKEsbzRUAYFrYJadLYZvvZ",
    "1MZ2L1gFrCtkkn6DnTT2e4PFUTHw9gNwaj",
    "1NBC8uXJy1GiJ6drkiZa1WuKn51ps7EPTv",
    "1NeGn21dUDDeqFQ63xb2SpgUuXuBLA4WT4",
    "1NevxKDYuDcCh1ZMMi6ftmWwGrZKC6j7Ux",
    "1NgVmsCCJaKLzGyKLFJfVequnFW9ZvnMLN",
    "1NLbHuJebVwUZ1XqDjsAyfTRUPwDQbemfv",
    "1NpnQyZ7x24ud82b7WiRNvPm6N8bqGQnaS",
    "1NpYjtLira16LfGbGwZJ5JbDPh3ai9bjf4",
    "1NtiLNGegHWE3Mp9g2JPkgx6wUg4TW7bbk",
    "1NWmZRpHH4XSPwsW6dsS3nrNWfL1yrJj4w",
    "1Pd8VvT49sHKsmqrQiP61RsVwmXCZ6ay7Z",
    "1PgQVLmst3Z314JrQn5TNiys8Hc38TcXJu",
    "1Pie8JkxBT6MGPz9Nvi3fsPkr2D8q3GBc1",
    "1PiFuqGpG8yGM5v6rNHWS3TjsG6awgEGA1",
    "1PitScNLyp2HCygzadCh7FveTnfmpPbfp8",
    "1PJZPzvGX19a7twf5HyD2VvNiPdHLzm9F6",
    "1PWABE7oUahG2AFFQhhvViQovnCr4rEv7Q",
    "1PWCx5fovoEaoBowAvF5k91m2Xat9bMgwb",
    "1PWo3JeB9jrGwfHDNpdGK54CRas7fsVzXU",
    "1PXAyUB8ZoH3WD8n5zoAthYjN15yN5CVq5",
    "1PxH3K1Shdjb7gSEoTX7UPDZ6SH4qGPrvq",
    "1PXv28YxmYMaB8zxrKeZBW8dt2HK7RkRPX",
    "1QCbW9HWnwQWiQqVo5exhAnmfqKRrCRsvW",
    "1QKBaU6WAeycb3DbKbLBkX7vJiaS8r42Xo",
    "1rSnXMr63jdCuegJFuidJqWxUPV7AtUf7",
    "1UDHPdovvR985NrWSkdWQDEQ1xuRiTALq",
]

# Converte a lista de endereços para um set para busca mais eficiente
target_addresses_set = set(data_address)

def get_puzzle_range(puzzle_number: int):
    """
    Calcula o intervalo MIN e MAX para um dado número de puzzle.
    """
    base_exp = puzzle_number - 1
    MIN = 1 << base_exp
    MAX = (MIN << 1) - 1
    return MIN, MAX

def get_progress_filename(puzzle_number: int) -> str:
    """Retorna o nome do arquivo de progresso para um dado número de puzzle."""
    return f"puzzle_{puzzle_number}_progress.txt"

def save_progress(puzzle_number: int, current_priv: int):
    """Salva a última chave privada verificada no arquivo de progresso."""
    filename = get_progress_filename(puzzle_number)
    try:
        with open(filename, 'w') as f:
            f.write(str(current_priv))
    except IOError as e:
        print(f"\n⚠️ Erro ao salvar progresso no arquivo {filename}: {e}")

def load_progress(puzzle_number: int) -> int | None:
    """Carrega a última chave privada verificada do arquivo de progresso."""
    filename = get_progress_filename(puzzle_number)
    if not os.path.exists(filename):
        return None
    try:
        with open(filename, 'r') as f:
            content = f.read().strip()
            if content:
                return int(content)
            return None
    except (IOError, ValueError) as e:
        print(f"\n⚠️ Erro ao carregar progresso do arquivo {filename}: {e}")
        return None

def find_private_key_in_range(target_addresses: set, xmin: int, xmax: int, start_priv: int, puzzle_number: int):
    """
    Procura por uma chave privada que corresponda a um dos endereços alvo
    dentro do intervalo [xmin, xmax] usando busca direta, com checkpointing.
    """
    print(f"🔍 Iniciando busca direta no intervalo de {hex(xmin)} a {hex(xmax)}...")
    print(f"▶️ Começando a busca a partir de: {hex(start_priv)}")

    # Garante que a busca não comece antes de xmin
    current_priv = max(xmin, start_priv)
    
    # Variável para controlar o checkpointing a cada 1 milhão de chaves
    checkpoint_interval = 1_000_000 
    
    for priv in range(current_priv, xmax + 1):
        try:
            key = Key.from_int(priv)
            if key.address in target_addresses:
                # Limpa a linha de progresso antes de imprimir o resultado final
                print("\r" + " " * 80 + "\r", end="", flush=True) 
                print(f"🎯 Endereço correspondente encontrado: {key.address}")
                print(f"🔑 Privkey (decimal): {priv}")
                save_progress(puzzle_number, priv) # Salva a chave encontrada
                return priv
        except Exception as e:
            print(f"\n⚠️ Erro ao processar privkey {priv}: {e}")
            # Não salvamos progresso em caso de erro, para tentar novamente
            continue
            
        # Imprime progresso na mesma linha
        if (priv - start_priv + 1) % 10000 == 0: # Atualiza a cada 10.000 tentativas para não sobrecarregar
            progress_message = f"➡️ Progresso: {priv - xmin + 1} chaves verificadas. Última privkey testada: {hex(priv)}"
            print(f"\r{progress_message.ljust(80)}", end="", flush=True) # ljust para preencher o restante da linha

        # Salva progresso a cada 1 milhão de chaves
        if (priv - start_priv + 1) % checkpoint_interval == 0:
            save_progress(puzzle_number, priv)
            print(f"\r✅ Progresso salvo: {hex(priv)}. Continuando...", end="", flush=True)

    # Limpa a linha de progresso final
    print("\r" + " " * 80 + "\r", end="", flush=True)
    print("🚫 Nenhuma chave encontrada no intervalo especificado.")
    return None

def main():
    puzzle_number = int(input("Digite o número do puzzle (ex: 68): "))
    MIN, MAX = get_puzzle_range(puzzle_number)

    print(f"\nIntervalo do puzzle #{puzzle_number}:")
    print(f"MIN = {hex(MIN)}")
    print(f"MAX = {hex(MAX)}\n")

    # Tenta carregar o progresso anterior
    last_saved_priv = load_progress(puzzle_number)
    start_search_from = MIN

    if last_saved_priv is not None:
        if last_saved_priv >= MAX:
            print(f"🎉 O puzzle {puzzle_number} já foi completamente verificado ou uma chave já foi encontrada e salva.")
            print(f"Última chave verificada/encontrada: {hex(last_saved_priv)}")
            # Se a última chave salva já é a MAX ou maior, não há mais o que procurar
            # Ou se a chave encontrada já foi salva, podemos carregar e exibir.
            key = Key.from_int(last_saved_priv)
            if key.address in target_addresses_set:
                print("\n--- Chave Encontrada Anteriormente ---")
                print("✅ Privkey (hex):", key.to_hex())
                print("🔑 WIF:", key.to_wif())
                print("📬 Address:", key.address)
            return # Sai do programa
        else:
            print(f"🔄 Retomando a busca a partir de: {hex(last_saved_priv + 1)}")
            start_search_from = last_saved_priv + 1
    else:
        print("🆕 Iniciando uma nova busca.")

    priv = find_private_key_in_range(target_addresses_set, MIN, MAX, start_search_from, puzzle_number)

    if priv:
        key = Key.from_int(priv)
        print("\n--- Chave Encontrada ---")
        print("✅ Privkey (hex):", key.to_hex())
        print("🔑 WIF:", key.to_wif())
        print("📬 Address:", key.address)
    else:
        print("\n❌ Nenhuma chave correspondente encontrada para os endereços fornecidos no intervalo.")
        # Se não encontrou, mas o last_saved_priv era menor que MAX, significa que o intervalo foi percorrido
        if last_saved_priv is None or last_saved_priv < MAX:
            save_progress(puzzle_number, MAX) # Salva o MAX para indicar que o intervalo foi concluído

if __name__ == "__main__":
    main()
