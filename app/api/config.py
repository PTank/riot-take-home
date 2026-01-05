import secrets
from functools import lru_cache
from typing import Literal

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings

from app.models.config import EncryptionConfig, SigningConfig


class Config(BaseSettings):
    encryption_type: Literal["base64"] = "base64"
    signer_type: Literal["hmac"] = "hmac"

    signing: SigningConfig = Field(
        default_factory=lambda: SigningConfig(
            secret_key=SecretStr(secrets.token_urlsafe())
        )
    )
    encryption: EncryptionConfig = Field(default_factory=EncryptionConfig)


@lru_cache
def get_config():
    return Config()
