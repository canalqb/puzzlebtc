
# 🔢 Convert Int Representations

```markdown

Este repositório contém um script Python poderoso que converte inteiros em diversas representações binárias, textuais, criptográficas e numéricas. Ele é ideal para testes de codificação, estudos de representação de dados e análise de transformações digitais.
```
## ✨ O que o script faz?

Dado um intervalo de inteiros (até números extremamente grandes — 256 bits ou mais), o script gera **diversas formas de representação** desses inteiros. Isso inclui:

- Representações em bases variadas (binária, hexadecimal, base64, base58, base62, etc.)
- Representações codificadas (BCD, Elias Gamma, Fibonacci, VLQ, etc.)
- Vetores binários e bitmaps
- Representações criptográficas (SHA-1, SHA-256, SHA-512, MD5, Blake2b, Blake3, PBKDF2, UUIDv5)
- Representações para uso com instruções SIMD (como __m256, __m256d, __m256i)
- Chaves para criptografia (AES-256 Key, IV)
- Vetores de multiplicação, vetores densamente empacotados, entre outros

### Exemplos de conversores disponíveis:

- 🔡 `UTF-8`, `ASCII padded`, `Base64`, `Base32`, `Base16`
- 🔐 `SHA-256`, `PBKDF2`, `UUIDv5`, `CRC32`, `AES`
- 🧮 `BCD`, `VLQ`, `Gray Code`, `Elias Gamma`, `Fibonacci Encoding`
- 🔢 `Binário`, `Hexadecimal`, `Base 3` até `Base 62`

## 📦 Estrutura do código

- Cada número é processado por dezenas de conversores.
- O script pode operar sobre ranges de inteiros definidos no array `intervalos`.
- É fácil adicionar novos conversores, seguindo o modelo do dicionário `converters`.

## 📁 Organização

```

bit\_transformations/
│
├── convert\_int\_representations.py  # Script principal com todas as funções
├── README.md                       # Este arquivo

````

## 🔧 Requisitos

- Python 3.7+
- Bibliotecas:
  - `numpy`
  - `pandas`
  - `blake3`

Instale com:

```bash
pip install numpy pandas blake3
````

## 📌 Uso

No terminal:

```bash
python convert_int_representations.py
```

O script irá processar os valores definidos em `intervalos` e aplicar as transformações.

## 📚 Aplicações

* Ensino de estruturas de dados e algoritmos
* Geração de dados de teste para sistemas de criptografia
* Análise de entropia e compressibilidade
* Representações alternativas para identificação e hashing

## 📜 Licença

Este projeto está licenciado sob a Licença MIT. 

## 📬 Contato

Feito por [CanalQb ou GitHub](https://github.com/canalqb)

Visite o Blog [Canalqb](https://canalqb.blogspot.com/)
