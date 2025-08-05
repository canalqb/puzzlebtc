# 📊 Estimador de Pontos Médios com Base em Logaritmos `log₂`

Este projeto implementa uma técnica estatística para **estimar a posição do ponto médio** em um intervalo `[início, fim]`, usando uma **regressão polinomial baseada em `log₂(início)` e `log₂(fim)`**.

---

## 🎯 Objetivo

Em vez de simplesmente tirar a média de `início` e `fim`, este script tenta prever um valor "central" *observado/ajustado* com base em dados anteriores.
É ideal para situações em que os pontos médios seguem um comportamento **logarítmico não linear**.

---

## 🤓 Como funciona?

O script parte de uma base de dados com tuplas `(início, meio_observado, fim)` e realiza:

1. **Normalização dos valores** — calcula a posição relativa do meio no intervalo.
2. **Extração de características logarítmicas** — usando `log₂` e `log₂²` dos extremos.
3. **Treinamento de uma regressão polinomial** — para modelar a relação com mais precisão.
4. **Geração de uma função de previsão** — reutilizável para novos intervalos.

---

## 🧮 Técnicas aplicadas

* 📐 **Regressão Linear Simples**
* 🧠 **Regressão Polinomial de 2ª ordem**
* 🔢 **Modelagem com `numpy.linalg.lstsq()`**
* 📊 **Análise de erro real vs. previsto**

---

## ✅ Exemplo de uso

### Código:

```python
inicio = 2048
fim = 4095
meio_estimado = prever_meio(inicio, fim)
print(f"Meio estimado: {meio_estimado:.2f}")
```

### Saída:

```
Meio estimado para o intervalo 2048-4095: 2243.30
```

O valor é *diferente da média aritmética*, pois considera a curva ajustada pelos logs dos limites.

---

## 🔍 O que tem no script?

* **`dados`** com intervalos e meios observados
* Normalização via:

  ```python
  meio_rel = (meio - inicio) / (fim - inicio)
  ```
* Cálculo de `log₂`, `log₂²` e `log₂(início) * log₂(fim)`
* Ajuste dos coeficientes com:

  ```python
  np.linalg.lstsq(X, y)
  ```
* Função reutilizável `prever_meio()` pronta para uso em outros projetos

---

## 📦 Requisitos

* **Python 3.7+**
* **Numpy**
* **Pandas**

Instale os pacotes necessários com:

```bash
pip install numpy pandas
```

---

## 📌 Aplicações possíveis

* 🔬 Modelagem de padrões logarítmicos
* 📈 Previsão em séries temporais com comportamento exponencial
* 🧠 Machine Learning interpretável com base em transformações matemáticas
* 📚 Educação e demonstração de regressão polinomial com variáveis transformadas

---

## 📬 Contato

Feito por [CanalQb no GitHub](https://github.com/canalqb)
Visite o blog: [canalqb.blogspot.com](https://canalqb.blogspot.com/)
💸 Apoie o projeto via Bitcoin: `13Ve1k5ivByaCQ5yer6GoV84wAtf3kNava`
