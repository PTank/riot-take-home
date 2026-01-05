from abc import ABC, abstractmethod

from app.models.config import EncryptionConfig, SigningConfig


class Encrypter(ABC):
    def __init__(self, config: EncryptionConfig) -> None:
        self._config = config

    @abstractmethod
    def encrypt(self, value: str) -> str:
        pass

    @abstractmethod
    def decrypt(self, value: str) -> str:
        pass


class Signer(ABC):
    def __init__(self, config: SigningConfig) -> None:
        self._config = config

    @abstractmethod
    def sign(self, value: str) -> str:
        pass

    @abstractmethod
    def verify(self, value: str, signature: str) -> bool:
        pass
