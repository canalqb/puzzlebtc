---

# 🔍 Bitcoin Address Matcher via Multiplicative Interval Search

Este projeto realiza buscas por **endereços Bitcoin gerados a partir de chaves privadas específicas**, multiplicando blocos de valores base por múltiplos definidos pelo usuário. O objetivo é tentar encontrar correspondências com **endereços conhecidos**, previamente definidos em uma lista.

---

## 🚀 Objetivo

O script permite verificar se determinados **endereços Bitcoin** (Legacy, P2SH ou Bech32) podem ser gerados a partir de **chaves privadas derivadas de valores inteiros multiplicados por constantes específicas**.

Ele é especialmente útil para:

* Pesquisadores em segurança de criptografia.
* Estudos sobre padrões ou fraquezas em geração de chaves.
* Auditorias de endereços comprometidos ou suspeitos.

---

## ⚙️ Como funciona

1. O usuário informa:

   * Intervalo de **multiplicadores decimais**.
   * Passo entre os multiplicadores.
   * Intervalo de expoentes `n`, onde são analisados valores entre `2^n` e `2^(n+1) - 1`.

2. Para cada bloco dentro do intervalo:

   * O valor base é multiplicado por cada multiplicador e ajustado por `*256`.
   * São gerados endereços Bitcoin (Legacy, P2SH, Bech32).
   * Esses endereços são comparados com uma **lista fixa de endereços conhecidos**.

3. Se um endereço gerado coincidir com a lista:

   * A chave WIF e o endereço correspondente são salvos no arquivo `valoresdeaddres.txt`.

---

## 🧠 Conceitos envolvidos

* Chave privada SECP256K1 derivada de um inteiro.
* Conversão para formatos de endereço Bitcoin:

  * Legacy (Base58Check).
  * P2SH (SegWit compatível).
  * Bech32 (nativo SegWit).
* Comparação de endereços gerados com lista de alvos.

---

## 💻 Como usar

1. Clone o repositório:

   ```
   git clone https://github.com/seuusuario/btc-address-matcher.git
   cd btc-address-matcher
   ```

2. Instale as dependências:

   ```
   pip install bit psutil
   ```

3. Execute o script:

   ```
   python scan_by_multiplier.py
   ```

4. Preencha os dados solicitados no terminal:

   * Menor e maior multiplicador.
   * Passo decimal.
   * ID inicial e final (representando o expoente do intervalo `2^n`).

---

## 📁 Saída gerada

* **valoresdeaddres.txt**
  Arquivo contendo pares de chaves privadas e endereços que **coincidiram com a lista** fornecida.

---

## 🛑 Aviso Legal

Este script é apenas para **fins educacionais e de pesquisa**.
**NÃO use com intenções maliciosas.** A posse ou uso não autorizado de chaves privadas pode ser ilegal em diversas jurisdições.

---

## 📬 Contato

Feito por [CanalQb no GitHub](https://github.com/canalqb)
Visite o blog: [canalqb.blogspot.com](https://canalqb.blogspot.com/)
💸 Apoie o projeto via Bitcoin: `13Ve1k5ivByaCQ5yer6GoV84wAtf3kNava`

