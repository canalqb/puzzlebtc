# 📊 Hex Interval Normalizer & Proportion Calculator

Este projeto tem como objetivo **normalizar valores hexadecimais** dentro de **intervalos de potência de 2**, calculando sua **proporção relativa** com alta precisão e permitindo **comparações reversas**.

Ideal para análises técnicas de **criptografia**, **blockchain**, **compressão**, ou qualquer contexto onde a distribuição e variação proporcional de dados seja relevante.

---

## ✨ O que o script faz?

* 🔢 Converte uma lista de valores hexadecimais para decimais
* 🧮 Para cada índice `i`, calcula o intervalo `[2^i, 2^(i+1)-1]`
* 📐 Determina a **posição proporcional** do valor dentro desse intervalo
* 🔁 Reverte o cálculo para recuperar o valor decimal a partir da proporção
* 🔍 Calcula a **diferença exata** entre o valor original e o reconstruído
* 📄 Exporta tudo em um `.csv` bem organizado

---

## 📁 Estrutura de saída

Um arquivo será gerado com o nome:

```
hex_intervalo_normalizado.csv
```

Ele conterá as seguintes colunas:

| ID  | 2^ID | decimal | 2^(ID+1)-1 | proporcao | proporcao\_arredondada | decimal\_inverso | diferenca   |
| --- | ---- | ------- | ---------- | --------- | ---------------------- | ---------------- | ----------- |
| '0' | '1'  | '3'     | '3'        | '127.5'   | '128'                  | '3.0000000'      | '0.0000000' |

---

## 🚀 Como usar

### 📦 Requisitos

* Python 3.7+
* `pandas`

Instale o Pandas, caso ainda não tenha:

```bash
pip install pandas
```

---

### ▶️ Passo a passo

1. **Clone o repositório**

```bash
git clone https://github.com/canalqb/btc-normalizer.git
cd btc-normalizer
```

2. **Edite a precisão desejada**

No script, altere a linha:

```python
precisao_decimal = Decimal('1.0000000')
```

Para algo como:

* `'1.000000'` → 6 casas decimais
* `'1.000000000000'` → 12 casas decimais

3. **Adicione ou edite os valores em `hex_list`**

   * Use strings hexadecimais como `'1f'`, `'a3b'`, etc.
   * Valores `None` são ignorados automaticamente

4. **Execute o script**

```bash
python normalizador_hex_proporcional.py
```

5. **Verifique a saída**

   * O arquivo `hex_intervalo_normalizado.csv` será criado na mesma pasta

---

## 💡 Exemplo de cálculo

Suponha que o valor hexadecimal seja `'3'` com ID `2`:

* `2^2 = 4` → início do intervalo
* `2^3 - 1 = 7` → fim do intervalo
* Proporção: posição relativa entre 4 e 7
* Valor reconstruído: `decimal_inverso`
* Diferença entre original e reconstruído: `diferenca`

---

## 📦 Aplicações possíveis

* 🔐 Criptografia e segurança
* 💰 Blockchain e análise de endereços
* 📊 Compressão de dados
* 🧬 Estudo de entropia
* 🔁 Testes reversíveis de conversão proporcional

---

## ✅ Resultado final

Mensagem de sucesso no terminal:

```
✅ Arquivo 'hex_intervalo_normalizado.csv' criado com sucesso!
```

---

## 📬 Contato

Feito por [CanalQb no GitHub](https://github.com/canalqb)
Visite o blog: [canalqb.blogspot.com](https://canalqb.blogspot.com/)
💸 Apoie o projeto via Bitcoin:

```
13Ve1k5ivByaCQ5yer6GoV84wAtf3kNava
```

---

## 🧠 Licença

Este projeto está sob a licença **MIT**.
Sinta-se livre para usar, modificar e compartilhar.
