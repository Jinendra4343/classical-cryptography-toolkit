# Mini-Project Report

## 1. Title Page

**Project:** Design and Development of a Classical Cryptography Toolkit  
**Course:** Network Security  
**Class:** ECM  
**Academic Year:** 2026–27  
**Student Name:** [Student Name]  
**Roll Number:** [Roll Number]  
**Batch:** [Batch]

## 2. Objectives

1. Implement eight classical encryption and decryption algorithms correctly.
2. Expose a modular, independently validated FastAPI service.
3. Build an accessible responsive workstation for exploring the algorithms.
4. Show intermediate structures so students can connect formulas to output.
5. Support text-file operations, measured comparisons, and session history without persisting secrets.

## 3. Problem Statement

Students often see classical ciphers as isolated formulas. This project provides a single educational environment where inputs, keys, normalization, intermediate structures, timing, and limitations can be inspected together. It must also reject malformed keys and explain formatting loss rather than presenting misleading output.

## 4. Software Requirements

- Python 3.10+, FastAPI, Pydantic, Uvicorn, Pytest.
- Node.js 20+, React, TypeScript, Vite, Framer Motion, Recharts, Lucide React.
- Modern browser with JavaScript enabled.
- No third-party cryptographic primitive is used; cipher logic is written with Python standard-library operations.

## 5. System Design (Flowchart)

```text
[Browser workspace]
       |
       | JSON / multipart REST
       v
[FastAPI routes + Pydantic validation]
       |
       v
[Pure cipher engine]
  |-- substitution: Caesar, Monoalphabetic, Playfair, Hill, Vigenère, OTP
  |-- transposition: Rail Fence, Columnar
       |
       v
[Structured result + metadata + measured duration]
```

No plaintext, ciphertext, or key is written to server logs or persistent history by default. CORS is restricted to the configured frontend origin.

## 6. Algorithms

### Substitution

- **Caesar:** `C = (P + k) mod 26`, preserving case and punctuation.
- **Monoalphabetic:** maps A–Z through a validated 26-letter permutation.
- **Playfair:** creates a 5×5 keyword square, combines I/J, and transforms digraphs by row, column, or rectangle rules.
- **Hill:** multiplies 2×2 or 3×3 blocks modulo 26. Decryption requires an invertible matrix; incomplete blocks use X padding.
- **Vigenère:** applies repeating-key Caesar shifts to letters only.
- **One-Time Pad:** adds a cryptographically secure random key modulo 26. Perfect secrecy requires random, secret, equal-length, single-use material.

### Transposition

- **Rail Fence:** writes characters along a zigzag and reads each rail.
- **Columnar Transposition:** writes rows under a keyword and reads stable sorted columns, preserving duplicate-letter order.

## 7. Program Modules

- `backend/app/ciphers/core.py` — testable algorithm and metadata engine.
- `backend/app/api/routes.py` — REST, comparison, key generation, and upload handling.
- `backend/app/schemas/api.py` — request and response validation.
- `frontend/src/App.tsx` — dashboard pages and stateful workflows.
- `frontend/src/components/Visualizations.tsx` — live educational views.
- `backend/tests/` — known examples, round trips, invalid keys, API, and files.

## 8. Sample Inputs and Outputs

| Cipher | Input | Key | Output |
|---|---|---|---|
| Caesar | `NETWORK SECURITY` | `5` | `SJYBTWP XJHZWNYD` |
| Playfair | `INSTRUMENTS` | `MONARCHY` | `GATLMZCLRQXA` |
| Hill | `HELP` | `3 3 2 5` | `HIAT` |
| Vigenère | `ATTACKATDAWN` | `LEMON` | `LXFOPVEFRNHR` |

See `samples/expected-outputs.json` for more examples.

## 9. Testing

The suite covers known outputs, encryption/decryption round trips, spaces and punctuation, Unicode behavior, invalid keys, Playfair repeated letters, Hill invertibility, OTP length, Rail Fence edges, duplicate Columnar keys, API status codes, and multipart files.

**Verified run record:** `pytest -q` — [record result after running in the deployment environment].

## 10. Results

The application produces actual algorithm output through the API and exposes measured operation durations. Comparison uses repeated runs and median values; timing is not presented as a strength ranking.

## 11. Applications

Network Security teaching, classroom demonstrations, algorithm labs, formula visualization, and introductory cryptography exercises.

## 12. Future Scope

Frequency analysis, Kasiski examination, configurable filler removal, secure modern primitives in a separate clearly labeled module, persistent instructor lesson plans, and 3D matrix walkthroughs.

## 13. Links

- Python documentation: https://docs.python.org/3/
- FastAPI documentation: https://fastapi.tiangolo.com/
- OWASP Cryptographic Storage guidance: https://cheatsheetseries.owasp.org/
