📄 README.md
# 📥 BTC Address Importer

Este projeto importa um arquivo `.tsv` contendo endereços de Bitcoin e seus respectivos saldos para um banco de dados SQLite. Útil para análises offline, busca por endereços específicos ou integração com sistemas de monitoramento.

## 🧾 Formato do arquivo .tsv

O arquivo `.tsv` (tab-separated values) deve conter as seguintes colunas, sem cabeçalhos extras:

address<TAB>balance

Exemplo:

1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa\t682344791
3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy\t0


## 📂 Estrutura do banco de dados

O script cria um banco SQLite chamado `banco.db` com uma tabela chamada `enderecos` contendo:

| Coluna  | Tipo    | Descrição                          |
|---------|---------|------------------------------------|
| address | TEXT    | Endereço Bitcoin (chave primária) |
| balance | INTEGER | Saldo em satoshis                 |

## ▶️ Como usar

1. Instale os requisitos:
```bash
pip install -r requirements.txt
Coloque seu arquivo .tsv no diretório do projeto e ajuste o nome do arquivo no script, se necessário.

Execute o script:

python import_tsv_to_sqlite.py

📦 Requisitos

Python 3.7+

Bibliotecas: sqlite3 (nativo), csv (nativo)

🧠 Observações
O script realiza commits a cada 10.000 linhas para melhor desempenho em grandes volumes.

Linhas malformadas (com menos ou mais de 2 colunas) são ignoradas.

O campo balance é convertido para inteiro automaticamente.

⚠️ Aviso legal: Este projeto é para fins educacionais. Não use para atividades maliciosas ou para explorar sistemas sem permissão.

 
---

### 📦 `requirements.txt`

```txt
# Nenhuma biblioteca externa necessária
# sqlite3 e csv são nativos do Python

# Caso queira forçar uma versão mínima do Python:
python_version >= 3.7
