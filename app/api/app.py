from typing import Annotated, Any

from fastapi import Depends, FastAPI
from fastapi.responses import Response

from app.api.config import get_config
from app.core.encryption import EncrypterFactory, EncryptionService
from app.core.signing import SignerFactory, SigningService
from app.models import dto

app = FastAPI(title="egnima")


@app.get("/health", response_model=dto.HealthResponse)
async def health_check():
    return {"status": "OK", "service": "egnima"}


def get_encryption_service():
    config = get_config()
    return EncryptionService(
        EncrypterFactory.build(config.encryption_type, config.encryption),
        config.encryption,
    )


def get_signing_service():
    config = get_config()
    return SigningService(
        SignerFactory.build(config.signer_type, config.signing), config.signing
    )


@app.post(path="/encrypt")
async def encrypt(
    body: dict[str, Any],
    encryption_service: Annotated[EncryptionService, Depends(get_encryption_service)],
) -> dict[str, str]:
    return encryption_service.encrypt(body)


@app.post(path="/decrypt")
async def decrypt(
    body: dict[str, Any],
    encryption_service: Annotated[EncryptionService, Depends(get_encryption_service)],
) -> dict[str, Any]:
    return encryption_service.decrypt(body)


@app.post(path="/sign")
async def sign(
    body: dict[str, Any],
    signing_service: Annotated[SigningService, Depends(get_signing_service)],
) -> dto.SignResponse:
    return dto.SignResponse(signature=signing_service.sign(body))


@app.post(path="/verify", status_code=204)
async def verify(
    body: dto.VerifyPost,
    signing_service: Annotated[SigningService, Depends(get_signing_service)],
) -> Response:
    if not signing_service.verify(body.data, body.signature):
        return Response(status_code=400)
    return Response(status_code=204)
