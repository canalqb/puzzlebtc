# 📊 BTC Interval Midpoint Predictor

---

## 🚀 Sobre o Script

Este script é uma ferramenta **avançada de análise matemática** aplicada ao estudo de intervalos numéricos relacionados ao universo Bitcoin. Ele usa uma **regressão linear múltipla** para estimar o valor intermediário (meio) dentro de intervalos definidos por seus limites iniciais e finais. A abordagem é baseada em transformações logarítmicas, tratando grandes intervalos numéricos que surgem frequentemente em análise de dados blockchain.

---

## 🔍 Para que Serve?

Você já se perguntou como prever um valor *intermediário* entre dois extremos, baseado em padrões históricos de dados? Este script:

* Recebe uma lista de intervalos `(inicio, meio, fim)`.
* Filtra dados completos (sem valores faltantes).
* Transforma os dados usando logaritmos base 2 para lidar com a grande escala numérica.
* Usa regressão linear para calcular coeficientes que relacionam o meio ao início e fim do intervalo.
* Permite **estimar o ponto médio relativo** em novos intervalos, mesmo que o ponto intermediário real seja desconhecido.

Ideal para quem deseja:

* Modelar e prever padrões numéricos complexos.
* Trabalhar com dados financeiros, blockchain ou sistemas com intervalos exponenciais.
* Aprender técnicas práticas de regressão e modelagem estatística aplicada.

---

## ⚙️ Como Usar

### Passo a passo:

1. **Clone o repositório** ou copie o script `predict_midpoint.py` para seu ambiente local.
2. **Prepare seus intervalos**: eles devem seguir o formato `(inicio, meio, fim)`. Caso o meio seja desconhecido, ele pode ser omitido para previsão.
3. **Execute o script** para treinar o modelo usando os dados completos disponíveis.
4. **Use a função `prever_meio(inicio, fim)`** para obter a previsão do ponto médio relativo entre `inicio` e `fim`.
5. Analise os resultados impressos para validar suas previsões.

---

## 💡 Exemplo de saída

```plaintext
Previsões de meios estimados com varredura relativa:

Inicio: 1180591620717411303424
Fim:    2361183241434822606848
Previsão do meio relativo: 0.43
```

---

## 📬 Contato

Feito por **[CanalQb no GitHub](https://github.com/canalqb)**
Visite o blog: [canalqb.blogspot.com](https://canalqb.blogspot.com/)

💸 Apoie o projeto via Bitcoin:
`13Ve1k5ivByaCQ5yer6GoV84wAtf3kNava`

---

## ⚠️ Aviso

Este script é uma demonstração técnica e não constitui aconselhamento financeiro. Use-o para aprendizado e desenvolvimento de modelos preditivos, sempre validando os dados e resultados.
