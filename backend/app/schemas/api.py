from typing import Any

from pydantic import BaseModel, Field


class CipherRequest(BaseModel):
    algorithm: str
    text: str = Field(min_length=1, max_length=200_000)
    key: str = Field(default="", max_length=100_000)


class CipherResponse(BaseModel):
    result: str
    algorithm: str
    operation: str
    elapsed_ms: float
    input_length: int
    output_length: int
    normalized_length: int
    metadata: dict[str, Any] = {}


class CompareRequest(BaseModel):
    text: str = Field(min_length=1, max_length=100_000)
    algorithms: list[str] = Field(min_length=1, max_length=8)
    keys: dict[str, str] = {}
    runs: int = Field(default=15, ge=3, le=50)
