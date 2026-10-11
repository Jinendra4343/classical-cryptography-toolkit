import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router

app = FastAPI(title="Classical Cryptography Toolkit API", version="1.0.0")
origins = [origin.strip() for origin in os.getenv("FRONTEND_ORIGINS", "http://localhost:5173").split(",") if origin.strip()]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=False, allow_methods=["GET", "POST"], allow_headers=["*"])
app.include_router(router)


@app.get("/")
def root() -> dict[str, str]:
    return {"name": "Classical Cryptography Toolkit API", "docs": "/docs"}


@app.get("/health")
def health_alias() -> dict[str, str]:
    return {"status": "ok", "service": "classical-crypto-toolkit"}
