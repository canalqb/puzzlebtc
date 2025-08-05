# 🔐 BTC Mask Scan

**BTC Mask Scan** é uma ferramenta avançada que realiza varreduras matemáticas utilizando *máscaras binárias* com múltiplos bits ativados. O objetivo é gerar chaves privadas válidas, derivar os respectivos **endereços Bitcoin**, e verificar se algum deles já consta em um **banco de dados local SQLite**.

O processo é altamente otimizado para utilizar **combinações específicas de bits ativados**, o que permite investigar regiões específicas da curva SECP256k1 com base em padrões binários.

---

## 🚀 Funcionalidades

* 🔢 Geração de chaves privadas baseadas em **máscaras com N bits ligados**
* 🧠 Criação inteligente de combinações a partir de **potências de 2**
* 🏁 Verificação de cada endereço gerado contra um banco SQLite local
* 🧾 Salva resultados em arquivo se encontrar uma chave correspondente
* ⚙️ Processamento com **prioridade baixa** para evitar travamentos no sistema

---

## 🧠 Como funciona?

1. Gera combinações binárias com **N bits ligados** (ex: 20 bits ativados entre os 160 possíveis).
2. Cada combinação é somada, formando um número a ser testado como **chave privada**.
3. A chave é convertida para o formato **WIF** e usada para derivar o **endereço Bitcoin**.
4. O endereço é consultado em um **banco de dados local SQLite**.
5. Se o endereço estiver presente, a chave é salva em `chave_encontrada.txt` e o script é finalizado imediatamente.

---

## 🛠️ Pré-requisitos

* Python 3.8+
* Pacotes Python:

  * `bit`
  * `psutil`
* Banco de dados SQLite com tabela `enderecos(address TEXT)`

---

## 📦 Instalação

```bash
git clone https://github.com/canalqb/btc-mask-scan.git
cd btc-mask-scan
pip install bit psutil
```

---

## ⚙️ Configuração

Edite o caminho do banco de dados no início do script:

```python
CAMINHO_BANCO = "D:/Rodrigo/20052025/blockchair/banco.db"
```

Você também pode ajustar a profundidade de busca com:

```python
max_bits_ligados = 20  # Pode reduzir para economizar RAM
```

> ⚠️ *Quanto mais bits ligados, mais combinações e mais memória serão necessárias.*

---

## ▶️ Como executar

```bash
python gerador_mascaras_verificador.py
```

O script exibirá os endereços verificados em tempo real, e ao encontrar uma correspondência, salvará:

📄 `chave_encontrada.txt`
Com o conteúdo:

```
WIF: Lxxx...xxx - End: 1ABC...123
```

---

## 📁 Exemplo de saída no terminal

```
🔗 Conectando ao banco de dados...
✅ Geradas 1048575 máscaras com 20 bits ligados.
📄 Consultando endereços no banco...
🔍 29228701 - 1Fabc123xyz - não encontrado.
🔍 29876344 - 1Lmnop456abc - não encontrado.
...
🔒 Chave encontrada!
WIF: L4mxxx....xx
Endereço: 1Qz...abc
```

---

## ⚠️ Aviso legal

> Este projeto é para **uso educacional e de pesquisa criptográfica**.
>
> Tentar encontrar chaves privadas de carteiras reais é **computacionalmente inviável** e pode ser **ilegal**, dependendo da jurisdição.
> **Use por sua conta e risco.**

---

## 📬 Contato

Feito por [CanalQb no GitHub](https://github.com/canalqb)
📝 Visite o blog: [canalqb.blogspot.com](https://canalqb.blogspot.com/)
💸 Apoie o projeto via Bitcoin:

```
13Ve1k5ivByaCQ5yer6GoV84wAtf3kNava
```

---

## 🧾 Licença

Licenciado sob a **MIT License**.
Você pode usar, estudar, modificar e redistribuir livremente.
