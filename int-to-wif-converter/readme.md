# 🔐 Conversor de Inteiros para Chave Privada WIF

> Script simples para converter números inteiros em **chaves privadas Bitcoin** no formato **WIF (Wallet Import Format)**, com suporte para chaves comprimidas e diferentes redes (mainnet/testnet).

---

## ✨ O que este projeto faz?

Este pequeno utilitário em Python permite que você converta um **inteiro arbitrário** em uma **chave privada Bitcoin** válida, codificada em WIF.

Isso é especialmente útil para:

* **Testes e experimentos** com chaves Bitcoin
* Geração de chaves a partir de números definidos
* Entender o formato WIF e o processo de codificação Bitcoin

---

## ⚙️ Como funciona o script?

### Passo a passo:

1. **Conversão do inteiro em bytes**
   O número é convertido para uma sequência de 32 bytes no formato big endian.

2. **Prefixo da rede**
   Um byte é adicionado no início para indicar se a chave é para mainnet (`0x80`) ou testnet (`0xEF`).

3. **Sufixo de compressão (opcional)**
   Se a chave for comprimida, adiciona-se o byte `0x01` no final.

4. **Checksum de segurança**
   Aplica-se dupla SHA-256 para criar um checksum de 4 bytes, que ajuda a detectar erros na chave.

5. **Codificação Base58**
   Finalmente, concatena-se tudo e codifica na base58, produzindo a chave WIF legível.

---

## 🚀 Como usar?

Basta executar o script passando o inteiro desejado para a função `int_to_wif()`:

```python
wif_key = int_to_wif(83)
print(wif_key)
```

O exemplo acima gera a chave privada WIF correspondente ao número 83.

---

## 📝 Personalização

* **Chave comprimida ou não:** altere o parâmetro `compressed` (padrão: `True`).
* **Rede principal ou testnet:** altere o parâmetro `mainnet` (padrão: `True`).

---

## 💡 Por que usar este script?

* Para **estudar o formato WIF** e como chaves Bitcoin são representadas.
* Facilita a **conversão direta de inteiros** em chaves, útil em ambientes educacionais e experimentais.
* Pode ser integrado em projetos que lidam com **geração customizada de chaves**.

---

## 📬 Contato

Feito por [CanalQb no GitHub](https://github.com/canalqb)
Visite o blog: [canalqb.blogspot.com](https://canalqb.blogspot.com/)
💸 Apoie o projeto via Bitcoin: `13Ve1k5ivByaCQ5yer6GoV84wAtf3kNava`
