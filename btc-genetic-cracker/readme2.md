# 🔑 Bitcoin Genetic Cracker - genetic_bitcoin_cracker.py

🚀 **Descubra chaves privadas Bitcoin usando Algoritmos Genéticos e Banco de Dados local**

---

### 📋 Sobre o Script

Este script utiliza **algoritmos genéticos** para tentar encontrar chaves privadas Bitcoin a partir de um banco de dados local contendo endereços conhecidos. Ele emprega técnicas avançadas de **evolução computacional** para gerar, cruzar e mutacionar populações de bits que representam potenciais chaves privadas, buscando encontrar alguma correspondência com endereços existentes.

---

### ⚙️ Como Funciona?

1. **Inicialização**
   O script conecta a um banco de dados SQLite (`banco.db`) que armazena endereços Bitcoin.

2. **Geração da População Inicial**
   Cria uma população aleatória de indivíduos (representados como sequências de bits).

3. **Avaliação de Fitness**
   Cada indivíduo é convertido em uma chave privada, a partir da qual múltiplos formatos de endereço são gerados (P2PKH, Segwit, Bech32). A função de fitness verifica se algum desses endereços existe no banco.

4. **Seleção e Reprodução**
   Indivíduos com maior fitness têm maior chance de serem selecionados para cruzamento (crossover) e mutação, gerando a próxima geração.

5. **Iteração**
   O processo é repetido por até 140 gerações, melhorando continuamente a população.

6. **Resultado**
   Se algum endereço correspondente for encontrado no banco, ele é registrado em `enderecos_encontrados.txt`.

---

### 🎯 Objetivo

* **Explorar o espaço de chaves privadas possíveis usando métodos genéticos.**
* **Encontrar correspondências com endereços Bitcoin reais, possibilitando análise e estudo de segurança.**
* **Rodar em múltiplos núcleos com paralelismo para maior performance.**

---

### 📌 Requisitos

* Python 3.x
* Bibliotecas Python:

  * `deap` (algoritmos genéticos)
  * `bit` (manipulação de chaves Bitcoin)
  * `psutil` (ajuste de prioridade do processo)
* Banco de dados SQLite (`banco.db`) contendo tabela `enderecos` com coluna `address`

---

### 🚀 Como Usar

1. Clone o repositório:

   ```bash
   git clone https://github.com/canalqb/btc-genetic-cracker.git
   cd btc-genetic-cracker
   ```

2. Instale as dependências:

   ```bash
   pip install deap bit psutil
   ```

3. Ajuste o caminho do banco (`DB_PATH`) no script para seu arquivo local.

4. Execute o script:

   ```bash
   python genetic_bitcoin_cracker.py
   ```

5. Acompanhe a saída para ver potenciais chaves/endereço encontrados.

---

### 📂 Estrutura

```
btc-genetic-cracker/
├── genetic_bitcoin_cracker.py  # Script principal
├── banco.db                    # Banco SQLite (externo)
├── enderecos_encontrados.txt   # Resultados gravados
└── README.md                   # Este arquivo
```

---

### ⚠️ Avisos importantes

* **Uso Ético:** Este projeto é para fins educacionais e de pesquisa.
* **Não utilize para atividades ilegais ou não autorizadas.**
* **A geração e teste de chaves privadas envolve processamento intenso e pode consumir muitos recursos computacionais.**

---

### 📬 Contato

Feito por [CanalQb no GitHub](https://github.com/canalqb)
Visite o blog: [canalqb.blogspot.com](https://canalqb.blogspot.com/)
💸 Apoie o projeto via Bitcoin: `13Ve1k5ivByaCQ5yer6GoV84wAtf3kNava`
