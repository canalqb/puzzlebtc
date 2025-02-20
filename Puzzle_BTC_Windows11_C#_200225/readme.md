# Instruções de Uso do Programa

## Passo 1: Preparação Inicial

### 1.1 Distribuição do Programa
- Envie o arquivo executável (EXE) ou o pacote compilado para os seus amigos.

### 1.2 Configuração do Arquivo de Configuração
- Envie o arquivo `config.txt` contendo o caminho e a visualização do processo.
- O arquivo `config.txt` é utilizado para configurar os parâmetros de execução do programa.

### 1.3 Configuração do Banco de Dados
- O arquivo `range.db` será gerado automaticamente quando o programa for executado pela primeira vez.
- Esse banco de dados contém as informações de intervalos e endereços gerados.

---

## Passo 2: Executando o Programa

### 2.1 Abrir o Aplicativo
- Dê um duplo clique no arquivo executável para iniciar o programa.

### 2.2 Entrada do Usuário
- Se necessário, forneça informações sobre o intervalo de pesquisa ou o endereço de destino. 

---

## Passo 3: Funcionalidade Principal

- O programa automaticamente dividirá o intervalo fornecido em partes menores, com um tamanho máximo de 30.000.000 por vez, e inserirá os dados no banco de dados SQLite.

---

## Passo 4: Gerar Endereço Bitcoin SV

- O programa gera endereços Bitcoin SV a partir de chaves privadas e valores hexadecimais.
- Ele gera os endereços conforme o intervalo da pesquisa configurado.

---

## Passo 5: Busca e Sorteio

- O programa seleciona um intervalo aleatório para gerar endereços e verifica se algum endereço corresponde à carteira alvo.
- Se encontrar um endereço correspondente, o programa gera um arquivo `[endereco].txt` contendo o endereço encontrado.

---

## Passo 6: Acompanhamento do Progresso

- O progresso da execução é exibido, incluindo informações sobre o grupo e o endereço enquanto o processo está em andamento.

---

## Passo 7: Atualização do Banco de Dados

- O banco PostgreSQL é atualizado com as informações sobre o processo de sorteio (se necessário).
- Após o processo de sorteio ser concluído, o programa exclui as entradas no banco SQLite.

---

## Passo 8: Encerramento do Programa

- Ao encontrar um endereço correspondente ou após terminar o processo de busca, o programa informa o resultado final e termina a execução.

---

## Passo 9: Gerenciamento de Erros

- O programa tenta reconectar automaticamente em caso de falha no banco de dados ou problemas de leitura.
- Ele também lida com erros de permissão e caminhos inválidos para os arquivos de entrada e saída.
