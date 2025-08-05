# 📊 Decimal Analyzer - Processador de Dados Numéricos com Alta Precisão

Este projeto foi desenvolvido para **ler, interpretar e transformar arquivos com dados decimais ou intervalos numéricos**, mesmo quando esses dados contêm valores ausentes (como `None`).
É ideal para análises de séries numéricas, transformações estruturadas e preparação de datasets para exploração ou visualização.

---

## 🎯 O que este script faz?

* 📂 Lê um arquivo `decimais.txt` contendo linhas com 3 valores separados por vírgula: **início**, **passos**, **fim**.
* ✅ Trata linhas com valores ausentes (`None`) sem quebrar o fluxo de execução.
* 🧠 Calcula:

  * Intervalo (`fim - início + 1`)
  * Número de blocos de 255 unidades
  * Proporção de passos sobre o intervalo com **alta precisão decimal**
* 💾 Salva os resultados em um arquivo CSV separado por `;` chamado `saida.csv`.

---

## 🧮 Exemplo de entrada (`decimais.txt`)

```
1000, 500, 2000
None, 300, 500
1500, 255, 3000
```

---

## 📦 Exemplo de saída (`saida.csv`)

| 'Inicio |  'Fim | 'Passos | 'Intervalo | 'Blocos\_255 | 'Proporcao |
| ------: | ----: | ------: | ---------: | -----------: | ---------: |
|   '1000 | '2000 |    '500 |      '1001 |     '3.92549 |   '0.49950 |
|   'None |  '500 |    '300 |      'None |        'None |      'None |
|   '1500 | '3000 |    '255 |      '1501 |     '5.89019 |   '0.16988 |

> ⚠️ Todas as colunas começam com apóstrofo `'` para forçar o Excel a interpretar os dados como texto (inclusive números grandes).

---

## ⚙️ Como usar

### 1. 🔧 Requisitos

* Python 3.7+
* Nenhuma biblioteca externa necessária (apenas `csv` e `decimal`, que são nativas do Python)

### 2. 📥 Coloque seu arquivo `decimais.txt` na mesma pasta do script

Cada linha deve conter 3 valores separados por vírgula:
`inicio, passos, fim` (ex: `1000, 500, 2000`)

### 3. ▶️ Execute o script

```bash
python processar_decimais.py
```

### 4. 📁 Resultado

Um arquivo `saida.csv` será criado com as colunas:

* `'Inicio`
* `'Fim`
* `'Passos`
* `'Intervalo`
* `'Blocos_255`
* `'Proporcao`

> 📌 O script trata valores `None` e garante que o CSV seja gerado mesmo com entradas incompletas.

---

## 🧠 Técnicas utilizadas

* **Alta precisão com `decimal.Decimal`** (precisão definida para 50 casas decimais)
* **Tratamento robusto de erros e dados incompletos**
* **Formatação compatível com Excel (colunas com `'`)**

---

## 💡 Dicas

* Você pode adaptar o script para processar outros tipos de métricas.
* Ideal para análises de séries temporais, faixas numéricas ou dimensionamentos.

---

## 📬 Contato

Feito por [CanalQb no GitHub](https://github.com/canalqb)
Visite o blog: [canalqb.blogspot.com](https://canalqb.blogspot.com/)
💸 Apoie o projeto via Bitcoin: `13Ve1k5ivByaCQ5yer6GoV84wAtf3kNava`
