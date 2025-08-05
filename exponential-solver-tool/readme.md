# 🧮 Exponential Division Solver — Ferramenta para Resolver Equações com Potências de 2

Este projeto contém dois scripts matemáticos em Python voltados para encontrar valores relacionados a potências de dois em equações específicas. Ele resolve dois tipos de problemas com foco em precisão e desempenho.

---

## 📌 O que o script resolve?

### 🔍 Parte 1 – Encontrar `EXP` e `L` a partir de `X` e `N`

Resolve a seguinte equação:

```
X * EXP = L * 2^(N+1)
```

Onde:

* `X` é fornecido
* `N` é o expoente fixo
* O script **tenta encontrar um `EXP` (potência de 2)** e um **valor de `L`** que satisfaçam essa equação.

### 🔍 Parte 2 – Encontrar `X` a partir de `EXP`, `L` e `N`

Resolve:

```
X = (L * 2^N * 2) / EXP
```

Neste caso, o script busca todos os possíveis valores de `X` que **caibam no intervalo \[2^N, 2^{N+1} - 1]**.

---

## ⚙️ Como funciona?

### 🔁 Algoritmos implementados

* **Precisão alta com `decimal.Decimal`**: garante resultados confiáveis mesmo com grandes potências.
* **Loop reverso em `EXP = 2^i` até 2^256**: busca a maior potência que satisfaça a equação.
* **Intervalo dinâmico para `L`**: valores testados de forma incremental.

---

## ▶️ Como usar

1. **Clone o repositório ou baixe o arquivo:**

```bash
git clone https://github.com/seuusuario/exponential-solver-tool
cd exponential-solver-tool
```

2. **Instale o Python 3 (recomenda-se versão 3.8+)**

3. **Execute o script com:**

```bash
python exponential_division_solver.py
```

---

## 📂 Exemplos práticos

### 🧪 Exemplo 1: Encontrar `EXP` e `L` a partir de `X`

```python
encontrar_exp_por_x(12, 5216)
```

💡 Resultado:

```
Encontrado: EXP=4096 (2^12), L=5216, X=5216
```

---

### 🧪 Exemplo 2: Encontrar `X` para múltiplos valores de `EXP` e `L`

```python
encontrar_X_por_exp_e_l(8)
```

💡 Saída:

```
N=8, EXP=2^2=4, L=128, X=16384
N=8, EXP=2^3=8, L=128, X=8192
...
```

---

## 💡 Casos de uso

* 🧠 Estudos de criptografia modular
* 📈 Simulações matemáticas com restrições binárias
* 🛠️ Engenharia reversa de algoritmos de compressão, hashing, codificação
* 🧪 Testes de aritmética binária

---

## 📬 Contato

Feito por [CanalQb no GitHub](https://github.com/canalqb)
Visite o blog: [canalqb.blogspot.com](https://canalqb.blogspot.com/)
💸 Apoie o projeto via Bitcoin:
`13Ve1k5ivByaCQ5yer6GoV84wAtf3kNava`

---

## 📄 Licença

Distribuído sob a licença **MIT** — totalmente livre para uso pessoal, acadêmico ou comercial.
🚫 Nenhuma responsabilidade é assumida pelo uso indevido dos scripts.
