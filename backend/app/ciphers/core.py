"""Pure-Python implementations of the eight required classical ciphers.

The functions intentionally keep the algorithms independent from HTTP concerns so
they can be used by the API, tests, and future command-line tools.
"""

from __future__ import annotations

import math
import secrets
import string
from collections import Counter
from typing import Any

ALPHABET = string.ascii_uppercase


class CipherError(ValueError):
    """Raised when a cipher cannot safely process the supplied input."""


def _letters(text: str) -> str:
    return "".join(char.upper() for char in text if char.isascii() and char.isalpha())


def _shift_char(char: str, shift: int) -> str:
    if not char.isascii() or not char.isalpha():
        return char
    base = ord("A") if char.isupper() else ord("a")
    return chr((ord(char) - base + shift) % 26 + base)


def caesar(text: str, key: str, decrypt: bool = False) -> tuple[str, dict[str, Any]]:
    try:
        shift = int(key)
    except (TypeError, ValueError) as exc:
        raise CipherError("Caesar shift must be an integer from 0 to 25.") from exc
    if not 0 <= shift <= 25:
        raise CipherError("Caesar shift must be between 0 and 25.")
    result = "".join(_shift_char(c, -shift if decrypt else shift) for c in text)
    return result, {"shift": shift, "normalization": "Preserves case, spaces, and punctuation."}


def _validate_substitution(key: str) -> str:
    normalized = key.upper().replace(" ", "")
    if len(normalized) != 26 or set(normalized) != set(ALPHABET):
        raise CipherError("Monoalphabetic key must contain each A-Z letter exactly once.")
    return normalized


def monoalphabetic(text: str, key: str, decrypt: bool = False) -> tuple[str, dict[str, Any]]:
    normalized = _validate_substitution(key)
    source = normalized if decrypt else ALPHABET
    target = ALPHABET if decrypt else normalized
    mapping = str.maketrans(source + source.lower(), target + target.lower())
    return text.translate(mapping), {"alphabet": normalized, "normalization": "Preserves case, spaces, and punctuation."}


def generate_mono_key() -> str:
    letters = list(ALPHABET)
    secrets.SystemRandom().shuffle(letters)
    return "".join(letters)


def _playfair_square(keyword: str) -> list[list[str]]:
    clean = _letters(keyword).replace("J", "I")
    if not clean:
        raise CipherError("Playfair keyword must contain at least one alphabetic character.")
    sequence: list[str] = []
    for char in clean + ALPHABET.replace("J", ""):
        if char not in sequence:
            sequence.append(char)
    return [sequence[index : index + 5] for index in range(0, 25, 5)]


def _playfair_pairs(text: str) -> list[tuple[str, str]]:
    clean = _letters(text).replace("J", "I")
    if not clean:
        raise CipherError("Playfair input must contain at least one alphabetic character.")
    pairs: list[tuple[str, str]] = []
    index = 0
    while index < len(clean):
        first = clean[index]
        if index + 1 >= len(clean):
            pairs.append((first, "X"))
            index += 1
        elif clean[index + 1] == first:
            # Q avoids an infinite-looking XX pair when the message itself has X.
            pairs.append((first, "Q" if first == "X" else "X"))
            index += 1
        else:
            pairs.append((first, clean[index + 1]))
            index += 2
    return pairs


def _playfair_transform(pair: tuple[str, str], square: list[list[str]], decrypt: bool) -> tuple[str, str]:
    positions = {char: (row, col) for row, line in enumerate(square) for col, char in enumerate(line)}
    a, b = pair
    row_a, col_a = positions[a]
    row_b, col_b = positions[b]
    step = -1 if decrypt else 1
    if row_a == row_b:
        return square[row_a][(col_a + step) % 5], square[row_b][(col_b + step) % 5]
    if col_a == col_b:
        return square[(row_a + step) % 5][col_a], square[(row_b + step) % 5][col_b]
    return square[row_a][col_b], square[row_b][col_a]


