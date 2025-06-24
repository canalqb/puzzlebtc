# Collatz Steps Database

Este projeto contém um script Python para calcular o número de passos na conjectura de Collatz para números dentro de um intervalo definido por bits, e armazenar os resultados em um banco de dados SQLite.

## Descrição

O script calcula, para todos os números no intervalo `[2^bits, 2^(bits+1) - 1]`, quantos passos são necessários para chegar a 1 na sequência de Collatz. Os números são organizados e armazenados em tabelas SQLite, classificadas pelo número de passos.

Para otimizar, utiliza cache para evitar recomputações durante a avaliação dos passos.

## Funcionalidades

* Calcula passos da sequência de Collatz para grandes intervalos definidos por bits.
* Usa cache para otimização da computação.
* Armazena resultados em banco SQLite com tabelas separadas para cada quantidade de passos.
* Permite processamento em lotes para inserção eficiente no banco de dados.
* Exibe estatísticas básicas e tempo de execução.

## Como usar

1. Certifique-se de ter Python 3 instalado.

2. Clone este repositório ou copie o script para sua máquina.

3. Execute o script:

```bash
python collatz_db.py
```

4. Informe o número de bits do intervalo para busca (de 1 a 160).

5. O script cria um arquivo SQLite `<bits>.db` com as tabelas dos resultados.

## Estrutura do Banco de Dados

* Para cada número de passos `p`, existe uma tabela chamada `passos_p`.
* Cada tabela armazena os números que levam exatamente `p` passos para atingir 1.

## Exemplo de Uso

Se você informar `bits = 10`, o script processará números de 1024 a 2047.

## Dependências

* Python 3.x (testado com 3.8+)
* Módulo `sqlite3` (incluso na biblioteca padrão do Python)

## Melhorias Futuras

* Interface gráfica para visualização dos dados.
* Paralelização para acelerar cálculos em intervalos maiores.
* Exportação dos resultados para formatos CSV ou JSON.

## Licença

Este projeto está sob a licença MIT.
