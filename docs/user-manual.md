# User Manual

## Start

Run the backend and frontend commands in the root `README.md`, then open `http://localhost:5173`.

## Encrypt or decrypt text

1. Open **Encrypt & decrypt**.
2. Select an algorithm and read its key hint.
3. Enter text and key. Use **Example** for a known sample.
4. Choose **Encrypt** or **Decrypt**.
5. Copy or save the result. Read the normalization note beneath the editor.

The visualizer updates only from returned API metadata. It is not a hardcoded illustration.

## Keys

- Caesar: integer 0–25.
- Monoalphabetic: a permutation containing every A–Z letter once; Generate creates one.
- Playfair / Vigenère / Columnar: alphabetic keyword.
- Hill: four or nine letters/numbers; the matrix must be invertible modulo 26.
- OTP: Generate creates an exact-length secure key for the current normalized input. Copy it and never reuse it.
- Rail Fence: integer rails ≥ 2.

## Files

Open **File operations**, select a UTF-8 `.txt` file up to 1 MB, preview it, provide the same key used for encryption or decryption, then download the result. The server does not persist uploaded files.

## Compare

Open **Compare algorithms**, select compatible algorithms, provide keys, and run the median 15-run measurement. The result is a runtime observation only and must not be interpreted as cryptographic strength.

## History and privacy

History is held in browser memory for the current session. It stores timestamp, cipher, operation, lengths, duration, and status—not plaintext, ciphertext, or keys. Use **Clear history** to remove it.

## Common errors

- Empty input: provide at least one character.
- Hill matrix error: choose a determinant coprime with 26.
- OTP key length: count alphabetic characters only; key length must match exactly.
- Playfair odd ciphertext: decryption requires prepared even-length digraphs.
- Unicode: only ASCII A–Z participates in alphabetic transformations; non-ASCII characters are preserved by formatting-preserving ciphers and ignored by normalized ciphers.
