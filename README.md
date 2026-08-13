# Puzzle Bitcoin (puzzlebtc)

Scripts para busca e resolução de puzzles Bitcoin (private keys em intervalos específicos).

## Visão Geral

Este repositório contém scripts para buscar chaves privadas Bitcoin dentro de intervalos específicos definidos pelos [puzzles Bitcoin](https://privatekeys.github.io/). Cada puzzle define um intervalo `[2^N, 2^(N+1)-1]` e a chave privada está dentro desse intervalo.

## Estrutura do Repositório

```
puzzlebtc/
├── Offline/                          # Scripts offline de geração e busca
│   ├── GeraBancos.py                 # Gera bancos SQLite com intervalos hex
│   ├── Puzzle.py                     # Busca direta usando bancos SQLite
│   ├── multiacionador.py             # Gerenciador multiprocesso de sessões
│   └── requirements.txt              # Dependências do módulo Offline
├── btc-from-bytes/                   # Geração de chaves a partir de bytes
│   ├── btc_keygen.py                 # Geração de chaves e endereços Bitcoin
│   ├── test_byte_to_btc.py           # Testes unitários
│   ├── setup.py                      # Setup do pacote
│   └── requirements.txt              # Dependências
├── btc-genetic-cracker/              # Cracker genético
│   └── btc_cracker.py                # Algoritmo genético (DEAP)
├── btc-genetic-finder/               # Busca genética
│   └── btc_bruteforce_ga.py          # Brute force genético
├── kangaroo_CanalQb/                 # Algoritmo Kangaroo
│   └── kangaroo_CanalQb.py           # Implementação do Kangaroo
├── btc-multiplicador-checker/        # Validador por múltiplos
│   └── multiplicador_enderecos_validador.py
├── ultra-bitcoin-utils/              # Utilitários otimizados
│   └── ultra_fast_bitcoin.py         # Geração ultra-rápida de chaves
├── btc-address-scanner/              # Scanner de endereços
│   └── gerador_chaves_validador.py   # Gerador e validador
├── bitcoin-private-key-scanner/      # Scanner avançado
│   ├── find_matching_bitcoin_address.py
│   └── find_matching_bitcoin_address2.py
├── bitcoin-wif-generator/            # Gerador WIF
│   └── generate_wif_keys.py
├── bitcoin_address_analyzer/         # Analisador de endereços
│   └── address_length_report.py
├── int-to-wif-converter/             # Conversor int -> WIF
│   └── convert_int_to_wif.py
├── interval-target-search/           # Busca por intervalo alvo
│   └── search_target.py
├── multi_base_key_converter/         # Conversor multi-base
│   └── gerar_chaves_multibase.py
├── log2-midpoint-estimator/          # Estimador log2
│   └── prever_meio_intervalo.py
├── btc_normalizer/                   # Normalizador BTC
│   └── normalizador_hex_proporcional.py
└── puzzle.txt                        # Lista de endereços alvo
```

## Requisitos

### Python 3.8+

### Dependências Principais

```bash
pip install ecdsa bit base58 bech32 psutil deap requests numpy
```

### Instalação por Módulo

```bash
# Módulo Offline
cd Offline && pip install -r requirements.txt

# Módulo btc-from-bytes
cd btc-from-bytes && pip install -r requirements.txt && pip install -e .
```

### Aceleração com ice_secp256k1.dll (Opcional)

Para aceleração de operações de multiplicação escalar, coloque a `ice_secp256k1.dll` em `C:\Users\Qb\Desktop\ola\` ou defina a variável de ambiente:

```bash
# Windows
set ICE_DLL_PATH=C:\Users\Qb\Desktop\ola\ice_secp256k1.dll

# Linux/Mac
export ICE_DLL_PATH=/c/Users/Qb/Desktop/ola/ice_secp256k1.dll
```

## Uso

### 1. Geração de Bancos de Dados (Offline)

Gera bancos SQLite com intervalos hexadecimais para busca distribuída:

```bash
cd Offline
python GeraBancos.py \
  --target 13zb1hQbWVsc2S7ZTZnP2G4undNNpdh5so \
  --start 0x2832ed74f2b5e25ee \
  --end 0x2832ed74f2b5e35ee \
  --parts 1000000000 \
  --batch 1000000 \
  --dbs 20
```

### 2. Busca com Kangaroo

```bash
cd kangaroo_CanalQb
python kangaroo_CanalQb.py --puzzle 68
python kangaroo_CanalQb.py --start 73786976294838206464 --end 147573952589676412927 --continue
```

### 3. Busca Direta (Puzzle.py)

```bash
cd Offline
python Puzzle.py -banco partes_hex_0.db
```

### 4. Gerenciador Multiprocesso

```bash
cd Offline
python multiacionador.py -num_sessoes 4
```

### 5. Converção int -> WIF

```bash
cd int-to-wif-converter
python convert_int_to_wif.py --range 66
python convert_int_to_wif.py --int 83
```

### 6. Análise Ultra-Rápida

```bash
cd ultra-bitcoin-utils
python ultra_fast_bitcoin.py --db /path/to/banco.db --n 20
```

### 7. Algoritmo Genético

```bash
cd btc-genetic-cracker
python btc_cracker.py --bits 64 --pop-size 500 --max-gen 1000
```

### 8. Busca Genética

```bash
cd btc-genetic-finder
python btc_bruteforce_ga.py --bits 71
```

## Integração com ice_secp256k1.dll

Scripts que suportam aceleração via DLL:
- `kangaroo_CanalQb/kangaroo_CanalQb.py` - Multiplicação escalar otimizada
- `ultra-bitcoin-utils/ultra_fast_bitcoin.py` - Geração de chaves públicas
- `Offline/Puzzle.py` - Derivação de endereços durante busca
- `int-to-wif-converter/convert_int_to_wif.py` - Carregamento da DLL

## Testes

```bash
cd btc-from-bytes
pip install pytest
pytest test_byte_to_btc.py -v
```

## Licença

MIT License - veja LICENSE para detalhes.

## Créditos

- Puzzles Bitcoin: [privatekeys.github.io](https://privatekeys.github.io/)
- ice_secp256k1.dll: Biblioteca nativa de aceleração secp256k1
- Autor: CanalQb ([@canalqb](https://github.com/canalqb))