import io
import statistics
import time
from typing import Any

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import JSONResponse

from app.ciphers.core import CIPHERS, CipherError, execute_cipher, generate_key
from app.schemas.api import CipherRequest, CipherResponse, CompareRequest

router = APIRouter(prefix="/api")
MAX_FILE_BYTES = 1_000_000


def _process(request: CipherRequest, decrypt: bool) -> CipherResponse:
    started = time.perf_counter_ns()
    try:
        result, metadata = execute_cipher(request.algorithm, request.text, request.key, decrypt)
    except CipherError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    elapsed = (time.perf_counter_ns() - started) / 1_000_000
    return CipherResponse(
        result=result,
        algorithm=request.algorithm,
        operation="decrypt" if decrypt else "encrypt",
        elapsed_ms=round(elapsed, 5),
        input_length=len(request.text),
        output_length=len(result),
        normalized_length=sum(1 for char in request.text if char.isascii() and char.isalpha()),
        metadata=metadata,
    )


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "classical-crypto-toolkit"}


@router.get("/ciphers")
def ciphers() -> list[dict[str, Any]]:
    return CIPHERS


@router.post("/keys/generate")
def keys_generate(algorithm: str, text: str = "") -> dict[str, str]:
    try:
        return {"key": generate_key(algorithm, text)}
    except CipherError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/encrypt", response_model=CipherResponse)
def encrypt(request: CipherRequest) -> CipherResponse:
    return _process(request, False)


@router.post("/decrypt", response_model=CipherResponse)
def decrypt(request: CipherRequest) -> CipherResponse:
    return _process(request, True)


@router.post("/compare")
def compare(request: CompareRequest) -> dict[str, Any]:
    results: list[dict[str, Any]] = []
    for algorithm in dict.fromkeys(request.algorithms):
        key = request.keys.get(algorithm, "")
        if algorithm == "otp" and not key:
            try:
                key = generate_key("otp", request.text)
            except CipherError as exc:
                results.append({"algorithm": algorithm, "status": "error", "error": str(exc)})
                continue
        encryption_times: list[float] = []
        decryption_times: list[float] = []
        output_length = 0
        status = "ok"
        error = ""
        try:
            encrypted, metadata = execute_cipher(algorithm, request.text, key, False)
            for _ in range(request.runs):
                start = time.perf_counter_ns()
                execute_cipher(algorithm, request.text, key, False)
                encryption_times.append((time.perf_counter_ns() - start) / 1_000_000)
            for _ in range(request.runs):
                start = time.perf_counter_ns()
                execute_cipher(algorithm, encrypted, key, True)
                decryption_times.append((time.perf_counter_ns() - start) / 1_000_000)
            output_length = len(encrypted)
        except CipherError as exc:
            status, error = "error", str(exc)
            metadata = {}
        results.append({
            "algorithm": algorithm,
            "status": status,
            "error": error,
            "encrypt_ms": round(statistics.median(encryption_times), 5) if encryption_times else None,
            "decrypt_ms": round(statistics.median(decryption_times), 5) if decryption_times else None,
            "output_length": output_length,
            "metadata": metadata,
        })
    return {"results": results, "runs": request.runs, "note": "Median timings vary with hardware, runtime, and input length; speed is not cryptographic strength."}


async def _read_text_upload(upload: UploadFile) -> str:
    if upload.content_type not in ("text/plain", "application/octet-stream", None):
        raise HTTPException(status_code=415, detail="Only UTF-8 text files are supported.")
    data = await upload.read(MAX_FILE_BYTES + 1)
    if len(data) > MAX_FILE_BYTES:
        raise HTTPException(status_code=413, detail="File exceeds the 1 MB limit.")
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise HTTPException(status_code=422, detail="File must be valid UTF-8 text.") from exc


@router.post("/files/encrypt")
async def encrypt_file(file: UploadFile = File(...), algorithm: str = Form(...), key: str = Form("")) -> JSONResponse:
    text = await _read_text_upload(file)
    response = _process(CipherRequest(algorithm=algorithm, text=text, key=key), False)
    return JSONResponse({**response.model_dump(), "filename": f"{file.filename or 'output'}.encrypted.txt"})


@router.post("/files/decrypt")
async def decrypt_file(file: UploadFile = File(...), algorithm: str = Form(...), key: str = Form("")) -> JSONResponse:
    text = await _read_text_upload(file)
    response = _process(CipherRequest(algorithm=algorithm, text=text, key=key), True)
    return JSONResponse({**response.model_dump(), "filename": f"{file.filename or 'output'}.decrypted.txt"})
