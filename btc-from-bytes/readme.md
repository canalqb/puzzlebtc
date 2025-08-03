# 🧠 Bitcoin Key Generator from Byte Arrays

Este projeto implementa a geração de chaves privadas e endereços Bitcoin a partir de vetores de bytes, normalmente extraídos de endereços existentes. O objetivo principal é transformar esses dados em **chaves privadas (WIF)** e endereços nos formatos **P2PKH**, **P2SH** e **Bech32**.

> ⚠️ Este projeto é experimental e **não deve ser usado com fundos reais de Bitcoin**. As chaves públicas geradas neste código não usam a curva elíptica real `secp256k1`, portanto os endereços e chaves resultantes são inválidos para uso em redes reais.

---

## 📦 Funcionalidades

- Decodifica endereços base58 e gera vetores de bytes.
- Normaliza esses vetores para o tamanho apropriado (32 bytes).
- Converte os vetores em chaves privadas comprimidas.
- Gera a chave pública (em formato comprimido – simplificado).
- Gera:
  - Endereço P2PKH (prefixo 0x00)
  - Endereço P2SH (prefixo 0x05, via script P2WPKH)
  - Endereço Bech32 (SegWit)
- Gera o **WIF (Wallet Import Format)** comprimido.

---

## 🧪 Exemplo de Saída

L1aW4aubDFB7yfras2S1mMEG36iDW2f7qcJjbaLrciVrZbY6zZKj - 1PMycacnJaSqwwJqjawXBErnLsZ7RkXUAs - bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kygt080


---

## ⚙️ Como funciona

### 🔐 WIF (Wallet Import Format)

WIF é uma forma de codificar chaves privadas Bitcoin para facilitar a importação em carteiras.

**Formato do WIF comprimido:**

1. Prefixo `0x80` (Bitcoin mainnet)
2. 32 bytes da chave privada
3. Sufixo `0x01` (indica chave pública comprimida)
4. Checksum (primeiros 4 bytes do SHA256(SHA256(...)))
5. Codificação Base58Check

### 📥 Entrada

Um vetor de bytes derivado da decodificação base58 de um endereço existente.

### 📤 Saída

- Chave privada comprimida (WIF)
- Endereços:
  - **P2PKH** (`1...`)
  - **P2SH (P2WPKH-in-P2SH)** (`3...`)
  - **Bech32** (`bc1...`)

---

## 📊 Entropia

O código também calcula a **entropia da distribuição dos bytes**, o que pode ser útil para analisar a aleatoriedade ou qualidade do vetor convertido.

---

## ⚠️ Limitações

- A função `private_key_to_public_key(...)` **não utiliza a curva elíptica `secp256k1` real** para geração da chave pública. Isso significa que:
  - Os endereços gerados não são válidos para transações reais.
  - A chave pública é apenas uma hash simplificada da chave privada (via SHA256).
- **Nunca use isso para armazenar ou movimentar bitcoins reais.**
- Este projeto é apenas para estudo, testes ou simulações offline.

---

## 🚀 Sugestões de melhoria

Se quiser transformar este projeto em algo funcional:

- Use a biblioteca [`ecdsa`](https://pypi.org/project/ecdsa/) ou [`secp256k1`](https://pypi.org/project/secp256k1/) para gerar a chave pública real via curva elíptica.
- Valide os endereços com carteiras reais para testes em testnet.

---

## 📄 Licença

Este projeto é distribuído como **open source apenas para fins educacionais**. Nenhuma garantia é fornecida sobre segurança, funcionalidade ou integridade dos dados gerados.

---

🚀 Como usar
Clone o repositório:
 
git clone https://github.com/seu-usuario/byte2btc.git
cd byte2btc
Instale com pip:
 
pip install .
Execute:
 
python byte2btc/byte_to_btc.py
Testes:
 
pytest
