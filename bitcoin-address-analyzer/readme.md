---

# 🔍 Bitcoin Address Analyzer

Este projeto é um script Python que analisa e gera endereços de Bitcoin a partir de chaves privadas dentro de um intervalo baseado em valores `n`, verificando se algum endereço gerado já existe em um banco de dados local.

## 🧠 Como funciona?

Dado um número `n`, o script irá:

1. Gerar um intervalo entre `2^n` e `2^(n+1) - 1`.
2. Criar chaves privadas com diferentes quantidades de bits ativos.
3. Gerar os seguintes tipos de endereços Bitcoin:

   * Legacy (Compressed e Uncompressed)
   * P2SH (P2WPKH)
   * Bech32 (P2WPKH)
4. Comparar os endereços gerados com um banco de dados SQLite contendo endereços reais de Bitcoin.
5. Salvar os resultados encontrados no arquivo `verbit2_chaves_encontradas.txt`.
6. Exportar um relatório em CSV com pares de varredura entre diferentes grupos de bits.

## 📦 Pré-requisitos

* Python 3.8+

* Dependências:

  ```bash
  pip install ecdsa base58 bit psutil
  ```

* Banco de dados SQLite com a tabela:

  ```sql
  enderecos(address TEXT)
  ```

## 🧪 Execução

Execute o script com:

```bash
python analisar_enderecos.py
```

Você será solicitado a digitar o valor de `n`, por exemplo:

```
Digite o valor de n (ex: 71):
```

⚠️ O valor de `n` deve estar entre **1 e 612**.

## 🗃️ Estrutura de diretórios sugerida

```plaintext
bitcoin-address-analyzer/
├── analisar_enderecos.py
├── verbit2_chaves_encontradas.txt
├── pares_loop_n<N>.csv
├── banco.db              # (fora do repositório ou listado no .gitignore)
└── README.md
```

## ⚙️ Configurações

Algumas configurações importantes no script:

* `CAMINHO_BANCO`: caminho para o banco SQLite contendo endereços.
* `ARQUIVO_CHAVES_ENCONTRADAS`: onde as chaves encontradas são salvas.

Você pode alterar esses valores diretamente no script conforme necessário.

## ⚠️ Avisos

* O script **não realiza brute-force massivo**. Ele foca em explorar padrões específicos (como número fixo de bits ativos).
* Ideal para análise estatística, auditoria ou estudo de distribuição de endereços.
* Use **com responsabilidade**.

## 📬 Contato

Feito por [CanalQb no GitHub](https://github.com/canalqb)  
Visite o blog: [canalqb.blogspot.com](https://canalqb.blogspot.com/)  
💸 Que tal apoiar a ideia? Bitcoin: `13Ve1k5ivByaCQ5yer6GoV84wAtf3kNava`
