import hmac
import json
from hashlib import sha256
from typing import Any

from app.core.base import Signer
from app.models.config import SigningConfig


class HMACSigner(Signer):
    def __init__(self, config: SigningConfig) -> None:
        super().__init__(config)

    def sign(self, value: str) -> str:
        return hmac.new(
            self._config.secret_key.get_secret_value().encode(),
            msg=value.encode(),
            digestmod=sha256,
        ).hexdigest()

    def verify(self, value: str, signature: str) -> bool:
        new_signature = self.sign(value)
        return new_signature == signature


class SignerFactory:
    signer: dict[str, type[Signer]] = {
        "hmac": HMACSigner,
    }

    @staticmethod
    def build(signer_type: str, config: SigningConfig) -> Signer:
        return SignerFactory.signer[signer_type](config)


class SigningService:
    def __init__(self, signer: Signer, config: SigningConfig) -> None:
        self._signer = signer
        self._config = config

    def sign(self, obj: dict[Any, Any]) -> str:
        obj_string: str = json.dumps(obj, sort_keys=True)
        return self._signer.sign(obj_string)

    def verify(self, obj: dict[Any, Any], signature: str) -> bool:
        return self._signer.verify(json.dumps(obj, sort_keys=True), signature)
