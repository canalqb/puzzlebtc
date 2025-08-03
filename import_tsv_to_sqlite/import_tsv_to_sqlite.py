caminho_arquivo_tsv = 'blockchair_bitcoin_addresses_and_balance_18052025.tsv'
nome_banco = 'banco.db'

def importar_tsv_para_sqlite(arquivo_tsv, banco):
    conexao = sqlite3.connect(banco)
    cursor = conexao.cursor()

    # Cria a tabela se não existir
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS enderecos (
            address TEXT PRIMARY KEY,
            balance INTEGER
        )
    ''')

    with open(arquivo_tsv, 'r', encoding='utf-8') as f:
        leitor = csv.reader(f, delimiter='\t')
        next(leitor, None)  # Pula o cabeçalho

        count = 0
        for linha in leitor:
            if len(linha) != 2:
                continue  # Pula linhas malformadas

            address, balance = linha
            try:
                cursor.execute('INSERT OR REPLACE INTO enderecos (address, balance) VALUES (?, ?)', (address, int(balance)))
                count += 1

                # Commit periódico para performance
                if count % 10000 == 0:
                    conexao.commit()
                    print(f"{count} linhas inseridas...")

            except Exception as e:
                print(f"Erro ao inserir linha: {linha} → {e}")

    conexao.commit()
    conexao.close()
    print(f"\nImportação concluída. Total de linhas inseridas: {count}")

if __name__ == "__main__":
    importar_tsv_para_sqlite(caminho_arquivo_tsv, nome_banco)