def playfair(text: str, key: str, decrypt: bool = False) -> tuple[str, dict[str, Any]]:
    square = _playfair_square(key)
    if decrypt:
        clean = _letters(text).replace("J", "I")
        if not clean or len(clean) % 2:
            raise CipherError("Playfair ciphertext must contain an even number of letters.")
        pairs = [(clean[i], clean[i + 1]) for i in range(0, len(clean), 2)]
    else:
        pairs = _playfair_pairs(text)
    result = "".join("".join(_playfair_transform(pair, square, decrypt)) for pair in pairs)
    return result, {
        "square": square,
        "pairs": ["".join(pair) for pair in pairs],
        "normalization": "Removes non-letters, merges J into I, and uses X/Q fillers for digrams.",
        "warning": "Decryption returns prepared digrams; filler characters may remain.",
    }


def _parse_hill_key(key: str) -> list[list[int]]:
    raw = key.strip()
    numeric = raw.replace(",", " ").split()
    if len(numeric) in (4, 9) and all(item.lstrip("-").isdigit() for item in numeric):
        values = [int(item) % 26 for item in numeric]
    else:
        letters = _letters(raw)
        if len(letters) not in (4, 9):
            raise CipherError("Hill key must be 4 or 9 numbers, or a 4/9-letter key.")
        values = [ord(char) - 65 for char in letters]
    size = int(math.sqrt(len(values)))
    return [values[i : i + size] for i in range(0, len(values), size)]


def _matrix_inverse(matrix: list[list[int]]) -> list[list[int]]:
    size = len(matrix)
    if size == 2:
        determinant = (matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]) % 26
        if math.gcd(determinant, 26) != 1:
            raise CipherError("Hill matrix determinant is not invertible modulo 26 (it must be coprime with 26).")
        inverse_det = pow(determinant, -1, 26)
        return [[matrix[1][1] * inverse_det % 26, -matrix[0][1] * inverse_det % 26],
                [-matrix[1][0] * inverse_det % 26, matrix[0][0] * inverse_det % 26]]
    # Gauss-Jordan over Z/26Z works here because every pivot chosen has an inverse.
    augmented = [[value % 26 for value in row] + [1 if i == j else 0 for j in range(size)] for i, row in enumerate(matrix)]
    for col in range(size):
        pivot = next((row for row in range(col, size) if math.gcd(augmented[row][col], 26) == 1), None)
        if pivot is None:
            raise CipherError("Hill matrix is not invertible modulo 26.")
        augmented[col], augmented[pivot] = augmented[pivot], augmented[col]
        scale = pow(augmented[col][col], -1, 26)
        augmented[col] = [(value * scale) % 26 for value in augmented[col]]
        for row in range(size):
            if row != col:
                factor = augmented[row][col]
                augmented[row] = [(a - factor * b) % 26 for a, b in zip(augmented[row], augmented[col])]
    return [row[size:] for row in augmented]


def hill(text: str, key: str, decrypt: bool = False) -> tuple[str, dict[str, Any]]:
    matrix = _parse_hill_key(key)
    size = len(matrix)
    inverse = _matrix_inverse(matrix)
    clean = _letters(text)
    if not clean:
        raise CipherError("Hill input must contain at least one alphabetic character.")
    if len(clean) % size:
        clean += "X" * (size - len(clean) % size)
    working = inverse if decrypt else matrix
    output: list[str] = []
    for start in range(0, len(clean), size):
        vector = [ord(char) - 65 for char in clean[start : start + size]]
        for row in working:
            output.append(chr(sum(a * b for a, b in zip(row, vector)) % 26 + 65))
    return "".join(output), {
        "matrix": matrix,
        "block_size": size,
        "normalization": f"Removes non-letters, uppercases, and pads to {size}-letter blocks with X.",
        "warning": "Padding X may remain after decryption.",
    }


