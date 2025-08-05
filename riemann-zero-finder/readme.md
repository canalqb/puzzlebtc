# 🧮 Riemann Zero Finder

> **Encontre zeros não triviais da função zeta de Riemann e armazene resultados com codificação WIF**

---

## 🚀 O que é este projeto?

Este script é uma ferramenta avançada para **calcular zeros não triviais da função zeta de Riemann**, aquela famosa função que está no centro de uma das maiores conjecturas da matemática: a Hipótese de Riemann.

* Ele **varre intervalos muito grandes**, buscando zeros na linha crítica $\text{Re}(s) = 0.5$.
* Ajusta **dinamicamente a precisão numérica** para garantir resultados confiáveis.
* **Armazena os resultados** em um banco de dados SQLite para análise posterior.
* Cada zero encontrado é convertido em uma chave privada Bitcoin no formato WIF (Wallet Import Format) — uma forma curiosa e criativa de codificar esses números.

---

## 🔍 Como funciona?

### Passo a passo do processo:

1. **Configuração dinâmica da precisão numérica**

   A precisão dos cálculos (número de dígitos decimais) é ajustada conforme o intervalo que será analisado, para garantir exatidão mesmo em valores muito grandes.

2. **Busca por zeros em intervalos**

   O script verifica subintervalos em uma faixa $[2^{valor}, 2^{valor+1})$, procurando onde o valor real da função zeta muda de sinal — um indício da presença de zero.

3. **Refinamento com método numérico**

   Quando detectada uma possível raiz, o script utiliza o método de Müller para encontrar a posição exata do zero com alta precisão.

4. **Codificação do zero em chave WIF**

   O valor imaginário do zero é convertido em uma chave privada Bitcoin no formato WIF, permitindo armazenamento e uso criativo dos dados.

5. **Armazenamento em banco SQLite**

   Os dados são salvos em uma tabela com os campos:

   * `valor`: indica o intervalo $valor$ usado, como referência.
   * `wif`: a chave privada Bitcoin gerada.

6. **Processamento em lotes**

   Para otimizar memória e desempenho, os intervalos são processados em lotes grandes, com coleta de lixo (garbage collection) a cada ciclo.

---

## 📋 Requisitos

* Python 3.7+
* Bibliotecas Python:

  * `mpmath`
  * `bit`
  * `sqlite3` (nativo do Python)
* Espaço em disco suficiente para banco SQLite

---

## ⚙️ Como usar

1. Clone o repositório:

```bash
git clone https://github.com/canalqb/riemann-zero-finder.git
cd riemann-zero-finder
```

2. Instale as dependências:

```bash
pip install mpmath bit
```

3. Execute o script principal:

```bash
python find_riemann_zeros.py
```

4. O banco de dados `zerosdeRiemann.db` será criado/atualizado na pasta atual, contendo os zeros encontrados e suas chaves WIF.

---

## 🧠 Considerações técnicas

* A função zeta de Riemann é avaliada na linha crítica $s = 0.5 + it$, onde $t$ varia.
* O método Müller é usado para garantir precisão em encontrar os zeros reais.
* A conversão para WIF usa o valor inteiro da parte imaginária, que representa o zero.
* O script é projetado para rodar em intervalos exponenciais grandes, garantindo escalabilidade.
* O banco de dados pode ser usado para estudos matemáticos ou projetos que envolvam números complexos associados à criptografia.

---

## 📬 Contato

Feito por [CanalQb no GitHub](https://github.com/canalqb)
Visite o blog: [canalqb.blogspot.com](https://canalqb.blogspot.com/)
💸 Apoie o projeto via Bitcoin: `13Ve1k5ivByaCQ5yer6GoV84wAtf3kNava`
