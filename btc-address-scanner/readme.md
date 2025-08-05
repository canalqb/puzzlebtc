# 🔐 BTC Address Scanner & Key Generator

Este projeto é um **scanner de endereços Bitcoin** que **gera chaves privadas**, converte para **endereços públicos** em múltiplos formatos (*Legacy*, *P2SH-P2WPKH*, *Bech32*) e, opcionalmente, **verifica se esses endereços existem em um banco de dados local**.

---

## ⚙️ Funcionalidades

* 🔢 Geração matemática precisa de chaves privadas com base em valores decimais
* 🧠 Converte para múltiplos formatos de endereço:

  * `Legacy`
  * `P2SH-P2WPKH`
  * `Bech32`
* 📊 Salva os dados em arquivos `.csv`
* 🗃️ Consulta opcional a um banco de dados SQLite de endereços
* 🧼 Gerenciamento eficiente de memória com coleta de lixo (`gc.collect()`)

---

## 💡 Como funciona?

O script utiliza valores decimais como ponto de partida e aplica transformações matemáticas com múltiplos de potências de 2 para calcular possíveis **private keys**.

Cada chave gerada:

1. É convertida em formato WIF.
2. Gera os respectivos endereços públicos.
3. Pode ser consultada no banco de dados (se habilitado).
4. É salva em um arquivo `.csv`.

---

## 🚀 Como usar

### Pré-requisitos

> 📦 Bibliotecas necessárias:

```bash
pip install bit bech32 psutil
```

---

### 🧰 Passo a passo

1. **Clone o repositório**

   ```bash
   git clone https://github.com/canalqb/btc-address-scanner.git
   cd btc-address-scanner
   ```

2. **Edite o caminho do banco de dados SQLite**

   * No início do script, altere a variável `CAMINHO_BANCO` para apontar para seu arquivo `.db`.

3. **Execute o script**

   ```bash
   python gerador_chaves_validador.py
   ```

4. **Responda à pergunta:**

   > Deseja consultar no banco de dados durante o processo? (s/n)

5. **Espere os CSVs serem gerados**

   * Cada arquivo é nomeado conforme:

     ```
     chaves_wif_{indice_valor}_mult_{multiplo}.csv
     ```

6. **Chave encontrada?**

   * Se algum endereço gerado for encontrado no banco de dados, ele será salvo em:

     ```
     chave_encontrada.txt
     ```

---

## 🧠 Exemplo de entrada

```python
valores_str = [
   '0.000000000000113686837701',
   '0.000000000000113686837702',
   ...
]
```

---

## 📁 Estrutura esperada de saída

```
📁 btc-address-scanner
├── gerador_chaves_validador.py
├── chave_encontrada.txt  ← se alguma chave for encontrada
├── chaves_wif_0_mult_2.csv
├── chaves_wif_0_mult_4.csv
├── ...
```

Cada `.csv` contém:

| WIF       | Endereço    | PrivInt    |
| --------- | ----------- | ---------- |
| 5HueCG... | 1A1zP1eP... | 1234567890 |

---

## 🛡️ Segurança

⚠️ **Aviso**: Este script é apenas para fins educacionais. Nunca use chaves privadas geradas aleatoriamente com valores reais de Bitcoin. Utilize redes de teste (Testnet) se necessário.

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

Este projeto está licenciado sob a licença **MIT**. Sinta-se livre para estudar, modificar e compartilhar.

---
 
