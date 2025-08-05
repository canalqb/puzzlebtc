

# Bitcoin WIF Key Generator 🔑

Este projeto contém um **script em Python** que gera chaves privadas aleatórias na faixa de valores entre $2^{71}$ e $2^{72} - 1$, e as converte para o formato **WIF comprimido** (Wallet Import Format), amplamente utilizado para importar/exportar chaves privadas em carteiras Bitcoin.

---

## 🚀 Para que serve este script?

* **Gerar chaves privadas Bitcoin aleatórias** dentro de um intervalo muito grande, adequado para testes ou estudos;
* **Converter essas chaves para o formato WIF comprimido**, que é uma representação codificada e segura da chave privada, pronta para ser usada em softwares de carteira Bitcoin que suportem chaves comprimidas;
* Demonstrar os passos fundamentais da conversão:

  * conversão para bytes com tamanho fixo de 32 bytes,
  * prefixo de rede e sufixo para indicar chave comprimida,
  * cálculo do checksum duplo SHA-256,
  * codificação em Base58 para gerar a string final.

---

## 🔍 Como o script funciona?

1. Define o intervalo de geração de chaves privadas entre $2^{71}$ e $2^{72} - 1$.
2. Para cada chave privada aleatória gerada:

   * Converte o inteiro para uma sequência de 32 bytes.
   * Aplica o prefixo `0x80` (indica que é uma chave privada para Bitcoin mainnet).
   * Adiciona o byte `0x01` ao final para indicar que a chave é **comprimida**.
   * Calcula o checksum usando duas vezes o hash SHA-256.
   * Codifica tudo em Base58, o que resulta na chave privada no formato WIF comprimido.
3. Imprime as chaves geradas no formato legível, exibindo o número inteiro da chave e sua versão WIF.

---

## 📋 Passo a passo para usar o script

* **Passo 1:** Clone este repositório ou baixe os arquivos.

* **Passo 2:** Navegue até a pasta `bitcoin-wif-generator`.

* **Passo 3:** Execute o script com Python 3:

  ```bash
  python generate_wif_keys.py
  ```

* **Passo 4:** Veja as chaves privadas geradas no terminal, cada uma exibida no formato inteiro e WIF comprimido.

---

## ⚠️ Atenção

* **NUNCA** utilize as chaves geradas aqui para guardar valores reais em Bitcoin! Este script é destinado apenas para fins educacionais e testes.
* O intervalo gerado é grande, mas não cobre todo o espaço possível de chaves privadas Bitcoin (que é muito maior).
* A segurança e o uso correto de chaves privadas são essenciais para proteção dos seus fundos.

---

## 💡 Benefícios deste projeto

* Compreender na prática o processo de geração e codificação de chaves privadas Bitcoin.
* Base para estudar formatos de chaves e criptografia envolvida em Bitcoin.
* Gerar várias chaves em batch para simulações e testes.

---

## 📬 Contato

Feito por [CanalQb no GitHub](https://github.com/canalqb)
Visite o blog: [canalqb.blogspot.com](https://canalqb.blogspot.com/)
💸 Apoie o projeto via Bitcoin: `13Ve1k5ivByaCQ5yer6GoV84wAtf3kNava`

---