def _keyword(key: str) -> str:
    normalized = _letters(key)
    if not normalized:
        raise CipherError("Key must contain at least one alphabetic character.")
    return normalized


def vigenere(text: str, key: str, decrypt: bool = False) -> tuple[str, dict[str, Any]]:
    keyword = _keyword(key)
    result: list[str] = []
    index = 0
    for char in text:
        if char.isascii() and char.isalpha():
            shift = ord(keyword[index % len(keyword)]) - 65
            result.append(_shift_char(char, -shift if decrypt else shift))
            index += 1
        else:
            result.append(char)
    alignment = ""
    key_index = 0
    for char in text:
        if char.isascii() and char.isalpha():
            alignment += keyword[key_index % len(keyword)]
            key_index += 1
        else:
            alignment += char
    return "".join(result), {"keyword": keyword, "alignment": alignment, "normalization": "Preserves case, spaces, and punctuation."}


def _otp_key(key: str, text: str) -> str:
    normalized = _letters(key)
    required = len(_letters(text))
    if required == 0:
        raise CipherError("One-Time Pad input must contain at least one alphabetic character.")
    if len(normalized) != required:
        raise CipherError(f"One-Time Pad key must contain exactly {required} alphabetic characters.")
    return normalized


def otp(text: str, key: str, decrypt: bool = False) -> tuple[str, dict[str, Any]]:
    normalized_key = _otp_key(key, text)
    result: list[str] = []
    index = 0
    for char in text:
        if char.isascii() and char.isalpha():
            shift = ord(normalized_key[index]) - 65
            result.append(_shift_char(char, -shift if decrypt else shift))
            index += 1
        else:
            result.append(char)
    return "".join(result), {"key_length": len(normalized_key), "normalization": "Preserves formatting while consuming key letters only for A-Z characters.", "warning": "Never reuse or persist a One-Time Pad key."}


def generate_otp_key(length: int) -> str:
    if length < 1 or length > 100_000:
        raise CipherError("OTP key length must be between 1 and 100,000.")
    return "".join(secrets.choice(ALPHABET) for _ in range(length))


def rail_fence(text: str, key: str, decrypt: bool = False) -> tuple[str, dict[str, Any]]:
    try:
        rails = int(key)
    except (TypeError, ValueError) as exc:
        raise CipherError("Rail Fence rail count must be an integer.") from exc
    if rails < 2:
        raise CipherError("Rail Fence requires at least 2 rails.")
    if len(text) < 2 or rails >= len(text):
        return text, {"rails": rails, "rows": [text], "normalization": "Preserves every character."}
    pattern = list(range(rails)) + list(range(rails - 2, 0, -1))
    if decrypt:
        rail_indices = [pattern[index % len(pattern)] for index in range(len(text))]
        counts = Counter(rail_indices)
        rows: dict[int, list[str]] = {}
        cursor = 0
        for rail in range(rails):
            rows[rail] = list(text[cursor : cursor + counts[rail]])
            cursor += counts[rail]
        offsets = Counter()
        restored: list[str] = []
        for rail in rail_indices:
            restored.append(rows[rail][offsets[rail]])
            offsets[rail] += 1
        result = "".join(restored)
    else:
        rows = [[] for _ in range(rails)]
        for index, char in enumerate(text):
            rows[pattern[index % len(pattern)]].append(char)
        result = "".join("".join(row) for row in rows)
    visual_rows = [[] for _ in range(rails)]
    for index, char in enumerate(text if not decrypt else result):
        visual_rows[pattern[index % len(pattern)]].append(char)
    return result, {"rails": rails, "rows": ["".join(row) for row in visual_rows], "normalization": "Preserves every character, including whitespace."}


def _column_order(keyword: str) -> list[int]:
    return sorted(range(len(keyword)), key=lambda index: (keyword[index], index))


