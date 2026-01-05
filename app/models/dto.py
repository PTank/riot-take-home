from typing import Any

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    service: str


class VerifyPost(BaseModel):
    signature: str
    data: dict[str, Any]


class SignResponse(BaseModel):
    signature: str
