# Algorithm notes

## Formatting contract

Caesar, Monoalphabetic, Vigenère, OTP, Rail Fence, and Columnar preserve all characters they do not transform. Playfair and Hill operate on normalized A–Z streams and therefore explicitly report formatting loss and padding/filler behavior.

## Columnar duplicates

Duplicate keyword letters are ordered by `(letter, original_index)`. That stable ordering is used for both encryption and decryption, so a key such as `BALLOON` is unambiguous.

## Hill invertibility

For 2×2 matrices, `det(K) = ad − bc` must have a modular inverse modulo 26. In practice `gcd(det(K), 26) = 1`. The API rejects matrices that cannot be inverted rather than returning misleading plaintext.
