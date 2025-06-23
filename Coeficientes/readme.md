## Descrição

Este script contém dois conjuntos de dados principais:

* **dados**: Uma lista de tuplas, onde cada tupla representa um intervalo numérico com três valores em formato string.
* **data\_address**: Uma lista de strings representando endereços (possivelmente endereços de carteira, identificadores ou similares).

Esses dados podem ser usados para mapeamento, busca ou validação em sistemas que trabalham com grandes números e endereços associados.

---

## Estrutura dos dados

### `dados`

Cada elemento da lista é uma tupla com três valores do tipo string:

```python
('início_intervalo', 'valor_intermediário', 'fim_intervalo')
```

O campo `'None'` indica ausência de valor para alguns intervalos.

### `data_address`

Lista de strings, que podem representar endereços ou identificadores associados aos intervalos.

---

## Como usar

Este arquivo contém somente os dados, você deve implementar as funções necessárias para processá-los, por exemplo:

* Buscar a qual intervalo um número pertence
* Mapear um endereço a um intervalo específico
* Validar se um número está dentro de algum intervalo

Exemplo simples para verificar se um número pertence a algum intervalo:

```python
def encontra_intervalo(numero):
    for inicio, meio, fim in dados:
        if fim == 'None':
            if int(numero) >= int(inicio):
                return (inicio, meio, fim)
        else:
            if int(inicio) <= int(numero) <= int(fim):
                return (inicio, meio, fim)
    return None

numero = '1500000000000'
intervalo = encontra_intervalo(numero)
if intervalo:
    print(f"Número {numero} está no intervalo {intervalo}")
else:
    print(f"Número {numero} não está em nenhum intervalo.")
```

---

## Requisitos

* Python 3.x

---

## Observações

* As strings representam números muito grandes e podem exceder o limite dos inteiros padrão dependendo da versão do Python (Python 3 lida bem com inteiros arbitrariamente grandes).
* Certifique-se de tratar corretamente valores `'None'` nas tuplas.
* Ajuste o script para o uso desejado, pois este arquivo serve como base de dados. 
