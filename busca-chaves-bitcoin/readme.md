# 🔐 Scanner de Chaves Bitcoin em Banco de Dados

Este projeto realiza uma **busca inteligente e automatizada por chaves privadas válidas** no banco de dados de endereços Bitcoin. Ele utiliza **combinações binárias otimizadas** para gerar e verificar possíveis chaves privadas, comparando-as com um banco SQLite de endereços conhecidos.

> ⚠️ Este script **não é uma ferramenta de cracking ou invasão**, mas sim um experimento técnico voltado para estudo de como funciona a geração e validação de chaves no protocolo Bitcoin.

---

## 🚀 Funcionalidades

* ✅ Geração de chaves privadas baseadas em somas específicas de potências de 2.
* 🔍 Verificação de endereços derivados contra um banco SQLite local.
* 🧠 Otimização com execução em **prioridade baixa** para não sobrecarregar o sistema.
* 💾 Log automático das chaves encontradas com endereço correspondente.
* 🔒 Geração compatível com o formato **WIF (Wallet Import Format)**.

---

## 🛠️ Como funciona?

O script utiliza a biblioteca [`bit`](https://ofek.dev/bit/) para gerar chaves privadas e endereços, fazendo combinações de somas de potências de 2 que **não ultrapassam o limite do SECP256k1**, a curva elíptica usada pelo Bitcoin.

Cada endereço gerado é comparado com o banco de dados SQLite informado. Se encontrar uma correspondência, grava a chave e endereço em um arquivo `chave_encontrada.txt`.

---

## 📂 Requisitos

Antes de rodar, instale os requisitos:

```bash
pip install bit psutil
```

---

## ⚙️ Configuração

1. **Configure o caminho do banco de dados** alterando a variável `CAMINHO_BANCO` no script:

   ```python
   CAMINHO_BANCO = "D:/Rodrigo/20052025/blockchair/banco.db"
   ```
2. Certifique-se de que seu banco tenha uma tabela chamada `enderecos` com uma coluna `address`.

---

## 🧪 Execução

Basta rodar o script normalmente:

```bash
python scanner_chaves.py
```

O processo testará diversas combinações e, caso encontre uma chave com endereço presente no banco, salvará em:

```plaintext
chave_encontrada.txt
```

---

## 📌 Exemplo de saída

```
🧪 L1aW4aubDFB7yfras2S1mME5Q3Uixf8Ktz2Y | 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa | ID: 70 | Total: 123456789
✅ Chave encontrada!
WIF: L1aW4aubDFB7yfras2S1mME5Q3Uixf8Ktz2Y
Endereço: 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa
```

---

## ⚠️ Avisos

* ⛔ O script não **força bruta** o Bitcoin. Ele apenas testa combinações específicas.
* 🧪 Uso recomendado **apenas para fins educacionais** e experimentação com curvas elípticas.

---

## 📬 Contato

Feito por [CanalQb no GitHub](https://github.com/canalqb)
Visite o blog: [canalqb.blogspot.com](https://canalqb.blogspot.com/)
💸 Apoie o projeto via Bitcoin: `13Ve1k5ivByaCQ5yer6GoV84wAtf3kNava`

---

## 🧠 Licença

Este projeto é de código aberto e está licenciado sob a **MIT License**. Sinta-se livre para estudar, modificar e compartilhar.
