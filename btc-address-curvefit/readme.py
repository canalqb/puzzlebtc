# 📈 Estimador de Intervalos BTC com Regressão Logarítmica

Este projeto tem como objetivo **estimar valores desconhecidos** em intervalos de dados relacionados ao universo do Bitcoin usando **ajuste de curva com regressão logarítmica**.

Utilizando a biblioteca `SciPy`, o script aplica `curve_fit` para encontrar os melhores parâmetros de uma função logarítmica que se ajusta aos dados fornecidos.

---

## 🔍 Sobre o que é esse script?

Este script Python serve para:

🔢 Analisar **intervalos numéricos de endereços ou chaves** (por exemplo, faixas de valores de chaves privadas Bitcoin)
📉 Aplicar uma **função logarítmica ajustada** aos dados
❓ Estimar o valor de um ponto onde o dado está **indisponível (None)**
📊 Utilizar **métodos científicos e estatísticos** confiáveis com `SciPy` para prever tendências ou preencher lacunas

---

## 🧠 Como ele funciona?

A função utilizada é:

```python
f(x) = A * log(B * x + C) + D
```

Ela é ajustada aos dados de entrada com base nos intervalos conhecidos e então usada para **prever o valor do ponto faltante**.

---

## 🛠️ Tecnologias e Bibliotecas

* 🐍 **Python 3**
* 🔬 `numpy`
* 🧮 `scipy.optimize.curve_fit`

---

## 📦 Instalação

1. Clone o repositório:

   ```
   git clone https://github.com/seuusuario/btc-address-curvefit.git
   ```

2. Instale as dependências:

   ```
   pip install numpy scipy
   ```

3. Execute o script:

   ```
   python estimador_intervalos_btc.py
   ```

---

## 🧾 Exemplo de uso

Com os seguintes dados de entrada:

```python
intervalos = [
    (1073741824, 2102388551, 2147483647),
    (2147483648, 3093472814, 4294967295),
    (4294967296, 7137437912, 8589934591),
    (8589934592, 14133072157, 17179869183),
    (17179869184, None, 34359738367)
]
```

A saída será parecida com:

```
Parâmetros ajustados: A=..., B=..., C=..., D=...
Valor estimado para 'None': 28351901245
```

---

## 👣 Passo a passo para usar

1. 📥 Edite a variável `intervalos` com os seus dados (mantenha `None` onde deseja estimar).
2. 🧠 O script irá:

   * Calcular o ponto médio dos intervalos.
   * Ajustar uma curva logarítmica aos dados disponíveis.
   * Estimar o valor onde o dado está ausente.
3. 🖨️ Veja o resultado no terminal.

---

## 📬 Contato

Feito por [CanalQb no GitHub](https://github.com/canalqb)
Visite o blog: [canalqb.blogspot.com](https://canalqb.blogspot.com/)
💸 Apoie o projeto via Bitcoin: `13Ve1k5ivByaCQ5yer6GoV84wAtf3kNava`
