# Six-slide project presentation

## Slide 1 — Title

**Design and Development of a Classical Cryptography Toolkit**  
Network Security · ECM · 2026–27  
Student: [Name] · Roll: [Number]

## Slide 2 — Need and objectives

- Make historical ciphers concrete through one interactive workstation.
- Validate keys on both frontend and backend.
- Explain normalization, filler characters, and invertibility.
- Provide comparison and text-file workflows without persisting secrets.

## Slide 3 — Eight algorithms

Caesar, Monoalphabetic, Playfair, Hill, Vigenère, One-Time Pad, Rail Fence, and Columnar Transposition. Group them as substitution versus transposition and show the live Playfair square / Hill matrix.

## Slide 4 — Architecture

Browser React + TypeScript client → JSON or multipart REST → FastAPI schemas and routes → pure Python cipher engine. The same engine is used by tests and UI operations.

## Slide 5 — Demonstration

1. Open Encrypt & decrypt.
2. Use Caesar with `NETWORK SECURITY` and shift `5`.
3. Show `SJYBTWP XJHZWNYD`, then decrypt.
4. Switch to Playfair `MONARCHY` and show the 5×5 square.
5. Run comparison and upload a UTF-8 sample file.

## Slide 6 — Results and limits

- Actual operations, measured timings, live visualization metadata, and session-only history.
- Classical ciphers are educational and breakable; speed is not security.
- Future: frequency analysis, Kasiski examination, and instructor lesson plans.
