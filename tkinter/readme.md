# 16x16 Address / Hash160 Generator ⚡

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Experimental-orange.svg)](LICENSE)

> Gerador de chaves Bitcoin com **grid 16x16**, mostrando bits ativados, gerando endereços P2PKH, WIF e HASH160, e verificando automaticamente contra alvos.

---

## 🔹 Demonstração Visual

O script exibe uma grid 16x16 que representa os bits da chave privada. Cada bit pode ter um estado diferente, indicado por cores:

| Cor         | Significado                       |
| ----------- | --------------------------------- |
| 🟩 Verde    | Bit ativo                         |
| ⬜ Cinza     | Bit inativo                       |
| 🟥 Vermelho | Match com `target.txt` encontrado |

### GIF do funcionamento

![Demo GIF](https://user-images.githubusercontent.com/yourusername/demo.gif)

---

## 🚀 Funcionalidades Interativas

| Botão / Controle | Descrição                                  |
| ---------------- | ------------------------------------------ |
| ▶ Iniciar        | Começa a geração de chaves                 |
| ⏸ Pausar         | Pausa o loop de geração                    |
| 🗑 Limpar        | Zera a grid 16x16                          |
| 🎲 Aleatorizar   | Ativa bits aleatórios (40%-60%)            |
| ↺ Reiniciar      | Reinicia a grid e contadores               |
| ⚡ Velocidade     | Ajusta tempo entre loops/mudança de coluna |

---

## 🛠️ O que o usuário pode fazer

1. **Gerar chaves**: Private Key HEX, WIF (comprimido/não comprimido), Endereço P2PKH, HASH160.
2. **Verificar alvos**: Automaticamente checa endereços/HASH160 contra `target.txt`.
3. **Salvar resultados**: Se houver match, um arquivo `<endereco>.txt` é criado e o log vai para `found_match.txt`.
4. **Visualizar bits**: Entenda como cada bit da chave está sendo definido na grid 16x16.
5. **Controlar loop**: Escolha entre sequência, aleatório ou loop infinito.
6. **Customizar velocidade**: Para ver ou acelerar a expansão da grid.

---

## ⚙️ Requisitos

* Python 3.8+
* Bibliotecas:

```bash
pip install ecdsa
```

* Tkinter (geralmente já incluso no Python)

---

## 📁 Estrutura de arquivos

```
16x16_rewritten.py      # Script principal
target.txt              # Endereços/HASH160 alvo
found_match.txt         # Histórico de matches
<enderecos>.txt         # Matches encontrados automaticamente
```

---

## 📝 Configuração do `target.txt`

Inclua **endereços P2PKH** ou **HASH160 hexadecimais**, um por linha:

```
1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa
5d41402abc4b2a76b9719d911017c592
```

---

## 💻 Como Usar

1. Configure `target.txt` com os alvos.
2. Execute o script:

```bash
python 16x16_rewritten.py
```

3. Explore a interface visual:

   * ▶ Iniciar / ⏸ Pausar geração
   * 🗑 Limpar grid
   * 🎲 Aleatorizar bits
   * ↺ Reiniciar grid 16x16
4. Ajuste a velocidade e os modos de geração (sequencial ou aleatório).
5. Quando um match é encontrado:

   * Alerta sonoro dispara
   * Arquivo `<endereco>.txt` é criado
   * Log detalhado salvo em `found_match.txt`

---

## ⚠️ Observações importantes

* **Segurança:** Apenas para uso educacional. Não use chaves com fundos reais.
* **Randomização:** Bits aleatórios (40%-60%)
* **Performance:** Loop infinito ou grid grande pode ser pesado no computador

---

## 📊 Detalhes técnicos

* **Criptografia:** `ecdsa` para gerar chave pública. HASH160 = RIPEMD160(SHA256(pubkey))
* **WIF:** Suporte a chaves comprimidas e não comprimidas
* **Randomização da grid:** Bits ativados coluna por coluna
* **Loop:** Configurável por milissegundos, parte da grid ou infinito

---

## 📝 Exemplo de saída

```
Private Key HEX: 1E99423A4ED27608A15A2616C8F2E42EBEFA44C47DF9BB55D8D26E0C3FBC8A17
WIF Comprimido: KwDiBf89QgGbjEhKnhXJuH7SUW1XwQj5tGVLV7JXp7pN7TGzj3s5
Endereço P2PKH: 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa
```
