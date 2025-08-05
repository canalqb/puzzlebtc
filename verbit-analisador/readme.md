---

# 🔍 Verbit — Analisador de Endereços Bitcoin por Bits Ativos

Este script faz a varredura de intervalos de chaves privadas Bitcoin com base no número de **bits ativos** (bits iguais a 1) na representação binária dos números, gera seus respectivos endereços em múltiplos formatos e verifica se algum deles existe em um banco de dados de endereços conhecidos.

---

## 🎯 Objetivo

A ideia central é explorar padrões matemáticos — especialmente números com **poucos bits ativos** — e investigar se algum endereço gerado a partir dessas chaves privadas já foi utilizado, o que pode indicar possíveis **fraquezas** na geração de chaves.

O script:

* Gera endereços Bitcoin (Legacy, P2SH-P2WPKH e Bech32) a partir de inteiros específicos.
* Conecta a um banco de dados SQLite contendo endereços Bitcoin conhecidos.
* Verifica se algum dos endereços gerados aparece no banco.
* Salva os resultados positivos no arquivo `verbit_chaves_encontradas.txt`.

---

## ⚙️ Requisitos

* Python 3.8 ou superior
* Bibliotecas Python necessárias:

  * `ecdsa`
  * `bit`
  * `psutil`
  * `base58`

Instale as dependências com:

```bash
pip install ecdsa bit psutil base58
```

---

## 🧪 Como usar

1. **Configure o caminho do banco de dados no script:**

   ```python
   CAMINHO_BANCO = "D:/Rodrigo/20052025/blockchair/banco.db"
   ```

   Certifique-se de que esse arquivo `.db` contenha a seguinte tabela:

   ```sql
   CREATE TABLE enderecos (
     address TEXT
   );
   ```

2. **Execute o script:**

   ```bash
   python verbit_checker.py
   ```

3. **Informe um valor para `n` quando solicitado:**

   O script analisará o intervalo de chaves de `2ⁿ` a `2ⁿ⁺¹ - 1`, agrupando os inteiros por quantidade de bits ativos.

---

## 📂 Saída

Se um endereço gerado for encontrado no banco, ele será salvo no arquivo:

```
verbit_chaves_encontradas.txt
```

Formato da saída:

```
WIF: [chave WIF] - End: [endereço encontrado] - PrivInt: [inteiro]
```

---

## 🛠 Recursos técnicos

* Geração de endereços Bitcoin nos formatos:

  * WIF (com e sem compressão)
  * Legacy (P2PKH)
  * P2SH-P2WPKH
  * Bech32 (P2WPKH)
* Redução automática da prioridade do processo para evitar sobrecarga do sistema.
* Consulta otimizada com uso de **lotes (batch)** no SQLite.
* Estratégia de varredura baseada em **bit density** (quantidade de bits 1 na chave).

---

## ⚠️ Aviso legal

> Este script é destinado exclusivamente a fins **educacionais** e de **pesquisa matemática/tecnológica**.

**Jamais use este código para tentar acessar fundos de terceiros.**
Isso é ilegal, imoral e viola princípios fundamentais de segurança e privacidade.

---

## 📬 Contato

Feito por [CanalQb no GitHub](https://github.com/canalqb)
Blog: [canalqb.blogspot.com](https://canalqb.blogspot.com/)
💸 Apoie a ideia (Bitcoin): `13Ve1k5ivByaCQ5yer6GoV84wAtf3kNava`

---

## 🧠 Curiosidade

> Você sabia?

A chance de encontrar uma chave privada válida em uso por **força bruta** é praticamente **nula**.
Este projeto explora padrões matemáticos em busca de **compreensão**, **curiosidade** e **educação**, não de exploração maliciosa.

---

## 📁 Nome da pasta sugerida

```
verbit-analisador
```

> "Verbit" vem da fusão de "verificação de bits" com "Bitcoin" — um nome curto e sugestivo.

---

## 🐍 Nome do script

```
verbit_checker.py
```

---

 
