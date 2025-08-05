import math
from decimal import Decimal, getcontext, ROUND_HALF_EVEN
from bit import Key
import psutil
import os
import sys

try:
    p = psutil.Process(os.getpid())
    p.nice(psutil.IDLE_PRIORITY_CLASS)  # Prioridade mínima no Windows
except Exception as e:
    print(f"⚠️ Não foi possível definir prioridade mínima: {e}", file=sys.stderr)

# Aumentar precisão para operações decimais
getcontext().prec = 100

# Lista fixa de endereços conhecidos
enderecos = {
    "1PWo3JeB9jrGwfHDNpdGK54CRas7fsVzXU",
    "1JTK7s9YVYywfm5XUH7RNhHJH1LshCaRFR",
    "12VVRNPi4SJqUTsp6FmqDqY5sGosDtysn4",
    "1FWGcVDK3JGzCC3WtkYetULPszMaK2Jksv",
    "1DJh2eHFYQfACPmrvpyWc8MSTYKh7w9eRF",
    "1Bxk4CQdqL9p22JEtDfdXMsng1XacifUtE",
    "15qF6X51huDjqTmF9BJgxXdt1xcj46Jmhb",
    "1ARk8HWJMn8js8tQmGUJeQHjSE7KRkn2t8",
    "15qsCm78whspNQFydGJQk5rexzxTQopnHZ",
    "13zYrYhhJxp6Ui1VV7pqa5WDhNWM45ARAC",
    "14MdEb4eFcT3MVG5sPFG4jGLuHJSnt1Dk2",
    "1CMq3SvFcVEcpLMuuH8PUcNiqsK1oicG2D",
    "1K3x5L6G57Y494fDqBfrojD28UJv4s5JcK",
    "1PxH3K1Shdjb7gSEoTX7UPDZ6SH4qGPrvq",
    "16AbnZjZZipwHMkYKBSfswGWKDmXHjEpSf",
    "19QciEHbGVNY4hrhfKXmcBBCrJSBZ6TaVt",
    "1EzVHtmbN4fs4MiNk3ppEnKKhsmXYJ4s74",
    "1AE8NzzgKE7Yhz7BWtAcAAxiFMbPo82NB5",
    "17Q7tuG2JwFFU9rXVj3uZqRtioH3mx2Jad",
    "1K6xGMUbs6ZTXBnhw1pippqwK6wjBWtNpL",
    "15ANYzzCp5BFHcCnVFzXqyibpzgPLWaD8b",
    "18ywPwj39nGjqBrQJSzZVq2izR12MDpDr8",
    "1CaBVPrwUxbQYYswu32w7Mj4HR4maNoJSX",
    "1JWnE6p6UN7ZJBN7TtcbNDoRcjFtuDWoNL",
    "1CKCVdbDJasYmhswB6HKZHEAnNaDpK7W4n",
    "1PXv28YxmYMaB8zxrKeZBW8dt2HK7RkRPX",
    "1AcAmB6jmtU6AiEcXkmiNE9TNVPsj9DULf",
    "1EQJvpsmhazYCcKX5Au6AZmZKRnzarMVZu",
    "18KsfuHuzQaBTNLASyj15hy4LuqPUo1FNB",
    "15EJFC5ZTs9nhsdvSUeBXjLAuYq3SWaxTc",
    "1HB1iKUqeffnVsvQsbpC6dNi1XKbyNuqao",
    "1GvgAXVCbA8FBjXfWiAms4ytFeJcKsoyhL",
    "1824ZJQ7nKJ9QFTRBqn7z7dHV5EGpzUpH3",
    "18A7NA9FTsnJxWgkoFfPAFbQzuQxpRtCos",
    "1NeGn21dUDDeqFQ63xb2SpgUuXuBLA4WT4",
    "174SNxfqpdMGYy5YQcfLbSTK3MRNZEePoy",
    "1MnJ6hdhvK37VLmqcdEwqC3iFxyWH2PHUV",
    "1KNRfGWw7Q9Rmwsc6NT5zsdvEb9M2Wkj5Z",
    "1PJZPzvGX19a7twf5HyD2VvNiPdHLzm9F6",
    "1GuBBhf61rnvRe4K8zu8vdQB3kHzwFqSy7",
    "1GDSuiThEV64c166LUFC9uDcVdGjqkxKyh",
    "1Me3ASYt5JCTAK2XaC32RMeH34PdprrfDx",
    "1CdufMQL892A69KXgv6UNBD17ywWqYpKut",
    "1BkkGsX9ZM6iwL3zbqs7HWBV7SvosR6m8N",
    "1AWCLZAjKbV1P7AHvaPNCKiB7ZWVDMxFiz",
    "1G6EFyBRU86sThN3SSt3GrHu1sA7w7nzi4",
    "1MZ2L1gFrCtkkn6DnTT2e4PFUTHw9gNwaj",
    "1Hz3uv3nNZzBVMXLGadCucgjiCs5W9vaGz",
    "16zRPnT8znwq42q7XeMkZUhb1bKqgRogyy",
    "1KrU4dHE5WrW8rhWDsTRjR21r8t3dsrS3R",
    "17uDfp5r4n441xkgLFmhNoSW1KWp6xVLD",
    "13A3JrvXmvg5w9XGvyyR4JEJqiLz8ZySY3",
    "16RGFo6hjq9ym6Pj7N5H7L1NR1rVPJyw2v",
    "1UDHPdovvR985NrWSkdWQDEQ1xuRiTALq",
    "15nf31J46iLuK1ZkTnqHo7WgN5cARFK3RA",
    "1Ab4vzG6wEQBDNQM1B2bvUz4fqXXdFk2WT",
    "1Fz63c775VV9fNyj25d9Xfw3YHE6sKCxbt",
    "1QKBaU6WAeycb3DbKbLBkX7vJiaS8r42Xo",
    "1CD91Vm97mLQvXhrnoMChhJx4TP9MaQkJo",
    "15MnK2jXPqTMURX4xC3h4mAZxyCcaWWEDD",
    "13N66gCzWWHEZBxhVxG18P8wyjEWF9Yoi1",
    "1NevxKDYuDcCh1ZMMi6ftmWwGrZKC6j7Ux",
    "19GpszRNUej5yYqxXoLnbZWKew3KdVLkXg",
    "1M7ipcdYHey2Y5RZM34MBbpugghmjaV89P",
    "18aNhurEAJsw6BAgtANpexk5ob1aGTwSeL",
    "1FwZXt6EpRT7Fkndzv6K4b4DFoT4trbMrV",
    "1CXvTzR6qv8wJ7eprzUKeWxyGcHwDYP1i2",
    "1MUJSJYtGPVGkBCTqGspnxyHahpt5Te8jy",
    "13Q84TNNvgcL3HJiqQPvyBb9m4hxjS3jkV",
    "1LuUHyrQr8PKSvbcY1v1PiuGuqFjWpDumN",
    "18192XpzzdDi2K11QVHR7td2HcPS6Qs5vg",
    "1NgVmsCCJaKLzGyKLFJfVequnFW9ZvnMLN",
    "1AoeP37TmHdFh8uN72fu9AqgtLrUwcv2wJ",
    "1FTpAbQa4h8trvhQXjXnmNhqdiGBd1oraE",
    "14JHoRAdmJg3XR4RjMDh6Wed6ft6hzbQe9",
    "19z6waranEf8CcP8FqNgdwUe1QRxvUNKBG",
    "14u4nA5sugaswb6SZgn5av2vuChdMnD9E5",
    "1NBC8uXJy1GiJ6drkiZa1WuKn51ps7EPTv",


}

