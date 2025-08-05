# 🧬 Genetic BTC Address Finder

> ⚠️ **Uso avançado — este projeto realiza varredura genética por endereços Bitcoin com base em dados locais.**
> Ideal para fins de *pesquisa*, *segurança*, ou *educação sobre vulnerabilidades e geração de chaves*.

---

### 🎯 Objetivo

Este script utiliza **algoritmos genéticos** para tentar encontrar chaves privadas que correspondam a endereços Bitcoin existentes em um banco de dados local. Embora extremamente improvável de encontrar algo útil, este processo é interessante do ponto de vista educacional e de segurança cibernética.

---

### ⚙️ Como Funciona

1. O script carrega um banco de dados SQLite com endereços Bitcoin.
2. Para cada tamanho de endereço (de 2 a 256 bits), ele:

   * Seleciona um endereço aleatório com aquele tamanho.
   * Usa um algoritmo genético para tentar **gerar uma chave privada** que resulte em um endereço semelhante.
   * Avalia candidatos com base na similaridade com o endereço alvo.
   * Tenta mutações e cruzamentos para evoluir indivíduos.
   * Se encontrar um endereço presente no banco, salva em `enderecos_encontrados.txt`.

---

### 🧠 Tecnologias Utilizadas

* 🧬 **DEAP**: Biblioteca de algoritmos evolutivos
* 🪙 **bit**: Biblioteca para manipulação de chaves Bitcoin
* 🧠 **multiprocessing**: Aceleração com múltiplos núcleos
* 🗃️ **SQLite3**: Banco de dados local
* ⚙️ **psutil**: Gerenciamento de prioridade de processos (Windows)

---

### 🚀 Passo a Passo para Executar

> 💡 Recomendado apenas para usuários avançados com conhecimento em Python e blockchain.

#### 1. **Pré-requisitos**

* Python 3.8+
* Instale as dependências:

  ```bash
  pip install deap bit psutil
  ```

#### 2. **Configure o banco de dados**

* Coloque seu arquivo `banco.db` no caminho definido na variável `DB_PATH` do script:

  ```python
  DB_PATH = r"D:\Rodrigo\20052025\blockchair\banco.db"
  ```
* A tabela esperada é `enderecos`, com a coluna `address`.

#### 3. **Execute o script**

```bash
python btc_genetic_finder.py
```

#### 4. **Resultados**

* Resultados positivos são salvos em:

  ```
  enderecos_encontrados.txt
  ```

---

### 🔬 Exemplo de Saída

```
== Iniciado TARGET_LEN=33 – Target: 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa
WIF: 5HueCGU8rMjxEXxiPuD5BDu... | Address: 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa
>>> Endereço 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa encontrado em gen 36!
```

---

### 🔐 Segurança e Ética

* **⚠️ Este script é educacional. Não deve ser usado para atividades maliciosas.**
* A chance de encontrar uma chave válida é praticamente **nula**, devido ao tamanho do espaço de chaves (2^256).
* Usado para demonstrar o quão seguro é o Bitcoin quando boas práticas são seguidas.

---

### 🧩 Curiosidades Técnicas

* Geração de indivíduos binários de tamanho variável (até 256 bits)
* Cada indivíduo é convertido em um número inteiro -> chave privada
* Avaliação com diferentes formatos de endereço:

  * `P2PKH`
  * `P2SH`
  * `Bech32`
* Otimização com múltiplos processos e prioridade baixa para rodar em segundo plano

---

## 📬 Contato

Feito por [CanalQb no GitHub](https://github.com/canalqb)
Visite o blog: [canalqb.blogspot.com](https://canalqb.blogspot.com/)
💸 Apoie o projeto via Bitcoin:
`13Ve1k5ivByaCQ5yer6GoV84wAtf3kNava`
