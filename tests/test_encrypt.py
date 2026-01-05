from typing import Any

import pytest

from app.core.encryption import EncrypterFactory, EncryptionService
from app.models.config import EncryptionConfig


@pytest.fixture
def encryption_config() -> EncryptionConfig:
    return EncryptionConfig()


@pytest.fixture
def encryption_service(encryption_config: EncryptionConfig) -> EncryptionService:
    return EncryptionService(
        EncrypterFactory.build("base64", encryption_config), encryption_config
    )


@pytest.mark.parametrize(
    "entry,expected",
    (
        ({"foo": "hello"}, {"foo": "data:ImhlbGxvIg=="}),
        (
            {"foo": {"bar": 2, "fuzz": "value"}},
            {"foo": "data:eyJiYXIiOiAyLCAiZnV6eiI6ICJ2YWx1ZSJ9"},
        ),
        (
            {"foo": {"fuzz": "value", "bar": 2}},
            {"foo": "data:eyJiYXIiOiAyLCAiZnV6eiI6ICJ2YWx1ZSJ9"},
        ),
    ),
)
def test_base64_encryption_service(
    entry: dict[str, Any],
    expected: dict[str, Any],
    encryption_service: EncryptionService,
) -> None:
    value = encryption_service.encrypt(entry)
    assert value == expected
    assert encryption_service.decrypt(value) == entry
