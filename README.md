# README do Repositório PuzzleBTC

Bem-vindo ao repositório **PuzzleBTC**! Este projeto contém dois scripts principais que permitem a geração de partes de uma sequência hexadecimal e a busca de uma chave privada associada a um endereço Bitcoin. A seguir, você encontrará uma descrição de cada script, bem como instruções sobre como configurá-los e utilizá-los.

[![Script modo Compartilhado - premio menor, chance maior]([https://i.sstatic.net/Vp2cE.png](https://i9.ytimg.com/vi/sV80KE9Q5uU/mqdefault.jpg?v=66ee1b63&sqp=CNyJwbcG&rs=AOn4CLCXJmO1Ww3bccPft06tBV2EzfOHEg))](https://youtu.be/sV80KE9Q5uU)

O Script Offline, está aberto para todos (sua chance de tirar o maior valor do puzzle ainda não descoberto), tudo depende da sua maquina.
O Arquivo puzzle.exe tem a mesma condição do script.py, a melhoria é simples, apenas uma pessoa leva o premio, só que todos participam da busca.

[Sozinho](https://blogger.googleusercontent.com/img/a/AVvXsEjN2PkLcH1Li7kbx6xg3kmFrsYhWKSn3INj3y04t0Q6OnXk9W8h1qatuHwzOSYOWNQjD-0kdWOm3aqXBvynU46iaYIczHGev5M55bi4CyfDLISGpx-JrZ0TaOvuuz_NkR_xlj9VL4UOYSebwCX-26RMJEKv_BOkwILhZ4NSRvBEkPH26UKBR-wT5tB_fGqE)

![Sozinho](https://blogger.googleusercontent.com/img/a/AVvXsEjN2PkLcH1Li7kbx6xg3kmFrsYhWKSn3INj3y04t0Q6OnXk9W8h1qatuHwzOSYOWNQjD-0kdWOm3aqXBvynU46iaYIczHGev5M55bi4CyfDLISGpx-JrZ0TaOvuuz_NkR_xlj9VL4UOYSebwCX-26RMJEKv_BOkwILhZ4NSRvBEkPH26UKBR-wT5tB_fGqE)
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

