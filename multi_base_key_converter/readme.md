


# 🔐 Multi Base Key Converter
```markdown

Este projeto contém um script Python que:

- Gera chaves privadas aleatórias dentro de intervalos de potências de 2.
- Converte cada número aleatório gerado em várias bases numéricas (2, 16, 32, 58, 62 e 85).
- Também converte cada número para formato **WIF (Wallet Import Format)** usando a biblioteca `bit`.
```
---

## 🚀 Objetivo

Demonstrar como representar um número grande (como uma chave privada de Bitcoin) em diferentes bases numéricas e gerar a chave no formato WIF, comum em carteiras de criptomoedas.

---

## 📦 Bases Suportadas

- **Base 2** (Binário)
- **Base 16** (Hexadecimal)
- **Base 32** (RFC 4648)
- **Base 58** (Usada no Bitcoin)
- **Base 62** (Letras e números)
- **Base 85** (ASCII 85, semelhante ao Base64)

---

## ⚙️ Como funciona

1. Para cada valor de `n` de 50 até 161:
   - Gera um número aleatório entre `2^n` e `2^(n+1) - 1`
   - Converte o número para WIF usando a biblioteca `bit`
   - Converte o mesmo número para todas as bases acima usando uma função customizada
   - Exibe os resultados no console

---

## 🧪 Exemplo de saída

```

intervalo 51
numeroaleatorio L3B7LZ3QZNVN5wAPMzVjM3YBiQvUULPH9rEvxXpMDuX6z4nPUD8Z - 100101..., 3F7A9C..., EAQF3..., etc.

````

> (A saída exibe o WIF e a representação do mesmo número em todas as bases)

---

## 🧰 Requisitos

- Python 3.6+
- Biblioteca [`bit`](https://ofek.dev/bit/)

Instale a biblioteca `bit` com:

```bash
pip install bit
````

---

## ▶️ Como executar

```bash
python gerar_chaves_multibase.py
```

---

## 📄 Licença

MIT

---

## 📬 Contato

Feito por [CanalQb ou GitHub](https://github.com/canalqb)

Visite o Blog [CanalQb](https://canalqb.blogspot.com/)
