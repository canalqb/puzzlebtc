---

# 🔍 Sequence Model Finder

Este projeto contém um **script Python** que busca identificar o modelo (coeficientes e sementes iniciais) de uma sequência numérica gerada por uma relação linear recursiva.

---

## ✨ O que o script faz?

Dado um conjunto de dados parciais com valores de uma sequência em índices específicos, o script tenta **descobrir os coeficientes e sementes iniciais** de um modelo que gere essa sequência.

* Utiliza um método **força bruta** para testar diferentes combinações de coeficientes e sementes;
* Cada combinação é avaliada para verificar se reproduz os valores fornecidos nos índices intermediários;
* Quando um modelo válido é encontrado, o script retorna:

  * O número de coeficientes/sementes (`k`),
  * Os coeficientes,
  * As sementes iniciais,
  * E a sequência gerada;
* Com o modelo descoberto, é possível prever valores futuros da sequência, inclusive índices não fornecidos no input.

---

## 🚀 Como funciona?

1. **Entrada:**
   Um conjunto de dados contendo os valores de uma sequência em índices específicos (exemplo: início, meio, fim).

2. **Geração de sequência:**
   A partir de sementes e coeficientes, o script gera a sequência segundo a fórmula recursiva:

   > seq\[i] = coef\[0] \* seq\[i-1] + coef\[1] \* seq\[i-2] + ... + coef\[k-1] \* seq\[i-k]

3. **Teste de modelos:**
   Tenta todas as combinações possíveis de coeficientes e sementes dentro de limites definidos:

   * `coef_range` controla o valor máximo de coeficientes testados;
   * `seed_range` controla o valor máximo das sementes;
   * `max_k` determina o número máximo de coeficientes/sementes.

4. **Validação:**
   Verifica se a sequência gerada bate exatamente com os valores dos índices fornecidos.

5. **Resultado:**

   * Se encontrar um modelo que satisfaça as condições, imprime coeficientes, sementes e sequência;
   * Caso contrário, informa que não encontrou modelo válido.

---

## 📋 Exemplo de uso

```python
dados = [
    (1, 1, 1),
    (2, 3, 3),
    (4, 7, 7),
    (8, 8, 15),
    (16, 21, 31),
    (32, 49, 63),
]

indices_meio = [(ini if ini == fim else (ini + fim) // 2, meio) for ini, meio, fim in dados]

resultado = testar_modelos(indices_meio, coef_range=6, seed_range=10, max_k=3)

if resultado:
    seq = gerar_sequencia(resultado['sementes'], resultado['coef'], 128)
    print("✅ Coeficientes encontrados:", resultado['coef'])
    print("✅ Sementes encontradas:", resultado['sementes'])
    print("🔮 Valor previsto para índice 95 (linha 6 - Meio):", seq[95])
else:
    print("❌ Nenhum modelo válido encontrado.")
```

---

## ⚙️ Como rodar o script

1. Clone o repositório
2. Navegue até a pasta `sequence-model-finder`
3. Execute:

   ```bash
   python find_sequence_model.py
   ```
4. Observe a saída no terminal para ver o modelo encontrado e a previsão.

---

## 📬 Contato

Feito por [CanalQb no GitHub](https://github.com/canalqb)
Visite o blog: [canalqb.blogspot.com](https://canalqb.blogspot.com/)
💸 Apoie o projeto via Bitcoin: `13Ve1k5ivByaCQ5yer6GoV84wAtf3kNava`

---
 
