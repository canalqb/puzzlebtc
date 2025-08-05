# 🔍 BTC Multiplicador Checker

Este projeto executa uma varredura matemática sobre múltiplos inteiros aplicados a potências de dois, buscando identificar chaves privadas válidas que resultem em **endereços Bitcoin conhecidos**.

Além de realizar a geração das chaves, o script verifica automaticamente esses endereços contra um **banco de dados local SQLite**, com objetivo de encontrar correspondências conhecidas, e, se alguma for encontrada, **salva e interrompe a execução imediatamente**.

---

## 🧠 Para que serve?

Este script foi idealizado para:

* 🧮 Explorar relações matemáticas entre inteiros, potências de 2 e múltiplos aplicados à geração de **chaves privadas Bitcoin**
* 🧠 Verificar se esses cálculos podem levar a **endereços já existentes**
* 🔐 Alertar imediatamente se **qualquer chave correspondente for encontrada**

---

## 📦 Funcionalidades principais

* 🧑‍💻 Geração automatizada de chaves privadas a partir de expressões com potências de 2 e múltiplos
* 🔄 Conversão para 3 tipos de endereços:

  * **Legacy (base58)**
  * **P2SH-P2WPKH**
  * **Bech32**
* 🗃️ Verificação em lote de endereços contra um banco SQLite
* 💾 Registro automático em `chave_encontrada.txt` se algum endereço conhecido for detectado
* 🧠 Cálculo com **alta precisão decimal** (precisão 1000)

---

## 🚀 Como usar

### 1. **Clone o repositório**

```bash
git clone https://github.com/canalqb/btc-multiplicador-checker.git
cd btc-multiplicador-checker
```

---

### 2. **Instale as dependências**

```bash
pip install bit bech32 psutil
```

---

### 3. **Configure o caminho do banco de dados**

Edite no topo do script:

```python
CAMINHO_BANCO = "banco.db"
```

> Este banco deve conter uma tabela chamada `enderecos` com uma coluna `address`.

---

### 4. **Execute o script**

```bash
python multiplicador_enderecos_validador.py
```

O script executará a varredura matemática e irá gerar os endereços correspondentes. Caso algum endereço esteja presente no banco de dados:

* O processo será interrompido
* A chave será salva em:

  ```
  chave_encontrada.txt
  ```

---

## 🧮 Como o cálculo funciona?

O algoritmo testa se a seguinte equação resulta em um número inteiro:

```
resultado = (X * m) / 256 / 2^n * 2
```

Se `resultado` for inteiro, este valor será usado como **chave privada**, e será convertida em formato **WIF**, e posteriormente transformada em **endereços públicos** Bitcoin.

O processo é feito para cada valor `X` no intervalo:

```
2^n até 2^(n+1) - 1
```

E para cada `m` em uma longa lista de múltiplos de potências de 2.

---

## 📁 Saída esperada

```bash
chave_encontrada.txt
```

> Será gerado apenas se um endereço conhecido for identificado.

---

## ⚠️ Avisos importantes

* **Uso educacional** apenas. Este script não deve ser utilizado com objetivos maliciosos.
* A busca por chaves privadas conhecidas em blockchains públicas **não é viável** na prática por força computacional.
* A verificação é puramente matemática e serve para **exploração e estudo** de possibilidades.

---

## 📬 Contato

Feito por [CanalQb no GitHub](https://github.com/canalqb)
Visite o blog: [canalqb.blogspot.com](https://canalqb.blogspot.com/)
💸 Apoie o projeto via Bitcoin:

```
13Ve1k5ivByaCQ5yer6GoV84wAtf3kNava
```

---

## 🧠 Licença

Este projeto está sob a licença **MIT**.
Sinta-se livre para usar, modificar e compartilhar.
