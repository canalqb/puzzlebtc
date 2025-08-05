### 🧬 `README.md` – *BTC Genetic Finder*

> ⚠️ **Aviso Legal:** Este projeto é educacional e demonstra como algoritmos genéticos funcionam em problemas computacionalmente inviáveis. **Não é um método viável ou legal para obter acesso a carteiras Bitcoin alheias.**

---

# 🧬 BTC Genetic Finder

> *Algoritmo genético para tentar encontrar uma chave privada de Bitcoin entre endereços conhecidos.*

🔍 Este projeto utiliza **algoritmos genéticos** para explorar o espaço de chaves privadas de forma probabilística, simulando um ataque *brute force* com estratégias evolutivas.

---

## 🧠 Como Funciona?

Este script:

1. Gera indivíduos aleatórios (sequências binárias);
2. Converte cada indivíduo em um número inteiro;
3. Transforma o número em uma chave privada Bitcoin;
4. Verifica se o endereço público gerado está entre os **endereços-alvo conhecidos**;
5. Evolui a população utilizando **seleção**, **cruzamento**, **mutação** e **avaliação de fitness** até encontrar uma correspondência ou atingir o número máximo de gerações.

---

## 🚀 Tecnologias Utilizadas

* 🐍 Python 3
* 🧬 [DEAP](https://deap.readthedocs.io/) – Framework de Algoritmos Genéticos
* 🔑 [bit](https://ofek.dev/bit/) – Biblioteca para manipulação de chaves Bitcoin
* 🧵 `multiprocessing` para paralelismo

---

## ⚙️ Requisitos

Instale os pacotes necessários com:

```bash
pip install deap bit
```

---

## 🛠️ Como Usar

### 1. Clone o repositório:

```bash
git clone https://github.com/seuusuario/btc-genetic-finder.git
cd btc-genetic-finder
```

### 2. Edite os dados:

O script já contém uma lista de endereços `data_address`. Você pode substituir ou adicionar os seus alvos dentro dessa lista.

### 3. Execute o script:

```bash
python btc_bruteforce_ga.py
```

---

## 📈 Exemplo de Saída

```
Target address selected: 13zb1hQbWVsc2S7ZTZnP2G4undNNpdh5so
Initial max fitness: 0
Gen 10: MaxFitness=1 Score=21 WIF: Kx... Address= 13z... TimeElapsed=12.38s
...
=== Final Result ===
Target Address: 13zb1hQbWVsc2S7ZTZnP2G4undNNpdh5so
Generation: 184
Best Score: 34
Best Address: 13zb1hQbWVsc2S7ZTZnP2G4undNNpdh5so
Secret (bin): 010010111010101...
Secret (int): 98126361231328
WIF: KwDiBf89QgGbjEhKnhXJu...
```

---

## ⚠️ Importante Saber

* 🔓 A chance de **acertar uma chave real de Bitcoin por força bruta é praticamente nula**, mesmo com estratégias genéticas.
* 💡 O propósito é **educacional**, para demonstrar como algoritmos evolutivos podem ser aplicados em problemas altamente complexos.
* ⛔ *Utilizar este script com intenções maliciosas é ilegal e contra os termos de uso do software livre.*

---

## 📬 Contato

Feito por [**CanalQb no GitHub**](https://github.com/canalqb)
📚 Visite o blog: [**canalqb.blogspot.com**](https://canalqb.blogspot.com/)
💸 Apoie o projeto via Bitcoin:

```
13Ve1k5ivByaCQ5yer6GoV84wAtf3kNava
```

---

## 🧠 Palavras-chave

`bitcoin` · `genetic algorithm` · `brute force` · `evolutionary` · `machine learning` · `crypto security` · `education`
