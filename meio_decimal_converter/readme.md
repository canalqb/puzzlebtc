## 📁 Objetivo
```markdown
# 📊 Gerador de Tabela de Meios em Decimal

Este projeto gera uma tabela CSV (`Tabela_Corrigida.csv`) a partir de uma lista de valores hexadecimais chamados **"meios"**, realizando a conversão para decimal e aplicando cálculos matemáticos com alta precisão.

## 🔍 Objetivo

- Converter valores hexadecimais (representando "meios") para decimal.
- Calcular valores derivados com base em potências de dois (`2^n`) e gerar uma tabela estruturada.
- Evitar notação científica e manter precisão decimal alta com o uso de `decimal.Decimal`.

```
## 📁 Estrutura do Projeto

```

meio\_decimal\_converter/
├── gerar\_tabela\_meios.py
├── Tabela\_Corrigida.csv  # (Gerado após executar o script)
└── README.md

````

## ⚙️ Como Usar

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/meio_decimal_converter.git
cd meio_decimal_converter
````

2. Execute o script:

```bash
python gerar_tabela_meios.py
```

3. O arquivo `Tabela_Corrigida.csv` será gerado na mesma pasta.

## 🧮 Detalhes Técnicos

* Usa a biblioteca `decimal` para precisão numérica (50 casas decimais).
* Lê os valores de `meios`, converte para decimal e calcula:

  * `2^ID` (início)
  * `2^(ID+1)-1` (fim)
  * Cálculo intermediário:

    ```python
    valor = inicio / ((potencia + meio_decimal) * 2) / 256
    ```
* Formatação do valor resultante para garantir:

  * Separador decimal com vírgula
  * Sem notação científica
  * Precisão visual

## 📌 Requisitos

* Python 3.6+
* Nenhuma biblioteca externa além da padrão (`csv`, `decimal`)

## 📄 Licença

MIT. Veja o arquivo [LICENSE](LICENSE) (adicione se necessário).

---

Feito com 💻 por [CanalQb ou GitHub](https://github.com/canalqb)
