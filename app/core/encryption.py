import base64
import binascii
import json
from typing import Any

from app.core.base import Encrypter
from app.models.config import EncryptionConfig


class Base64Encrypter(Encrypter):
    def __init__(self, config: EncryptionConfig) -> None:
        super().__init__(config)

    def encrypt(self, value: str) -> str:
        return base64.b64encode(value.encode()).decode()

    def decrypt(self, value: str) -> str:
        try:
            return base64.b64decode(value).decode()
        except binascii.Error:
            return value


...


class EncrypterFactory:
    encrypters: dict[str, type[Encrypter]] = {"base64": Base64Encrypter}

    @staticmethod
    def build(encryption_type: str, config: EncryptionConfig) -> Encrypter:
        return EncrypterFactory.encrypters[encryption_type](config)


...


class EncryptionService:
    def __init__(self, encrypter: Encrypter, config: EncryptionConfig) -> None:
        self._encrypter = encrypter
        self._config = config

    def encrypt(self, obj: dict[str, Any]) -> dict[str, str]:
        output: dict[str, str] = {}
        for key, value in obj.items():
            new_value = json.dumps(value, sort_keys=True)
            output[key] = f"data:{self._encrypter.encrypt(new_value)}"
        return output

    def decrypt(self, obj: dict[str, Any]) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for key, value in obj.items():
            if isinstance(value, str) and value.startswith("data:"):
                decrypted_value = self._encrypter.decrypt(value.split("data:")[1])
                try:
                    output[key] = json.loads(decrypted_value)
                except json.JSONDecodeError:
                    output[key] = decrypted_value
            else:
                output[key] = value
        return output
