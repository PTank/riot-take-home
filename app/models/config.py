from pydantic import BaseModel, SecretStr


class SigningConfig(BaseModel):
    secret_key: SecretStr


class EncryptionConfig(BaseModel): ...