# Constante da curva SECP256K1
SECP256K1_N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

# ... [código anterior inalterado até o final da lista "enderecos"] ...

def gerar_bloco_e_imprimir(bloco: int, tag: str, id: int, m: float, passo_atual: Decimal):
    valor = Decimal(bloco)
    if not (1 <= bloco < SECP256K1_N):
        return

    try:
        inteiro_inicial = int(valor * passo_atual * Decimal(256))
        inteiro_final = inteiro_inicial + 255  # 256 valores

        if inteiro_inicial >= SECP256K1_N:
            return

        k = Key.from_int(inteiro_inicial)
        wif = k.to_wif()
        legacy = getattr(k, 'address', 'N/A')
        p2sh = getattr(k, 'segwit_address', 'N/A')
        bech32 = getattr(k, 'bech32_address', 'N/A')

        match_legacy = legacy in enderecos
        match_p2sh = p2sh in enderecos
        match_bech32 = bech32 in enderecos

        '''print(
            f"🔐 [m={m}] ID={id} {tag} | BLOCO={bloco} "
            f"({bloco} * {passo_atual} * 256 = {inteiro_inicial}) INTERVALO={inteiro_inicial}..{inteiro_final} "
            f"WIF: {wif} "
            f"{legacy} {'✅' if match_legacy else ''} "
            f"{p2sh} {'✅' if match_p2sh else ''} "
            f"{bech32} {'✅' if match_bech32 else ''}", end="\r"
        )'''
        print(f"WIF: {wif} " , end="\r")

        if match_legacy or match_p2sh or match_bech32:
            with open("valoresdeaddres.txt", "a", encoding="utf-8") as f:
                if match_legacy:
                    f.write(f"WIF: {wif} | Legacy: {legacy}\n")
                if match_p2sh:
                    f.write(f"WIF: {wif} | P2SH: {p2sh}\n")
                if match_bech32:
                    f.write(f"WIF: {wif} | Bech32: {bech32}\n")

    except Exception as e:
        print(f"❌ Erro ao gerar WIF para valor {bloco}: {e}", end="\r")



