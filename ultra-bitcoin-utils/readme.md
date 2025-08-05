
### Sugestão de nomes:

* Nome da pasta: `ultra-bitcoin-utils`
* Nome do script: `ultra_fast_bitcoin.py`

---

### README.md já renderizado (como ficaria no GitHub)

---

# 🚀 Ultra Bitcoin Utils - Script Ultra-Otimizado

**Bem-vindo(a) ao Ultra Bitcoin Utils!**
Este script é uma ferramenta *ultra-rápida* e altamente otimizada para geração, análise e verificação de chaves privadas Bitcoin e seus endereços correspondentes. Ele foi desenvolvido para realizar varreduras eficientes em grandes intervalos de chaves privadas, possibilitando a busca por chaves específicas já existentes em um banco de dados local.

---

## 🎯 Para que serve este script?

O **Ultra Bitcoin Utils** tem como objetivo principal:

* Gerar chaves privadas no formato WIF (Wallet Import Format), com opção de gerar também os endereços Bitcoin *Legacy* e *Bech32* correspondentes.
* Realizar consultas ultra-rápidas em um banco de dados SQLite para verificar se algum endereço gerado já está registrado, indicando potenciais chaves "validadas".
* Permitir análises em batch (lotes) ou em loops sequenciais, com múltiplas threads/processos para maximizar a performance.
* Oferecer modos de operação que variam entre gerar apenas o WIF (modo rápido) ou gerar dados mínimos completos (WIF + endereços).
* Realizar benchmark para comparar performances dos modos de geração e análise.

---

## ⚙️ Como funciona?

Este script é dividido em etapas principais, todas focadas em **otimização extrema para alta performance**:

1. **Geração rápida de chaves privadas**:

   * Utiliza técnicas de cache para acelerar funções de hash (SHA256 + RIPEMD160).
   * Geração otimizada de chaves públicas comprimidas usando a biblioteca `ecdsa`.

2. **Criação e verificação de índices no banco de dados SQLite**:

   * Garante que as consultas de endereços sejam feitas com máxima velocidade por meio da criação de índices específicos.

3. **Consulta eficiente em lotes**:

   * Divisão das consultas em batches menores para contornar limitações do SQLite (máximo de 999 parâmetros por query).

4. **Paralelização**:

   * Usa múltiplos workers para distribuir a carga de trabalho e acelerar o processamento.

5. **Relatórios e logging**:

   * Chaves encontradas são registradas em arquivo separado com detalhes completos.

---

## 🚀 Principais funcionalidades

* **Modos de execução**:

  * **WIF apenas** (rápido)
  * **Dados mínimos** (WIF + endereços Legacy e Bech32)
  * **Loop sequencial ultra-rápido**
  * **Benchmark de performance**

* **Performance**:

  * Processa dezenas de milhares de chaves por segundo dependendo do hardware e configuração.

* **Compatibilidade**:

  * Utiliza bibliotecas padrão do Python + `ecdsa` e `bit`.

---

## 🔥 Passo a passo para usar

1. Clone este repositório:

   ```bash
   git clone https://github.com/canalqb/ultra-bitcoin-utils.git
   cd ultra-bitcoin-utils
   ```

2. Instale as dependências necessárias:

   ```bash
   pip install ecdsa bit base58
   ```

3. Prepare seu banco de dados SQLite contendo os endereços Bitcoin para consulta, e configure o caminho em `CAMINHO_BANCO` dentro do script.

4. Execute o script:

   ```bash
   python ultra_fast_bitcoin.py
   ```

5. Informe os parâmetros solicitados:

   * Valor de `n` para definir o intervalo de geração (exemplo: 20 a 30 recomendado).
   * Escolha o modo de operação.

6. Acompanhe o progresso no terminal. Se alguma chave for encontrada, ela será registrada no arquivo `verbit_chaves_encontradas.txt`.

---

## ⚠️ Avisos importantes

* A análise de grandes intervalos pode consumir muita memória e CPU. Ajuste o valor de `n` e o batch size conforme seu hardware.
* O banco de dados deve conter os endereços Bitcoin já conhecidos para que as consultas funcionem corretamente.
* Este script é fornecido para fins educacionais e de pesquisa. Use com responsabilidade e dentro da legislação aplicável.

---

## 📬 Contato

Feito por [CanalQb no GitHub](https://github.com/canalqb)
Visite o blog: [canalqb.blogspot.com](https://canalqb.blogspot.com/)
💸 Apoie o projeto via Bitcoin: `13Ve1k5ivByaCQ5yer6GoV84wAtf3kNava`
 
