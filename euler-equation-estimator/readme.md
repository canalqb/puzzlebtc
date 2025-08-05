# 🌀 Euler Equation Estimator

> Uma ferramenta didática para simular combinações e estimativas da **Equação de Euler** usando valores discretos e potências de 2

---

## 📖 O que este projeto faz?

Este script é uma abordagem simples e ilustrativa para **estimar a força de uma forma básica da equação de Euler** aplicada a dinâmica de fluidos:

> 🧪 *Força estimada = ρ × u² + p*

Onde:

* `ρ` (rho) = densidade do fluido
* `u` = velocidade do fluido
* `p` = pressão

O script percorre uma lista de números inteiros e, para cada um:

1. **Gera valores base relacionados à potência de 2 mais próxima** (log₂(n)).
2. **Monta diferentes combinações de ρ, u e p** com os valores `[n, 2^N, 2^(N+1) - 1]`.
3. **Aplica a equação simplificada** em todas as combinações e mostra os resultados.

---

## 🧠 Objetivo do Script

* Explorar **relações numéricas entre potências de 2 e variáveis físicas**.
* Demonstrar uma forma simplificada das equações de Euler.
* **Analisar padrões** que surgem da manipulação de grandezas físicas com números binários.
* Pode servir como base para testes matemáticos, fins educacionais ou visualizações experimentais.

---

## ⚙️ Como funciona

### 📌 Lista de valores testados:

```
[1, 3, 7, 8, 21, 50, 76, 224, 467, 514, 1155, 2683, 5216, 10544, 26867, 51510]
```

### 🔄 Para cada número `n`:

1. Calcula:

   * `val1 = n`
   * `val2 = 2^floor(log2(n))`
   * `val3 = 2^(floor(log2(n)) + 1) - 1`

2. Gera 6 combinações entre `rho`, `u` e `p`, por exemplo:

   * `(rho=n, u=2^N, p=2^(N+1)-1)`
   * `(rho=2^(N+1)-1, u=n, p=2^N)`
   * *(e outras variações...)*

3. Calcula:

   ```
   Força estimada = rho * u^2 + p
   ```

4. Exibe o resultado com 4 casas decimais para facilitar comparação.

---

## 📥 Como executar

1. Clone o repositório:

```
git clone https://github.com/canalqb/euler-equation-estimator.git
cd euler-equation-estimator
```

2. Execute o script diretamente com Python:

```
python estimate_euler_force.py
```

> ✅ Nenhuma biblioteca externa é necessária — tudo funciona apenas com a biblioteca padrão (`math`).

---

## 💡 Exemplos de uso

🧪 Ideal para:

* Estudantes explorando física computacional
* Professores que desejam ilustrar a equação de Euler de forma numérica
* Pesquisadores buscando insights de padrões com potências de 2
* Entusiastas de matemática experimental e modelagem simbólica

---

## 📬 Contato

Feito por [CanalQb no GitHub](https://github.com/canalqb)
Visite o blog: [canalqb.blogspot.com](https://canalqb.blogspot.com/)
💸 Apoie o projeto via Bitcoin:
`13Ve1k5ivByaCQ5yer6GoV84wAtf3kNava`
