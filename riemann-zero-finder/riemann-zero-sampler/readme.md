# 🎯 Riemann Zero Sampler

> Ferramenta para amostragem e identificação de zeros não triviais da função zeta de Riemann com codificação WIF

---

## ✨ Sobre este projeto

Este script foi desenvolvido para **encontrar zeros não triviais da função zeta de Riemann** na linha crítica $\text{Re}(s) = 0.5$, usando uma técnica de amostragem em grandes intervalos numéricos.

Além disso, cada zero identificado é **convertido em uma chave privada Bitcoin no formato WIF (Wallet Import Format)**, criando uma associação curiosa entre matemática pura e criptografia.

O resultado é armazenado em um banco de dados SQLite para posterior análise e uso.

---

## 🔎 Como o script funciona?

### Passo a passo detalhado:

1. **Ajuste Dinâmico da Precisão Numérica**
   A precisão dos cálculos (quantidade de dígitos decimais) é configurada com base no intervalo de busca, garantindo exatidão mesmo em valores muito grandes.

2. **Amostragem por Intervalos**
   O script percorre a linha crítica em passos grandes (exemplo: 10.000 em 10.000), buscando mudanças de sinal no valor real da função zeta, o que indica a presença de zeros.

3. **Refinamento Local dos Zeros**
   Ao detectar uma mudança de sinal, a função `findroot` é usada para calcular o zero com alta precisão, utilizando o método bissecção e tolerância rigorosa.

4. **Tratamento de Erros e Debug**
   Caso haja erro na busca do zero, o script gera e exibe chaves WIF para valores próximos, ajudando na identificação e diagnóstico.

5. **Conversão em Chaves Bitcoin**
   O valor inteiro da parte imaginária do zero encontrado é convertido em uma chave privada Bitcoin, exibida nos formatos p2wpkh, p2pkh e p2wpkh-p2sh.

6. **Armazenamento em Banco de Dados**
   Cada chave gerada é salva em uma tabela SQLite junto com o valor do intervalo para garantir rastreabilidade.

---

## ⚙️ Como usar

1. Clone o repositório:

```
git clone https://github.com/canalqb/riemann-zero-sampler.git
cd riemann-zero-sampler
```

2. Instale as dependências:

```
pip install mpmath bit
```

3. Execute o script principal:

```
python sample_riemann_zeros.py
```

4. Os zeros encontrados e suas chaves WIF ficarão salvos no arquivo `zerosdeRiemann.db`.

---

## 📌 Detalhes importantes

* A amostragem é feita em intervalos exponenciais $[2^{valor}, 2^{valor+1})$, com `valor` configurável no script.
* O método de busca usa **bissecção** para maior estabilidade.
* A tolerância de erro é configurada para **1e-18**, um nível alto para precisão.
* Passo de amostragem (step) padrão é 10.000, mas pode ser ajustado conforme necessidade.
* Uso intensivo de **coleta de lixo** para otimizar memória em grandes execuções.

---

## 🛠 Requisitos

* Python 3.7+
* Bibliotecas:

  * `mpmath`
  * `bit`
  * `sqlite3` (embutido no Python)

---

## 💡 Aplicações

* Estudos avançados sobre a **Hipótese de Riemann**.
* Exploração matemática e computacional da função zeta.
* Experimentos interdisciplinares ligando números complexos e criptografia.
* Banco de dados com chaves Bitcoin geradas a partir de dados matemáticos.

---

## 📬 Contato

Feito por [CanalQb no GitHub](https://github.com/canalqb)
Visite o blog: [canalqb.blogspot.com](https://canalqb.blogspot.com/)
💸 Apoie o projeto via Bitcoin: `13Ve1k5ivByaCQ5yer6GoV84wAtf3kNava`
