# 🧠 Gerador de Endereços Bitcoin com Chave Privada Personalizada

Este script Python gera diferentes **endereços Bitcoin** (Legacy, SegWit compatível e Native SegWit) a partir de uma **chave privada decimal customizada**. Ele também exibe os formatos **WIF comprimido e não comprimido**.

> ✅ Ideal para desenvolvedores, entusiastas de criptografia, testes, estudos ou qualquer pessoa que deseje entender melhor como funcionam os formatos de endereço Bitcoin.

---

## 🚀 O que o script faz?

A partir de **uma chave privada em formato decimal**, ele gera automaticamente:

* 🔐 Chave privada em **hex**
* 🔐 Chave privada em **WIF (Wallet Import Format)** (comprimida e não comprimida)
* 🏷️ Endereço **Legacy (P2PKH)** — comprimido e não comprimido
* 🏷️ Endereço **SegWit compatível (P2WPKH-in-P2SH)** — ideal para carteiras que não suportam Native SegWit
* 🏷️ Endereço **Native SegWit (Bech32/P2WPKH)** — menor taxa de transação, prefixo `bc1...`

---

## 📦 Requisitos

Certifique-se de ter o Python 3 instalado com as seguintes bibliotecas:

```bash
pip install ecdsa bit
```

---

## ⚙️ Como usar?

1. Clone o repositório ou baixe o arquivo:

   ```bash
   git clone https://github.com/seuusuario/bitcoin-address-generator
   cd bitcoin-address-generator
   ```

2. Edite a variável `privkey_int` no arquivo `generate_bitcoin_addresses.py` com o valor decimal desejado da chave privada:

   ```python
   privkey_int = 13407807929942597099...  # sua chave privada decimal aqui
   ```

3. Execute o script:

   ```bash
   python generate_bitcoin_addresses.py
   ```

4. O terminal exibirá:

   * Chave privada em HEX
   * WIF (comprimido e não comprimido)
   * Endereços Legacy, SegWit compatível e Native SegWit

---

## 🧪 Exemplo de saída

```
🔐 Private key hex: 1e99423a4ed27608a15a2616...
🔐 WIF Compressed:     L5BmPijJjrKbiUfG4zbiFKN...
🔐 WIF Uncompressed:   5HueCGU8rMjxEXxiPuD5BD...

🏷️ Legacy (compressed):      1PMycacnJaSqwwJqjawXBErnLsZ7RkXUAs
🏷️ Legacy (uncompressed):    1BgGZ9tcN4rm9KBzDn7KprQz87SZ26SAMH
🏷️ P2WPKH-in-P2SH (compat):  3Ai1JZ8pdJb2ksieUV8FsxSNVJCpoPi8W6
🏷️ Native SegWit (P2WPKH):   bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kygt080
```

---

## 🛠️ O que está acontecendo por trás?

* 🔄 A chave privada decimal é convertida em 32 bytes (`big endian`)
* 🔁 A chave pública é derivada usando a curva SECP256k1 (ECDSA)
* 🔐 A chave é formatada em WIF para uso em carteiras
* 🧮 Hashes (SHA256, RIPEMD160) são usados para gerar os endereços conforme o padrão:

  * **P2PKH** (Legacy)
  * **P2SH-P2WPKH** (Compatível SegWit)
  * **Bech32/P2WPKH** (Native SegWit)

---

## 📬 Contato

Feito por [CanalQb no GitHub](https://github.com/canalqb)
Visite o blog: [canalqb.blogspot.com](https://canalqb.blogspot.com/)
💸 Apoie o projeto via Bitcoin:
`13Ve1k5ivByaCQ5yer6GoV84wAtf3kNava`

---

## 📄 Licença

Este projeto é de código aberto e livre para uso pessoal e educacional.
Licença: **MIT**