def columnar(text: str, key: str, decrypt: bool = False) -> tuple[str, dict[str, Any]]:
    keyword = _keyword(key)
    columns = len(keyword)
    if not text:
        raise CipherError("Columnar input cannot be empty.")
    rows = math.ceil(len(text) / columns)
    lengths = [max(0, min(rows, len(text) - column * rows)) for column in range(columns)]
    # For encryption, the grid is row-major and the final row is left aligned.
    if not decrypt:
        grid = [text[row * columns : (row + 1) * columns] for row in range(rows)]
        result = "".join("".join(grid[row][column] for row in range(rows) if column < len(grid[row])) for column in _column_order(keyword))
        display = grid
    else:
        # Column lengths in a left-aligned ragged grid: early columns get the extra cells.
        base, extra = divmod(len(text), columns)
        actual_lengths = [base + (1 if column < extra else 0) for column in range(columns)]
        columns_data = [""] * columns
        cursor = 0
        for column in _column_order(keyword):
            columns_data[column] = text[cursor : cursor + actual_lengths[column]]
            cursor += actual_lengths[column]
        result = "".join(columns_data[column][row] for row in range(rows) for column in range(columns) if row < len(columns_data[column]))
        display = [result[row * columns : (row + 1) * columns] for row in range(rows)]
    return result, {"keyword": keyword, "order": _column_order(keyword), "grid": display, "normalization": "Preserves every character; the final row may be short."}


CIPHERS: list[dict[str, Any]] = [
    {"id": "caesar", "name": "Caesar", "category": "Substitution", "key_hint": "Integer shift, 0–25", "default_key": "5", "description": "A fixed rotation across the alphabet."},
    {"id": "monoalphabetic", "name": "Monoalphabetic", "category": "Substitution", "key_hint": "26-letter permutation", "default_key": "QWERTYUIOPASDFGHJKLZXCVBNM", "description": "A one-to-one replacement alphabet."},
    {"id": "playfair", "name": "Playfair", "category": "Substitution", "key_hint": "Alphabetic keyword", "default_key": "MONARCHY", "description": "Digraph substitution using a 5×5 square."},
    {"id": "hill", "name": "Hill", "category": "Substitution", "key_hint": "4/9 numbers or letters", "default_key": "HILL", "description": "Matrix multiplication modulo 26."},
    {"id": "vigenere", "name": "Vigenère", "category": "Substitution", "key_hint": "Alphabetic keyword", "default_key": "LEMON", "description": "Repeating-key Caesar shifts."},
    {"id": "otp", "name": "One-Time Pad", "category": "Substitution", "key_hint": "Exact normalized length", "default_key": "", "description": "Random, single-use additive key."},
    {"id": "rail-fence", "name": "Rail Fence", "category": "Transposition", "key_hint": "Number of rails", "default_key": "3", "description": "Zigzag writing across rails."},
    {"id": "columnar", "name": "Columnar Transposition", "category": "Transposition", "key_hint": "Alphabetic keyword", "default_key": "GERMAN", "description": "Read a row grid by sorted columns."},
]


def execute_cipher(cipher_id: str, text: str, key: str, decrypt: bool = False) -> tuple[str, dict[str, Any]]:
    if not isinstance(text, str) or not text:
        raise CipherError("Input text cannot be empty.")
    functions = {
        "caesar": caesar,
        "monoalphabetic": monoalphabetic,
        "playfair": playfair,
        "hill": hill,
        "vigenere": vigenere,
        "otp": otp,
        "rail-fence": rail_fence,
        "columnar": columnar,
    }
    if cipher_id not in functions:
        raise CipherError("Unknown cipher selected.")
    return functions[cipher_id](text, key, decrypt)


def generate_key(cipher_id: str, text: str = "") -> str:
    if cipher_id == "monoalphabetic":
        return generate_mono_key()
    if cipher_id == "otp":
        return generate_otp_key(max(1, len(_letters(text))))
    raise CipherError("This cipher does not have a generated key workflow.")
