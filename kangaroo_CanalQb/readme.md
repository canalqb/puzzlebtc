# Bitcoin Puzzle Solver KangaRoo CanalQb

Este projeto é uma ferramenta para busca direta de chaves privadas que correspondam a uma lista específica de endereços Bitcoin. O programa verifica intervalos de chaves privadas baseados no número de puzzle informado, com checkpointing para salvar progresso e retomar buscas interrompidas.

## Funcionalidades

* Busca eficiente em intervalos determinados pelo número do puzzle.
* Verificação de chaves privadas convertidas para endereços Bitcoin contra uma lista alvo.
* Salva progresso automaticamente a cada 1 milhão de tentativas para evitar perda de dados.
* Retoma buscas a partir do último progresso salvo.
* Exibe progresso detalhado durante a execução.

## Como funciona

O programa calcula um intervalo `[MIN, MAX]` para o puzzle informado, onde:

* `MIN = 2^(puzzle_number - 1)`
* `MAX = 2^puzzle_number - 1`

Ele então percorre todas as chaves privadas no intervalo, convertendo cada uma em endereço Bitcoin para verificar se corresponde a algum da lista alvo. Caso encontre, imprime a chave privada decimal e o endereço correspondente.

## Pré-requisitos

* Python 3.7+
* Bibliotecas Python:

  * `base58`
  * `hashlib` (padrão)
  * `ecdsa`
  * `bit`

Instale as dependências com:

```bash
pip install base58 ecdsa bit
```

## Uso

Execute o script e informe o número do puzzle quando solicitado:

```bash
python seu_script.py
```

Exemplo de uso:

```
Digite o número do puzzle (ex: 68): 68

Intervalo do puzzle #68:
MIN = 0x8000000000000000
MAX = 0xffffffffffffffff

🔍 Iniciando busca direta no intervalo de 0x8000000000000000 a 0xffffffffffffffff...
▶️ Começando a busca a partir de: 0x8000000000000000
➡️ Progresso: 10000 chaves verificadas. Última privkey testada: 0x8000000000002710
...
```

O programa salvará o progresso automaticamente em `puzzle_<número>_progress.txt`.

## Estrutura do código

* `data_address`: Lista dos endereços Bitcoin alvo.
* Funções para calcular intervalos, salvar/carregar progresso.
* Função principal de busca com checkpointing.
* Entrada interativa para escolher o puzzle.

## Observações

* A busca pode levar muito tempo dependendo do intervalo.
* Progresso salvo permite pausar e retomar a busca.
* Certifique-se de ter espaço e permissão para criar arquivos de progresso no diretório.

## Licença

Projeto aberto para fins educacionais. Use por sua conta e risco. 
