from itertools import combinations
import os
import sqlite3
import psutil
from bit import Key

# Constantes
SECP256K1_N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
CAMINHO_BANCO = "D:/Rodrigo/20052025/blockchair/banco.db"

def definir_prioridade_baixa():
    """Reduz a prioridade do processo para não travar o sistema."""
    try:
        p = psutil.Process(os.getpid())
        p.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    except Exception:
        try:
            os.nice(10)
        except Exception:
            print("⚠ Aviso: Não foi possível definir prioridade baixa.")

def conectar_banco_somente_leitura(caminho):
    """Conecta ao banco SQLite em modo somente leitura."""
    uri = f"file:{caminho}?mode=ro"
    return sqlite3.connect(uri, uri=True)

def potencias_de_2_ate_n(n):
    """Retorna potências de 2 até o bit length de n."""
    return [1 << i for i in range(n.bit_length())]

def gerar_mascaras_maiores(fim, max_bits_ligados):
    """Gera máscaras com exatamente max_bits_ligados bits ligados até o bit length de fim."""
    bits_possiveis = potencias_de_2_ate_n(fim)
    
    for combo in combinations(bits_possiveis, max_bits_ligados):
        mascara = sum(combo)
        yield mascara

def main():
    definir_prioridade_baixa()
    print("🔗 Conectando ao banco de dados...")
    
    try:
        conexao = conectar_banco_somente_leitura(CAMINHO_BANCO)
        cursor = conexao.cursor()
    except Exception as e:
        print(f"❌ Erro ao conectar ao banco: {e}")
        return

    fim = 2**160  # Não ultrapasse isso com bits demais!
    max_bits_ligados = 20  # Ajuste conforme a memória disponível

    mascaras_geradas = list(gerar_mascaras_maiores(fim, max_bits_ligados))
    print(f"✅ Geradas {len(mascaras_geradas)} máscaras com {max_bits_ligados} bits ligados.")

    print("📄 Consultando endereços no banco...")
    for m in mascaras_geradas:
        if 1 <= m < SECP256K1_N:
            try:
                bytes_valor = m.to_bytes(32, 'big')  # 32 bytes para chave privada
                private_key = Key.from_bytes(bytes_valor)
                wif = private_key.to_wif()
                address = private_key.address

                # Consulta ao banco
                cursor.execute("SELECT address FROM enderecos WHERE address = ?", (address,))
                resultado = cursor.fetchone()

                if resultado:
                    with open("chave_encontrada.txt", "a") as f:
                        f.write(f"WIF: {wif} - End: {address}\n")
                    print(f"\n🔒 Chave encontrada!\nWIF: {wif}\nEndereço: {address}")
                    return  # Encerra após encontrar

                # Opcional: mostrar progresso
                #print(f" -> {bin(m)}")
                print(f"🔍 {m} - {address} - não encontrado.",end="\r")

            except Exception as e:
                print(f"⚠ Erro ao processar valor {m}: {e}")
        else:
            print(f"⚠ Valor fora dos limites SECP256k1: {m}")

    print("✅ Fim do processamento.")
    conexao.close()

if __name__ == "__main__":
    main()
