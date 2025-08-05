# 🧮 Calculadora de Pontos Médios em Potências de Dois

Este projeto contém um script Python que **calcula valores intermediários entre dois números** com base em **potências sucessivas de 2**, seguindo a fórmula:

```
val = 2^(2^t) mod (end + 1)
```

É útil em contextos como:

* 🔐 Algoritmos com estrutura de intervalos binários
* ⚙️ Processamento de intervalos crescentes
* 📚 Estudo de exponenciação modular e teoria dos números

---

## 📌 O que esse script faz?

O script lê pares de números (`início`, `fim`) com um valor intermediário (`meio`). Quando o meio não é fornecido (`?`), o script tenta **encontrar automaticamente** um valor que satisfaça:

```
start < val = 2^(2^t) mod (end + 1) < end
```

Se encontrado, o valor e o expoente `t` correspondente são exibidos.
Caso contrário, uma mensagem informando que não foi possível calcular será exibida.

---

## ▶️ Como usar?

1. **Clone este repositório ou baixe o arquivo:**

```bash
git clone https://github.com/seuusuario/power-of-two-midpoint-finder
cd power-of-two-midpoint-finder
```

2. **Execute o script diretamente com Python:**

```bash
python midpoint_finder.py
```

3. **Saída esperada no terminal:**

```
Intervalo: 128, ?, 255
Meio calculado: 193 (para t=5)
---
Intervalo: 2097152, 3007503, 4194303
Meio informado, sem cálculo.
---
```

---

## 🛠️ Funcionamento interno

* O script usa **exponenciação modular eficiente** para encontrar um valor dentro do intervalo.
* O processo testa valores de `t` entre `0` e `15` (pode ser ajustado).
* Os dados são processados linha a linha em um array de strings no seguinte formato:

  ```
  "start, mid, end"
  ```

  Se o valor de `mid` for `"?"`, será calculado automaticamente.

---

## 🧪 Exemplo de entrada:

```python
linhas = [
    "128, ?, 255",
    "256, 467, 511",
    "1024, ?, 2047"
]
```

## 🧾 Exemplo de saída:

```
Intervalo: 128, ?, 255
Meio calculado: 193 (para t=5)
---
Intervalo: 256, 467, 511
Meio informado, sem cálculo.
---
Intervalo: 1024, ?, 2047
Meio calculado: 1155 (para t=6)
---
```

---

## 📬 Contato

Feito por [CanalQb no GitHub](https://github.com/canalqb)
Visite o blog: [canalqb.blogspot.com](https://canalqb.blogspot.com/)
💸 Apoie o projeto via Bitcoin:
`13Ve1k5ivByaCQ5yer6GoV84wAtf3kNava`

---

## 📄 Licença

Distribuído sob a licença **MIT** — sinta-se livre para usar, modificar e compartilhar!