def main():
    try:
        m_inicial = float(input("Informe o menor multiplicador (pode ser decimal): "))
        m_final = float(input("Informe o maior multiplicador (pode ser decimal): "))
        passo = float(input("Informe o passo entre os multiplicadores (ex: 0.5): "))
        id_inicial = int(input("Informe o ID inicial (ex: 0): "))
        id_final = int(input("Informe o ID final (ex: 160): "))
    except ValueError:
        print("❌ Entrada inválida. Use números válidos.")
        return

    if m_final < m_inicial or passo <= 0 or id_final < id_inicial or id_inicial < 0:
        print("❌ Valores inválidos. Verifique os intervalos.")
        return

    casas_decimais_max = 5
    passo_decimal_original = Decimal(str(passo))
    m_inicial_dec = Decimal(str(m_inicial))
    m_final_dec = Decimal(str(m_final))

    for casas in range(casas_decimais_max + 1):
        divisor = Decimal('10') ** casas
        passo_atual = (passo_decimal_original / divisor).quantize(Decimal(f'1e-{casas}'))

        print(f"\n🔄 Iniciando busca com passo = {passo_atual}")

        multiplicadores = []
        m = m_inicial_dec

        while m <= m_final_dec + Decimal("1e-12"):
            multiplicadores.append(m)
            m += passo_atual

        if len(multiplicadores) == 1:
            multiplicadores = []
            base = m_inicial_dec
            for i in range(casas + 1):
                multiplicadores.append(base / (Decimal('10') ** i))

        print("Multiplicadores gerados:", [float(x) for x in multiplicadores])

        for id in range(id_inicial, id_final + 1):
            intervalo_ini = 2 ** id
            intervalo_fim = (2 ** (id + 1)) - 1

            intervalo_total = intervalo_fim - intervalo_ini + 1
            tamanho_bloco = intervalo_total // 256  # divide em 256 partes

            for i in range(256):
                bloco_base = intervalo_ini + (i * tamanho_bloco)

                for m in multiplicadores:
                    gerar_bloco_e_imprimir(bloco_base, f"2^{id}={intervalo_ini} FIM={intervalo_fim}", id, float(m), passo_atual)



if __name__ == "__main__":
    main()
