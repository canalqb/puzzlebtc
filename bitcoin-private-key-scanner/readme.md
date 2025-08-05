# 🔐 Bitcoin Private Key Scanner

Este projeto é um **scanner matemático de chaves privadas Bitcoin**, que calcula possíveis valores de `X` baseados em uma fórmula envolvendo potências de 2. Em seguida, o script gera **endereços públicos** a partir de `X` e os compara com uma **lista conhecida de endereços Bitcoin**.

---

## 🎯 Objetivo

O script busca descobrir se **algum endereço conhecido** pode ser derivado de uma chave privada gerada com a fórmula:

```
X = (2^N * L * 2) / EXP
```

* `N` = potência base configurada pelo usuário
* `L` = número multiplicador incremental
* `EXP` = potências de 2 (de 2¹ até 2²⁵⁶)
* `X` = possível chave privada

---

## ⚙️ Como funciona

1. Gera uma lista de valores `X` com base na equação
2. Valida se `X` está no intervalo permitido de chaves privadas da curva secp256k1
3. Usa a biblioteca `bitcoinlib` para:

   * Derivar a chave WIF (Wallet Import Format)
   * Gerar o endereço público (formato legacy)
4. Verifica se o endereço gerado **já existe em uma lista conhecida**
5. Salva **um checkpoint automático** a cada 10 milhões de iterações

---

## 🚀 Como usar

### ✅ Pré-requisitos

* Python 3.8+
* Instale a biblioteca:

```bash
pip install bitcoinlib
```

---

### ▶️ Executar o script

```bash
python find_matching_bitcoin_address.py
```

Você será solicitado a informar o valor de `N`:

```bash
Digite o valor de N: 12
```

O script começará a calcular os possíveis valores de `X`, gerar chaves e verificar os endereços.

---

## 💾 Checkpoints

* O script salva o progresso em um arquivo `checkpoint.txt`
* Se você interromper a execução, **ela será retomada automaticamente do ponto salvo**

---

## 🧪 O que acontece se um endereço for encontrado?

Se o script gerar um endereço que **já está na lista conhecida**, ele:

✅ Exibe as informações completas no terminal
📁 Cria um arquivo chamado:

```
{endereco}_endereco_encontrado.txt
```

Com os dados:

* Endereço público encontrado
* Chave WIF
* Valor de `X`, `L`, `EXP` e `N`

---

## 🛠️ Casos de uso

* 🔐 Pesquisa de vulnerabilidades ou colisões de chave
* 🔍 Auditoria educacional de geração de endereços
* 🧠 Estudos de matemática aplicada à criptografia Bitcoin

> ⚠️ **Atenção**: Este projeto é apenas para fins educacionais e acadêmicos. O uso inadequado pode ser ilegal ou antiético.

---

## 🧠 Fórmulas envolvidas

### 🎓 Cálculo de `X`:

```
X = (2^N * L * 2) / EXP
```

### 🎯 Validação de intervalo:

```
X ∈ [2^N, 2^(N+1) - 1]
```

---

## 📬 Contato

Feito por [CanalQb no GitHub](https://github.com/canalqb)
Visite o blog: [canalqb.blogspot.com](https://canalqb.blogspot.com/)
💸 Apoie o projeto via Bitcoin:
`13Ve1k5ivByaCQ5yer6GoV84wAtf3kNava`

---

## 📄 Licença

📝 **MIT License**
Você é livre para usar, modificar, estudar ou distribuir, **por sua conta e risco**.
