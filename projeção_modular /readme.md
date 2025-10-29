# 🔢 - Teorema da Progressão Modular
[![Python](https://img.shields.io/badge/Python-3.7%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![LGN](https://img.shields.io/badge/Teorema-Lei%20dos%20Grandes%20Números-ff69b4.svg)](https://en.wikipedia.org/wiki/Law_of_large_numbers)

## Frase do Teorema

> "Valores em progressão modular se aproximam de certos limites previsíveis" – Isso significa que podemos estimar valores futuros usando padrões simples de repetição modular, mesmo que os números cresçam muito.

## Sumário

* [1. Introdução ao Teorema](#1-introdução-ao-teorema)
  * [1.1 Resumo](#11-resumo)
  * [1.2 Exemplos Práticos](#12-exemplos-práticos)
  * [1.3 Explicação Detalhada](#13-explicação-detalhada)
  * [1.4 Aplicações](#14-aplicações)
  * [1.5 Análise da Tabela](#15-análise-da-tabela)
* [2. Script `modular_prediction.py`](#2-script-modular_predictionpy)
  * [2.1 Relação com o Teorema](#21-relação-com-o-teorema)
  * [2.2 Objetivo do Script](#22-objetivo-do-script)
  * [2.3 Exemplo de Saída](#23-exemplo-de-saída)
  * [2.4 Funcionamento Interno](#24-funcionamento-interno)
  * [2.5 Tecnologias e Requisitos](#25-tecnologias-e-requisitos)
* [3 Extras](#3-extras)
  * [3.1 Licença](#31-licença)
  * [3.2 Referências](#32-referencias)
  * [3.3 Testes e Validações](#33-testes-e-validações)
* [4 Contato](#4-contato)
* [5. Nota](#5-nota)

---

## 1. Introdução ao Teorema

### 1.1 Resumo
O teorema explica como valores podem ser **previstos usando padrões modulares**. Quando aplicamos uma operação modular sucessivamente, os resultados começam a seguir uma curva previsível, mesmo em números grandes.

### 1.2 Exemplos Práticos
* Prever valores em sequências matemáticas ou algoritmos criptográficos.
* Estimar resultados em grandes progressões numéricas sem calcular todos os passos.

### 1.3 Explicação Detalhada
O cálculo modular é como "voltar ao início quando se ultrapassa um limite".  
Exemplo:  
Se temos 10 maçãs e damos 3 de cada vez, depois de algumas rodadas sobrará sempre o mesmo padrão de frutas. Esse "resto" é o que usamos para prever valores futuros.

### 1.4 Aplicações
* Matemática discreta e teoria dos números.
* Criptografia e segurança digital.
* Simulações computacionais que envolvem grandes sequências de números.

### 1.5 Análise da Tabela
O script gera uma tabela mostrando para cada 2^n:
* Valor real
* Valor de Mersenne (2^(n+1)-1)
* Predição modular
* Diferença (Δ)
* Percentual de Curva (%)

Isso permite **visualizar rapidamente o erro** de predição e a evolução da sequência.

---

## 2. Script `modular_prediction.py`

### 2.1 Relação com o Teorema
O script implementa a **regra de progressão modular** para gerar previsões numéricas e comparar com valores reais de Mersenne.

### 2.2 Objetivo do Script
* Gerar tabela completa de 2^n, valor, Mersenne, predição, Δ e curva percentual.
* Estimar o próximo valor da sequência usando padrão modular.

### 2.3 Exemplo de Saída
```

```
    4 |               7 |               7 |               7 |          0 |       0.00%
    8 |               8 |              15 |              15 |         -7 |     -87.50%
   16 |              21 |              31 |              24 |         -3 |     -14.29%
```

...
2^31 = 1073741824 → previsão ≈ 1373560525

```

### 2.4 Funcionamento Interno
1. Para cada linha, calcula a predição como:  
   `predicao = valor_anterior % pot + pot`
2. Calcula a diferença Δ entre valor real e predição.
3. Converte Δ em **percentual de curva**, indicando o erro relativo.
4. Exibe tabela completa com formatação legível.

### 2.5 Tecnologias e Requisitos
* Python 3.8.10
* Sem bibliotecas externas
* Qualquer terminal ou IDE que suporte Python

---

## 3 Extras

### 3.1 Licença
MIT License – Use e modifique livremente.

### 3.2 Referências
* Lei dos Grandes Números: [Wikipedia](https://en.wikipedia.org/wiki/Law_of_large_numbers)

### 3.3 Testes e Validações
* Testado com valores de 2^2 até 2^30.
* Percentual de curva avaliado para garantir previsões consistentes.

---

## 4 Contato
* Feito por CanalQb no GitHub
* Blog: [https://canalqb.blogspot.com](https://canalqb.blogspot.com)
* 💸 Apoie via Bitcoin: 13Ve1k5ivByaCQ5yer6GoV84wAtf3kNava
* PIX: [qrodrigob@gmail.com](mailto:qrodrigob@gmail.com)

*Readme.md corrigido por ChatGPT*

---

## 5. Nota
* {**Valor Modular**}: O resultado de uma operação "resto da divisão", ou seja, o que sobra quando um número é dividido por outro.  
* {**Mersenne**}: Números da forma 2^(n+1) - 1. São importantes em matemática e criptografia.  
* {**Δ (Delta)**}: Diferença entre valor real e valor previsto. Indica erro.  
* {**Curva (%)**}: Percentual de diferença em relação ao valor real, mostrando o desvio da predição.  
* {**Predição**}: Estimativa do próximo valor usando regra modular simples.  
``` 
