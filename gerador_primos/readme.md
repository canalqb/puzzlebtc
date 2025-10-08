# 🔢 Busca Massiva de Números Primos

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Primes](https://img.shields.io/badge/Números-Primos-orange.svg)](https://pt.wikipedia.org/wiki/Número_primo)

## Objetivo do Projeto

> **Descobrir e catalogar números primos em intervalos massivos** – Este script realiza uma busca sistemática e otimizada de números primos em potências de 2, desde 2³³ até 2²⁵⁶, armazenando todos os resultados em um banco de dados SQLite.

---

## Sumário

- [1. Introdução aos Números Primos](#1-introdução-aos-números-primos)
  - [1.1 O que são Números Primos](#11-o-que-são-números-primos)
  - [1.2 Exemplos Práticos](#12-exemplos-práticos)
  - [1.3 Por que Buscar Primos Grandes](#13-por-que-buscar-primos-grandes)
  - [1.4 Aplicações](#14-aplicações)
  - [1.5 Escala do Projeto](#15-escala-do-projeto)
- [2. Script `busca_primos.py`](#2-script-busca_primospy)
  - [2.1 Objetivo do Script](#21-objetivo-do-script)
  - [2.2 Funcionamento Geral](#22-funcionamento-geral)
  - [2.3 Exemplo de Saída](#23-exemplo-de-saída)
  - [2.4 Funcionamento Interno](#24-funcionamento-interno)
  - [2.5 Tecnologias e Requisitos](#25-tecnologias-e-requisitos)
  - [2.6 Proteções e Recursos](#26-proteções-e-recursos)
  - [2.7 Como Usar](#27-como-usar)
- [3. Extras](#3-extras)
  - [3.1 Requisitos de Hardware](#31-requisitos-de-hardware)
  - [3.2 Licença](#32-licença)
  - [3.3 Referências](#33-referências)
- [4. Contato](#4-contato)
- [5. Nota](#5-nota)

---

## 1. Introdução aos Números Primos

### 1.1 O que são Números Primos

Um **número primo** é um número natural maior que 1 que **só pode ser dividido por 1 e por ele mesmo** sem deixar resto. São os "átomos" da matemática — os blocos fundamentais que compõem todos os outros números através da multiplicação.

**Exemplos de primos pequenos:**
- 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37...

**Não são primos:**
- 4 (divisível por 2)  
- 6 (divisível por 2 e 3)  
- 9 (divisível por 3)  
- 15 (divisível por 3 e 5)

### 1.2 Exemplos Práticos

Imagine que você tem 12 maçãs e quer dividi-las igualmente:
- Pode fazer **2 grupos de 6**
- Ou **3 grupos de 4**
- Ou **4 grupos de 3**
- Ou **6 grupos de 2**

Mas, se você tem **11 maçãs**, não consegue dividi-las igualmente (exceto em 1 grupo de 11 ou 11 grupos de 1). **11 é primo!**

### 1.3 Por que Buscar Primos Grandes

Os números primos grandes têm valor **prático** e **teórico**:

1. 🔐 **Criptografia moderna**  
2. 🔒 **Segurança digital** (HTTPS, certificados, etc.)  
3. 🧠 **Desempenho de algoritmos**  
4. 🔢 **Estudos matemáticos**  
5. 🧪 **Curiosidade científica**

### 1.4 Aplicações

**Aplicações reais dos números primos:**

- 🔐 **Criptografia RSA**: Presente no comércio eletrônico  
- 💳 **Cartões de crédito**: Segurança em transações  
- 📱 **Mensagens criptografadas**: WhatsApp, Telegram  
- 🌐 **Certificados SSL/TLS**: Sites HTTPS  
- 🎲 **Geradores de números aleatórios**: Jogos, simulações  
- 🔬 **Pesquisa científica**: Testes e estudos

### 1.5 Escala do Projeto

Este script trabalha com **números astronômicos**:

| Potência | Valor Aproximado    | Dígitos | Descrição        |
|----------|----------------------|---------|------------------|
| 2³³      | 8,5 bilhões           | 10      | Início da busca  |
| 2⁴⁰      | 1,1 trilhão           | 13      | Ainda gerenciável |
| 2⁵⁰      | 1,1 quatrilhão        | 16      | Grande escala    |
| 2⁶⁰      | 1,15 quintilhão       | 19      | Massivo          |
| 2²⁵⁶     | 1,18 * 10⁷⁷           | 78      | Meta final       |

**Dimensão do desafio:**  
Processar todos os números de 2³³ a 2²⁵⁶ = analisar aproximadamente **1,18 × 10⁷⁷** candidatos a primos!

---

## 2. Script `busca_primos.py`

### 2.1 Objetivo do Script

O script realiza uma **busca sistemática e otimizada** de números primos em intervalos crescentes, salvando cada primo descoberto em um banco de dados SQLite.

**Metas principais:**
- ✅ Descobrir **todos os primos** de 2³³ até 2²⁵⁶  
- ✅ Armazenar resultados em banco de dados persistente  
- ✅ Retomar automaticamente após interrupções  
- ✅ Usar **processamento paralelo**  
- ✅ Garantir confiabilidade em ambientes concorrentes  

### 2.2 Funcionamento Geral

O script opera em **ciclos por potência**:

1. Para cada potência `i` (de 33 até 256):
   - Intervalo: `[2^i, 2^(i+1) - 1]`
   - Divide o intervalo em **chunks** de 10 milhões
   - Testa apenas **ímpares**
   - Elimina múltiplos de primos pequenos
   - Usa o **Teste de Miller-Rabin**
   - Salva em banco de dados SQLite
   - Registra progresso continuamente

2. **Otimizações**:
   - Paralelização por núcleos
   - Escrita periódica
   - Retomada automática
   - Proteção contra concorrência (modo WAL + retries)

### 2.3 Exemplo de Saída

```
============================================================
🔍 BUSCA DE NÚMEROS PRIMOS - Versão com Proteção de Concorrência
✅ Banco de dados inicializado (modo WAL)
📌 Retomando do i=0 (último processado: i=33)
Último primo registrado: 17179868927
🎯 Meta: processar até i=256
💾 Processando em chunks de 10.000.000 números
🔒 Proteção: Retry INFINITO se banco ocupado
============================================

...
✅ i=33 concluído! Total de primos encontrados: 783.964.159
📝 Progresso salvo: i=33, último primo=0359737831

```

### 2.4 Funcionamento Interno

#### 2.4.1 Teste de Primalidade – Miller-Rabin

- ⚡ **Rápido** e probabilístico
- 🎯 **Alta confiabilidade** (>99,9999%)
- 📈 Ideal para grandes números

#### 2.4.2 Processamento Paralelo

- Usa `multiprocessing` com todos os núcleos disponíveis
- Chunks divididos em partes simultâneas
- Resultados combinados e salvos

#### 2.4.3 Gerenciamento de Memória

- Chunking em 10M
- Escrita em lotes de 5.000 primos
- Liberação de memória automática

#### 2.4.4 Sistema de Retomada

- Banco grava `último_i`, `último_primo`
- Retomada direta sem retrabalho

### 2.5 Tecnologias e Requisitos
```
**Requisitos:**

```bash
Python >= 3.8.10
pip install psutil
```

**Bibliotecas utilizadas:**

* `random`: Para Miller-Rabin
* `multiprocessing`: Paralelismo
* `sqlite3`: Banco de dados
* `psutil`: Gerenciamento de processos
* `gc`, `signal`: Limpeza e controle

### 2.6 Proteções e Recursos

#### 2.6.1 Concorrência

* Retry infinito com backoff exponencial
* Modo WAL no SQLite

#### 2.6.2 Interrupção Segura

* Ctrl+C detectado com encerramento limpo
* Progresso salvo com segurança

#### 2.6.3 Tratamento de Erros

* `MemoryError`: Reduz chunk
* `sqlite3.OperationalError`: Retry automático
* Falhas inesperadas: Salva progresso e continua

### 2.7 Como Usar

**Executar:**

```bash
python busca_primos.py
```

**Verificar progresso via Python:**

```python
import sqlite3
conn = sqlite3.connect('primos.db')
cursor = conn.cursor()
```
```python
# Ver progresso
cursor.execute("SELECT * FROM progresso")
print(cursor.fetchone())
```
```python
# Total de primos
cursor.execute("SELECT COUNT(*) FROM `numeros-primos`")
print("Total de primos:", cursor.fetchone()[0])
```
```python
# Top 10
cursor.execute("SELECT primos FROM `numeros-primos` ORDER BY primos DESC LIMIT 10")
for (p,) in cursor.fetchall():
    print(p)

conn.close()
```

**Configurações no início do script:**

```python
MAX_I = 256
CHUNK_SIZE = 10_000_000
BATCH_SAVE_SIZE = 5000
DB_TIMEOUT = 30.0
MAX_RETRIES = 10
LONG_WAIT = 30
```

---

## 3. Extras

### 3.1 Requisitos de Hardware

| Componente    | Mínimo    | Recomendado | Ideal      |
| ------------- | --------- | ----------- | ---------- |
| RAM           | 8 GB      | 16 GB       | 32 GB+     |
| Armazenamento | 100 GB    | 500 GB      | 1 TB+ SSD  |
| Processador   | 2 núcleos | 4 núcleos   | 8+ núcleos |
| Disco         | HDD       | SSD SATA    | NVMe SSD   |

### 3.2 Licença

Este projeto está licenciado sob a **MIT License** – veja o arquivo [LICENSE](LICENSE) para detalhes.

### 3.3 Referências

* [Teste de Primalidade de Miller-Rabin (Wikipedia)](https://pt.wikipedia.org/wiki/Teste_de_primalidade_de_Miller-Rabin)
* [Números Primos (Wikipedia)](https://pt.wikipedia.org/wiki/N%C3%BAmero_primo)
* [SQLite WAL](https://www.sqlite.org/wal.html)
* [Multiprocessing Python](https://docs.python.org/3/library/multiprocessing.html)
* [Criptografia RSA (Wikipedia)](https://pt.wikipedia.org/wiki/RSA)

---

## 4. Contato

- Feito por: **CanalQb**
- Blog: [canalqb.blogspot.com](https://canalqb.blogspot.com)
- 💸 Apoie via Bitcoin: `13Ve1k5ivByaCQ5yer6GoV84wAtf3kNava`
- 📧 PIX: `qrodrigob@gmail.com`

---

## 5. Nota

* **Miller-Rabin**: Algoritmo probabilístico extremamente rápido e confiável para verificar primalidade.
* **Backoff exponencial**: Tempo de espera cresce exponencialmente em tentativas falhas.
* **Chunking**: Técnica de dividir grandes volumes em partes menores.
* **WAL**: Permite acesso concorrente no SQLite.
* **Multiprocessamento**: Acelera usando múltiplos núcleos.
* **SQLite**: Banco de dados leve, prático e robusto.
* **Retry infinito**: Nunca desiste de uma operação crítica.
* **NVMe SSD**: Armazenamento de altíssimo desempenho.
* **Signal handler**: Garante encerramento limpo em interrupções.
