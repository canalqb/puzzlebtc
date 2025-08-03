import pytest
from byte2btc.byte_to_btc import (
    normalizar_array,
    calculate_entropy,
    private_key_to_wif_compressed
)

def test_normalizar_array():
    input_arr = [300, 0, 0]
    result = normalizar_array(input_arr.copy(), 3)
    assert all(0 <= b <= 255 for b in result)
    assert len(result) == 3

def test_entropy():
    byte_vector = [0, 255] * 16
    entropy_avg, entropy_total = calculate_entropy(byte_vector)
    assert entropy_avg > 0

def test_wif_format():
    private_key = bytes.fromhex('1E99423A4ED27608A15A2616EACE3561A64B4A20C9DCC0CFE8D0C1E6C6B5B92E')
    wif = private_key_to_wif_compressed(private_key)
    assert wif.startswith('L') or wif.startswith('K')
