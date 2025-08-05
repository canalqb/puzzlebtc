# 📊 Geração de Tabela Expandida com Dados Binários e Estatísticas de Meios

Este projeto executa uma análise aprofundada de uma lista de valores centrais (*"meios"*) associados a intervalos potenciais em potências de 2. Ele calcula e exporta um arquivo `.csv` com **10 colunas de estatísticas binárias e matemáticas**, ideais para exploração de padrões em dados exponenciais.

---

## 🧠 O que o script faz?

✅ **Recebe** uma lista de valores (alguns válidos, outros nulos)
✅ **Calcula automaticamente** colunas derivadas como:

* Potência de 2 mais próxima (`2^ID`)
* Intervalo superior (`2^(ID+1)-1`)
* Número de bits `1` no valor e em `(2n - 1)`
* Operações combinadas como `n * bits`, `bits/n` e `A / B`

✅ **Exporta um CSV** delimitado por `;` com cabeçalhos legíveis
✅ Lida com valores ausentes (`None`) de forma segura

---

## 🔢 Exemplo de colunas geradas

| ID | 2^ID | decimal | 2^(ID+1)-1 | Total de Bits | A = decimal × bits | B = bits / decimal | A / B   | D = 2×decimal−1 | E = bits(D) |
| -- | ---- | ------- | ---------- | ------------- | ------------------ | ------------------ | ------- | --------------- | ----------- |
| 6  | 64   | 76      | 127        | 4             | 304                | 0.052632           | 5776    | 151             | 5           |
| 9  | 512  | 514     | 1023       | 5             | 2570               | 0.009727           | 264272  | 1027            | 6           |
| 11 | 2048 | 2683    | 4095       | 9             | 24147              | 0.003353           | 7201406 | 5365            | 7           |

---

## 🛠 Como usar

1. Clone o repositório:

   ```bash
   git clone https://github.com/seu-usuario/csv-meios-expandido
   cd csv-meios-expandido
   ```

2. Execute o script:

   ```bash
   python gerar_csv_meios.py
   ```

3. Veja o resultado:

   ```
   ✅ CSV 'meios_expandido.csv' gerado com sucesso com 10 colunas.
   ```

4. Abra o arquivo `meios_expandido.csv` no Excel, LibreOffice ou qualquer editor de planilhas que aceite `;` como delimitador.

---

## 📌 Finalidade

Este projeto pode ser útil para:

* 🔍 **Análise exploratória de dados** logarítmicos
* 📚 **Estudos de distribuições binárias**
* 🧠 **Modelagem de padrões computacionais**
* 📊 **Geração de features para modelos de machine learning**

---

## 📦 Requisitos

Este script é leve e só usa bibliotecas da **standard library do Python**:

* `csv`
* `math`

**✔️ Nenhuma instalação extra é necessária.**

---

## 📬 Contato

Feito por [**CanalQb no GitHub**](https://github.com/canalqb)
📘 Visite o blog: [canalqb.blogspot.com](https://canalqb.blogspot.com/)
💸 Apoie o projeto via Bitcoin:
`13Ve1k5ivByaCQ5yer6GoV84wAtf3kNava`
