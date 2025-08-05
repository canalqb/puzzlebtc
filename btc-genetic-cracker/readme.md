# 🧬 BTC Genetic Cracker - btc_cracker.py

⚡ Uma ferramenta de força bruta baseada em algoritmo genético para buscar endereços Bitcoin específicos a partir de chaves privadas.</p>

---

## 🚀 O que este script faz?

Este projeto é um **experimento computacional** que utiliza um **algoritmo genético** para gerar e testar **chaves privadas** de Bitcoin em busca de **endereços públicos previamente definidos**.

🔍 O processo é altamente otimizado e executado com múltiplos núcleos, aplicando técnicas de **evolução genômica** como:

* Mutação aleatória
* Crossover genético
* Seleção por torneio

Ele **testa bilhões de combinações binárias** até gerar uma chave privada válida cujo endereço público corresponde a um dos definidos na lista `DATA_ADDRESS`.

---

## 🛠️ Requisitos

* Python 3.8+
* Bibliotecas:

  * `bit`
  * `deap`
  * `multiprocessing`
  * `re`
  * `logging`

Instale os requisitos com:

```bash
pip install bit deap
```

---

## 🧪 Como funciona

O algoritmo segue os passos abaixo:

1. 📥 **Solicita o número de bits** para gerar as chaves (entre 1 e 256).
2. 🧬 Cria uma **população inicial** com sequências binárias aleatórias.
3. 🔁 Executa gerações evolutivas aplicando:

   * **Crossover** (recombinação genética)
   * **Mutação**
   * **Avaliação de fitness**
4. 🧠 Avalia se a chave gerada produz um endereço presente na lista `DATA_ADDRESS`.
5. 💾 Se encontrar uma correspondência, **salva o WIF e o endereço** em `carteiras.txt`.

---

## 📸 Exemplo de execução

```bash
$ python btc_cracker.py
Informe o valor de TARGET_SEQUENCE_LENGTH (1 a 256): 128
TARGET_SEQUENCE_LENGTH definido como 128
Iniciando AG com 128 bits | Crossover: 0.7000
[✔] Geração 237: WIF=KxyZ... Endereço=1Ab4... Tempo=53.29s
```

---

## 📁 Estrutura de Arquivos

```
btc-genetic-cracker/
│
├── btc_cracker.py        # Script principal
├── carteiras.txt         # Arquivo onde são salvos os WIFs e endereços encontrados
└── README.md             # Este arquivo explicativo
```

---

## ⚙️ Ajustes automáticos

🔧 O script **ajusta automaticamente os parâmetros** do algoritmo (como tamanho da população, taxa de mutação, etc) com base no número de bits definido.

---

## ⚠️ Aviso Legal

> ⚖️ **Este projeto é para fins educacionais e de pesquisa.**
>
> ❌ **Não é recomendado para uso com intenções maliciosas.**
>
> 🧠 Utilize com ética e responsabilidade.

---

## 🧠 Conhecimento aplicado

Este projeto demonstra uso de:

* Algoritmos Genéticos (GA)
* Multiprocessamento em Python
* Geração de chaves e endereços Bitcoin
* Regex para extração de WIFs e endereços
* Registro de logs e controle de estado

---

## 📬 Contato

Feito por [CanalQb no GitHub](https://github.com/canalqb)
📘 Visite o blog: [canalqb.blogspot.com](https://canalqb.blogspot.com/)
💸 Apoie o projeto via Bitcoin:
`13Ve1k5ivByaCQ5yer6GoV84wAtf3kNava`

---

📌 Sinta-se à vontade para clonar, modificar e experimentar.
⭐ Se achou útil, deixe uma estrela no repositório!
