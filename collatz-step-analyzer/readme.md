# 🔢 Analisador Otimizado dos Passos da Conjectura de Collatz

Este projeto consiste em um **script Python otimizado** para calcular o número de passos da famosa **Conjectura de Collatz** em intervalos definidos por potências de 2 (exemplo: números entre 2^bits e 2^(bits+1)-1), armazenando os resultados em um banco de dados SQLite.

---

## 🎯 Para que serve este script?

Este script foi desenvolvido para:

* **Calcular eficientemente a quantidade de passos** para que cada número no intervalo chegue a 1 segundo as regras da conjectura de Collatz.
* **Organizar os números em tabelas SQLite** separadas por quantidade de passos para fácil consulta e análise.
* **Aprimorar o desempenho** por meio de cache de resultados intermediários, evitando cálculos repetidos.
* Permitir a análise de grandes intervalos de números (até 160 bits), divididos em blocos para facilitar o processamento.

---

## ⚙️ Como funciona?

### Passos do processamento:

1. **Entrada do usuário**: informe a quantidade de bits para definir o intervalo (exemplo: 10 bits → intervalo de 2^10 a 2^11-1).
2. **Inicialização de cache** para armazenar resultados já calculados e acelerar o processamento.
3. **Iteração sobre todos os números do intervalo**, calculando o número de passos da Conjectura de Collatz.
4. **Agrupamento dos números em dicionário**, separando por quantidade de passos.
5. **Criação de tabelas SQLite dinamicamente** para cada quantidade de passos encontrada.
6. **Inserção em lote dos números nas tabelas correspondentes**.
7. Exibição de **estatísticas básicas** sobre a quantidade de números com mais passos que o limite inferior do intervalo.
8. Reporta o **tempo total de execução** do processo.

---

## 💡 Características principais

* **Otimização via cache:** evita recalcular passos já conhecidos.
* **Armazenamento estruturado:** facilita consultas e análises posteriores no banco SQLite.
* **Intervalos dinâmicos:** suporta intervalos gigantescos até 160 bits, facilitando escalabilidade.
* **Interface simples:** interação via terminal para definir o intervalo.

---

## 🚀 Como usar?

1. Clone o repositório e entre na pasta:

```bash
git clone https://github.com/canalqb/collatz-step-analyzer.git
cd collatz-step-analyzer
```

2. Execute o script Python:

```bash
python collatz_optimized_steps.py
```

3. Insira o número de bits desejado (de 1 a 160) quando solicitado.

4. Aguarde o processamento — os dados serão armazenados em um arquivo SQLite nomeado conforme o número de bits (ex: `10.db`).

---

## 📝 Exemplo de uso

```
Informe qual intervalo quer procurar (de 1 até 160 bits): 10

📌 Intervalo selecionado: 1024 até 2047
🔄 Passos de Collatz para 1024: 10
🔄 Passos de Collatz para 2047: 47

... (processamento e inserção no banco)

📊 Total de números com mais de 47 passos: 5

Tempo total de execução: 3.42 segundos
```

---

## 📬 Contato

Feito por [CanalQb no GitHub](https://github.com/canalqb)
Visite o blog: [canalqb.blogspot.com](https://canalqb.blogspot.com/)
💸 Apoie o projeto via Bitcoin: `13Ve1k5ivByaCQ5yer6GoV84wAtf3kNava`
