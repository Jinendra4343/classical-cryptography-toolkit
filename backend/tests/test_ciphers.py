import pytest

from app.ciphers.core import CipherError, execute_cipher, generate_mono_key, generate_otp_key


def test_caesar_known_example():
    result, _ = execute_cipher("caesar", "NETWORK SECURITY", "5")
    assert result == "SJYBTWP XJHZWNYD"


@pytest.mark.parametrize("algorithm,key,text", [
    ("caesar", "5", "Network Security!"),
    ("monoalphabetic", "QWERTYUIOPASDFGHJKLZXCVBNM", "Attack at Dawn!"),
    ("vigenere", "LEMON", "Network Security!"),
    ("otp", "XMCKLQWERT", "Hello World"),
    ("rail-fence", "3", "WE ARE DISCOVERED"),
    ("columnar", "GERMAN", "Network Security!"),
])
def test_round_trip(algorithm, key, text):
    encrypted, _ = execute_cipher(algorithm, text, key)
    decrypted, _ = execute_cipher(algorithm, encrypted, key, True)
    assert decrypted == text


def test_playfair_known_example_and_filler():
    encrypted, metadata = execute_cipher("playfair", "INSTRUMENTS", "MONARCHY")
    assert encrypted == "GATLMZCLRQXA"
    assert "square" in metadata


def test_hill_known_example():
    encrypted, _ = execute_cipher("hill", "HELP", "3 3 2 5")
    assert encrypted == "HIAT"


def test_hill_rejects_non_invertible_matrix():
    with pytest.raises(CipherError, match="not invertible"):
        execute_cipher("hill", "TEST", "2 4 2 4")


def test_key_validation_and_generation():
    with pytest.raises(CipherError):
        execute_cipher("monoalphabetic", "TEST", "SHORT")
    assert sorted(generate_mono_key()) == list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    assert len(generate_otp_key(17)) == 17


def test_otp_requires_exact_normalized_length():
    with pytest.raises(CipherError, match="exactly 9"):
        execute_cipher("otp", "PLAINTEXT", "SHORT")


def test_empty_and_unicode_behaviour():
    with pytest.raises(CipherError):
        execute_cipher("caesar", "", "5")
    result, _ = execute_cipher("caesar", "Café", "1")
    assert result == "Dbgé"


def test_playfair_repeated_letters_are_prepared():
    _, metadata = execute_cipher("playfair", "BALLOON", "KEYWORD")
    assert any(pair in metadata["pairs"] for pair in ("LX", "LO"))


def test_rail_fence_edge_cases():
    result, _ = execute_cipher("rail-fence", "A", "3")
    assert result == "A"
    with pytest.raises(CipherError):
        execute_cipher("rail-fence", "TEST", "1")


def test_columnar_duplicate_letters_are_stable():
    encrypted, metadata = execute_cipher("columnar", "WE ARE DISCOVERED", "BALLOON")
    assert metadata["order"] == sorted(range(7), key=lambda i: ("BALLOON"[i], i))
    decrypted, _ = execute_cipher("columnar", encrypted, "BALLOON", True)
    assert decrypted == "WE ARE DISCOVERED"
