# 📊 Bit Ranges Summary - bit_ranges_summary.py

Bem-vindo ao **Bit Ranges Summary**, um script Python que analisa números inteiros em intervalos de potências de dois e gera uma tabela detalhada com informações sobre a contagem de bits ligados (bits 1) em cada número.

---

## ✨ Para que serve este script?

Este script tem como objetivo principal gerar uma tabela CSV que mostra, para cada intervalo de números entre potências consecutivas de 2, o seguinte:

* **Quantidade total** de números que possuem exatamente `k` bits ligados, para vários valores de `k`.
* O **menor** e o **maior número** encontrados em cada categoria de `k` bits ligados.
* A **diferença** entre o maior e menor número para cada categoria.
* Além disso, soma os valores mínimos, máximos e as diferenças para todas as categorias dentro de cada intervalo.

---

## 🔍 Como funciona?

1. Para cada `n` de 1 a 9:

   * Define um intervalo entre `2^n` e `2^(n+1) - 1`.
2. Para cada número neste intervalo:

   * Conta quantos bits estão ligados (`1`) em sua representação binária.
   * Armazena estatísticas por quantidade de bits ligados:

     * Quantidade de números,
     * Menor número,
     * Maior número.
3. Calcula somas agregadas:

   * Soma dos menores números,
   * Soma dos maiores números,
   * Soma das diferenças (maior - menor).
4. Gera um arquivo CSV contendo:

   * ID do intervalo, início e fim,
   * Somatórios,
   * Estatísticas detalhadas para cada quantidade de bits ligados.

---

## 📁 Arquivo gerado

* `tabela_bits_com_somas.csv`

Contém a tabela com todas as informações organizadas e separadas por ponto e vírgula (`;`), pronta para análise ou visualização em Excel, LibreOffice Calc, ou outro software de sua preferência.

---

## 🚀 Como usar

1. Clone ou baixe o repositório.

2. Navegue até a pasta `bit_analysis`.

3. Execute o script com Python 3:

   ```bash
   python bit_ranges_summary.py
   ```

4. O arquivo `tabela_bits_com_somas.csv` será criado na mesma pasta.

---

## 🛠️ Requisitos

* Python 3.x
* Módulo `csv` (padrão na biblioteca do Python)

---

## 💬 Contato

Feito por [CanalQb no GitHub](https://github.com/canalqb)
Visite o blog: [canalqb.blogspot.com](https://canalqb.blogspot.com/)
💸 Apoie o projeto via Bitcoin: `13Ve1k5ivByaCQ5yer6GoV84wAtf3kNava`

---

## 📈 Visualização rápida

| ID | Início | Fim | Soma dos Mínimos | Soma dos Máximos | Soma das Diferenças | ... |
| -- | ------ | --- | ---------------- | ---------------- | ------------------- | --- |
| 1  | 2      | 3   | 2                | 3                | 1                   | ... |

*(Tabela completa no arquivo CSV)*
