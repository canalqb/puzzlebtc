# README do Repositório PuzzleBTC

Bem-vindo ao repositório **PuzzleBTC**! Este projeto contém dois scripts principais que permitem a geração de partes de uma sequência hexadecimal e a busca de uma chave privada associada a um endereço Bitcoin. A seguir, você encontrará uma descrição de cada script, bem como instruções sobre como configurá-los e utilizá-los.

# Puzzle.exe: Junte-se ao Desafio!

[![Script em Modo Compartilhado - Prêmio Menor, Chance Maior](https://i.sstatic.net/Vp2cE.png)](https://youtu.be/sV80KE9Q5uU)

## Visão Geral

Bem-vindo ao **Puzzle.exe**, a ferramenta definitiva para resolver quebra-cabeças criptográficos! Este não é apenas um script; é um esforço colaborativo que potencializa suas chances de sucesso. Enquanto o script offline está disponível para todos, a verdadeira força do **Puzzle.exe** está na união—juntos, podemos alcançar muito mais!

## Por que Baixar o Puzzle.exe?

- **Esforço Colaborativo**: Cada participante contribui para a busca, permitindo que todos compartilhem o sucesso. Embora apenas uma pessoa receba o prêmio, a dedicação é coletiva!
  
- **Maior Eficiência**: Em vez de uma única pessoa analisando vastas faixas de dados sozinha, os participantes trabalham em paralelo, eliminando ranges vazias e acelerando o processo de descoberta.

- **Recompensas Reais**: Com o potencial de prêmios superiores a R$ 500.000 (em 22/09/2024), por que encarar esse desafio sozinho?

![Trabalhando Sozinho](https://blogger.googleusercontent.com/img/a/AVvXsEjN2PkLcH1Li7kbx6xg3kmFrsYhWKSn3INj3y04t0Q6OnXk9W8h1qatuHwzOSYOWNQjD-0kdWOm3aqXBvynU46iaYIczHGev5M55bi4CyfDLISGpx-JrZ0TaOvuuz_NkR_xlj9VL4UOYSebwCX-26RMJEKv_BOkwILhZ4NSRvBEkPH26UKBR-wT5tB_fGqE)

## Como Funciona

Imagine um código de barras onde cada linha vertical representa um bilhão de linhas de dados que precisam ser lidas sequencialmente. Fazer isso sozinho levaria uma eternidade.

![Trabalhando em Grupo](https://blogger.googleusercontent.com/img/a/AVvXsEgTd3rpRGej8UcO260bZS418qbi8MfA_4BKWl9P87yVA0l-B05q7AZk-Rn5ZkBXMt0mKKH8pko-n5uTNngk6ZCwK06iDRJM8C-eRx4HjPrTVtr40JOatTRZ3Rx4spTnnvquonW_clUlzd6h_dH9fNvCH1sqcl_95LL2VV8r1sKODucFGtcs5Q5ZaNSQe0Fd)

No nosso modelo colaborativo, os usuários são representados como pequenos quadrados, cada um encarregado de eliminar ranges vazias. Ninguém trabalhará na mesma faixa ao mesmo tempo, garantindo que a busca seja rápida e eficaz.

Quanto mais pessoas aceitarem o desafio de colaborar, menos esforço e tempo cada usuário precisará investir, e mais rápido o grande prêmio será revelado!

Assim que o prêmio for descoberto, eu, Rodrigo do CanalQb, serei notificado e o pagamento de 20% da carteira que está minerando será realizado. 

## Participe Hoje Mesmo!

Ao unir forças, você não apenas aumenta suas chances de ganhar, mas também se torna parte de um esforço comunitário. Lembre-se, há mais de 84 quebra-cabeças para resolver, e à medida que mais pessoas abraçam o trabalho em equipe, nossa ferramenta se torna cada vez mais essencial para descobrir as WIFs dos puzzles.

Não perca a chance de fazer parte de algo maior—baixe o **Puzzle.exe** e comece a colaborar hoje mesmo!

---

Para mais informações, confira nosso [canal no YouTube](https://youtu.be/sV80KE9Q5uU) e prepare-se para embarcar nesta jornada emocionante!

Boa sorte nos puzzles!

## Scripts

### 1. GeraBancos.py

Este script é responsável por criar bancos de dados SQLite que armazenam partes de uma sequência hexadecimal. 

#### Funções principais:
- **criar_tabelas(conn)**: Cria as tabelas necessárias no banco de dados, caso não existam.
- **dividir_sequencia_hex(inicial_hex, final_hex, n)**: Divide uma sequência hexadecimal em `n` partes e calcula o intervalo entre elas.
- **salvar_em_db(partes, conn)**: Salva as partes geradas na tabela `partes` do banco de dados.
- **ler_ultimo_indice(conn, inicial, intervalo)**: Lê o último índice processado e retorna seu valor.
- **gerar_e_salvar_partes_hex(inicial_hex, final_hex, n, target_btc, batch_size)**: Função principal que gera as partes da sequência hexadecimal e as salva em bancos de dados separados.

#### Exemplo de uso:
### Valores referentes ao range do 66 descoberto no dia 14/09/2024. Após executar o script, note que um arquivo .txt será criado na sua pasta.
```python
# Valores exemplo
target_btc = '13zb1hQbWVsc2S7ZTZnP2G4undNNpdh5so'
inicial_hex = "0x2832ed74f2b5e25ee"
final_hex = "0x2832ed74f2b5e35ee"
n = 10**9  # número de partes
batch_size = 1000000
totaldebancos = 20

gerar_e_salvar_partes_hex(inicial_hex, final_hex, n, target_btc, batch_size)
```

### 2. Puzzle.py

O segundo script tem como objetivo encontrar uma chave privada correspondente a um endereço Bitcoin específico. Ele utiliza os dados armazenados no banco de dados criado pelo `GeraBancos.py`.

#### Funções principais:
- **criar_tabela_resultados(conn)**: Cria a tabela onde os resultados (chaves encontradas) serão armazenados.
- **private_key_to_wif(private_key_hex, compression='01')**: Converte uma chave privada em formato hexadecimal para o formato WIF.
- **salvar_progresso(conn, id_parte, valor1)**: Salva o progresso do processamento no banco de dados.
- **carregar_progresso(conn, id_parte)**: Carrega o progresso anterior de uma parte.
- **encontrar_chave_privada(conn, target_btc, args)**: A função principal que busca a chave privada correspondente ao endereço Bitcoin.

#### Exemplo de uso:
```bash
python Puzzle.py -banco partes_hex_0.db
```

### 3. multiacionador.py

Após criar os bancos com o **GeraBancos.py**, utilize o **multiacionador.py** para abrir um puzzle.py separado para cada banco. Lembre-se de que o sistema consome recursos do seu computador, por isso é recomendável usar uma máquina potente.

## Requisitos

Antes de executar os scripts, você precisa instalar as dependências listadas no arquivo `requirements.txt`. Para isso, execute o seguinte comando no terminal:

```bash
pip install -r requirements.txt
```

## Comentários e Log

Os scripts incluem comentários em suas funções e lógica, além de um sistema de logging que registra eventos e erros em um arquivo chamado `puzzledb.log`.

## Contribuições

Se você deseja contribuir com este projeto, sinta-se à vontade para fazer um fork do repositório e enviar um pull request. Todas as contribuições são bem-vindas!  

## Clonando o Repositório

Para clonar este repositório, utilize o seguinte comando:

```bash
git clone https://github.com/seuusuario/seurepositorio.git

