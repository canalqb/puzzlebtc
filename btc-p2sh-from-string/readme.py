# 🔐 Bitcoin P2SH Address Generator from String

Este script **gera um endereço Bitcoin P2SH** válido a partir de uma *string arbitrária*, criando também a chave privada correspondente e sua WIF (Wallet Import Format).

---

## ✨ O que ele faz?

* Deriva **deterministicamente uma chave privada** a partir da string informada.
* Gera a **WIF** (formato amigável para carteiras) dessa chave privada.
* Cria o **redeem script P2PKH** (pay-to-public-key-hash) para o endereço.
* Calcula o **endereço P2SH** válido e compatível com a rede Bitcoin mainnet.
* Assim, o endereço gerado está *relacionado* à chave privada derivada da string — ou seja, você pode gastar bitcoins enviados para ele.

---

## 🚀 Como usar

1. Clone este repositório ou baixe o arquivo `generate_p2sh_from_string.py` dentro da pasta `btc-p2sh-from-string`.

2. Instale a biblioteca `ecdsa` se ainda não tiver:

   ```
   pip install ecdsa
   ```

3. Execute o script no terminal/cmd:

   ```
   python generate_p2sh_from_string.py
   ```

4. Digite a string desejada para gerar a chave e o endereço.

---

## 📋 Passo a passo interno

1. **Entrada**: Você digita uma string, ex: `"canalqb"`.
2. **Chave privada**: O script usa SHA256 da string para gerar uma chave privada de 32 bytes.
3. **WIF**: Gera o formato WIF da chave privada, facilitando importação em carteiras.
4. **Chave pública comprimida**: A partir da chave privada, calcula a chave pública comprimida (33 bytes).
5. **Redeem Script**: Monta o script P2PKH que será embutido no P2SH.
6. **Endereço P2SH**: Gera o endereço P2SH baseado no hash do redeem script.

---

## 🎯 Resultado esperado

Exemplo para a string `"canalqb"`:

```
Para a string 'canalqb':
Chave privada (hex): 1f75d87c0d4cc31f35d31624565f7f6a2c7c207bd6d2ef304e36324ffd641e76
WIF: KxGsALRQF7eBzaFyVEPZd8fWYsrC1i7HjutHGth9V7WQLRhVe934
Endereço P2SH válido: 3BYaJhnZeyAjzeS3B5NBoktzKWw1gLomAG
```

---

## ⚠️ Avisos importantes

* **O endereço P2SH gerado pode receber bitcoins, e você pode gastar esses bitcoins usando a chave privada gerada**.
* A geração da chave é **determinística**: mesma string = mesma chave + endereço.
* Este script é para fins educativos e deve ser usado com cuidado em ambientes seguros.

---

## 📬 Contato

Feito por [CanalQb no GitHub](https://github.com/canalqb)
Visite o blog: [canalqb.blogspot.com](https://canalqb.blogspot.com/)
💸 Apoie o projeto via Bitcoin: `13Ve1k5ivByaCQ5yer6GoV84wAtf3kNava`
