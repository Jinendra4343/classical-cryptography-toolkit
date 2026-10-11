# Design and Development of a Classical Cryptography Toolkit

**Course:** Network Security · **Class:** ECM · **Academic year:** 2026–27

An educational full-stack toolkit implementing six substitution ciphers and two transposition ciphers with live explanations and measurements.

## What is included

- FastAPI backend with independently validated REST endpoints.
- React + TypeScript + Vite frontend with a responsive dark/light workspace.
- Caesar, Monoalphabetic, Playfair, Hill (2×2 and 3×3), Vigenère, One-Time Pad, Rail Fence, and Columnar Transposition.
- Live key squares, matrices, alphabet maps, repeating-key alignment, zigzag rows, and column grids.
- Text-file preview and download workflow (UTF-8, 1 MB limit).
- Session-only history that does not retain plaintext, ciphertext, or keys.
- Median repeated-run comparison measurements using `perf_counter_ns`.
- Pytest backend tests and Vitest/React Testing Library frontend test setup.
- Editable report, user manual, six-slide presentation content, video script, and samples.

## Requirements

- Python 3.10+
- Node.js 20+
- npm 10+

## Quick start

```bash
# terminal 1: API
cd backend
python -m venv .venv
source .venv/bin/activate                 # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# terminal 2: frontend
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`. The API documentation is available at `http://localhost:8000/docs`.

Single-command Docker setup: `docker compose up --build`.

Optional frontend API override:

```bash
VITE_API_URL=http://localhost:8000/api npm run dev
```

## Tests

```bash
cd backend
pytest -q

cd ../frontend
npm install
npm test
npm run build
```

Do not describe the project as fully tested unless these commands have been run successfully in the target environment. The report includes a blank results table for recording the verified run.

## API summary

| Method | Route | Purpose |
|---|---|---|
| GET | `/api/health` | Service health |
| GET | `/api/ciphers` | Cipher metadata and key hints |
| POST | `/api/keys/generate` | Generate a monoalphabetic or OTP key |
| POST | `/api/encrypt` | Encrypt JSON text |
| POST | `/api/decrypt` | Decrypt JSON text |
| POST | `/api/compare` | Median repeated-run comparison |
| POST | `/api/files/encrypt` | Encrypt a UTF-8 multipart text file |
| POST | `/api/files/decrypt` | Decrypt a UTF-8 multipart text file |

Request example: `{"algorithm":"caesar","text":"NETWORK SECURITY","key":"5"}`

## Normalization and security notes

- Caesar, Monoalphabetic, Vigenère, OTP, Rail Fence, and Columnar Transposition preserve formatting where their algorithm permits it.
- Playfair removes non-letters, merges J into I, prepares digraphs, and can retain filler X/Q after decryption.
- Hill removes non-letters, uppercases, and pads incomplete blocks with X.
- OTP keys must be exactly the normalized alphabetic input length. Keep a generated key separately and never reuse it.
- Classical ciphers are not suitable for confidential modern data. Use this project only for coursework and demonstrations.

## Project structure

```text
backend/app/ciphers/core.py       # pure algorithm engine
backend/app/api/routes.py         # validated FastAPI routes
backend/tests/                    # cipher and API tests
frontend/src/App.tsx              # dashboard pages and workflows
frontend/src/components/          # sidebar, panels, visualizations
docs/                             # report, manual, algorithm notes, demo script
samples/                          # sample plaintext and expected outputs
```
