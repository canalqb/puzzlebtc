# 🧠 Geração de CSV com Análise Dinâmica de Meios Binários — Ultra Otimizado

Este repositório contém um poderoso script em Python que realiza uma análise extensa de números inteiros posicionados como *valores médios* em intervalos binários.

🛠️ O script não apenas processa esses valores, mas aplica **mais de 25 cálculos e transformações** sobre cada número, produzindo um **arquivo CSV com dados enriquecidos**, incluindo:

* Estatísticas binárias
* Operações lógicas
* Propriedades matemáticas
* Localização relativa no intervalo
* Análises de paridade e primalidade
* Cálculos otimizados de extremos com mesmo número de bits ativos

---

## 🧮 O que exatamente ele faz?

Para cada número na lista:

* 📏 Determina seu intervalo com base em potências de 2
* 🔢 Conta os bits `1` (popcount)
* 🧮 Calcula expressões como `n * bits`, `bits / n`, `(A / B)`
* 🧠 Verifica se o número é potência de 2
* 📍 Determina posição entre início e fim do intervalo
* 🔍 Aplica bitwise: `AND`, `OR`, `XOR`, `NOT`, `SHIFT`
* 🧪 Testa se o número é primo
* 🧬 Calcula "meio aritmético", "meio inferior" e "superior"
* 🧮 Estima média de bits do intervalo
* 🚀 Encontra o **menor e maior número com mesmo total de bits** ativos dentro do intervalo (*versão ultra otimizada*)

---

## 🧾 Exemplo de algumas colunas geradas:

| ID | 2^ID    | decimal  | Total de Bits | Potência de 2? | Paridade | É primo? | Binário                | Menor (k bits) | Maior (k bits) |
| -- | ------- | -------- | ------------- | -------------- | -------- | -------- | ---------------------- | -------------- | -------------- |
| 6  | 64      | 76       | 4             | ❌              | Par      | ❌        | `01001100`             | 68             | 89             |
| 11 | 2048    | 2683     | 9             | ❌              | Ímpar    | ✅        | `101001111011`         | 2567           | 2683           |
| 20 | 1048576 | 14428676 | 9             | ❌              | Ímpar    | ❌        | `11011011111101100100` | 14428162       | 14428686       |

---

## 🧑‍💻 Como usar

### ✅ Pré-requisitos:

* Python 3.x
* Apenas **bibliotecas padrão**: `csv`, `math`, `time`

### ▶️ Executar:

```bash
python gerador_csv_meios_ultra_otimizado.py
```

📄 Isso gerará o arquivo:

```
meios_completo_dinamico_ultra_otimizado.csv
```

---

## 📂 Conteúdo do CSV

Este arquivo contém **30 colunas**, entre elas:

* `ID`, `2^ID`, `decimal`, `2^(ID+1)-1`
* Total de bits `1`
* Paridade (par/ímpar)
* Potência de 2?
* Binário com padding
* Distância do início e do fim
* Posição percentual
* Teste de primalidade
* Operações bitwise: `&`, `|`, `^`, `~`, `<<`, `>>`
* Análise de meios: aritmético, inferior, superior
* Média de bits no intervalo
* 🔍 **Menor e maior com mesmo total de bits ativos** (otimizado!)

---

## ⚡ Performance

✅ A versão atual utiliza **estratégias matemáticas otimizadas** para reduzir drasticamente o tempo de cálculo dos extremos com `k` bits ativos.

⏱️ Tempo médio de execução: **< 2 segundos** para mais de 100 entradas, mesmo com análise completa.

---

## 🧪 Aplicações práticas

* 🔬 Análise de padrões binários
* 📚 Estudos de estruturas numéricas exponenciais
* 🧠 Geração de datasets com recursos matemáticos
* ⚙️ Pré-processamento para algoritmos de compressão ou criptografia
* 📊 Enriquecimento de dados para aprendizado de máquina

---

## 📬 Contato

Feito por [**CanalQb no GitHub**](https://github.com/canalqb)
🌐 Visite o blog: [canalqb.blogspot.com](https://canalqb.blogspot.com/)
💸 Apoie o projeto via Bitcoin:
`13Ve1k5ivByaCQ5yer6GoV84wAtf3kNava` 
