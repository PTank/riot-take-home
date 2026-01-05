from typing import Any

import pytest
from pydantic import SecretStr

from app.core.signing import SignerFactory, SigningService
from app.models.config import SigningConfig


@pytest.fixture
def token() -> SecretStr:
    return SecretStr("fake_token")


@pytest.fixture
def signing_config(token: SecretStr) -> SigningConfig:
    return SigningConfig(secret_key=token)


@pytest.fixture
def signing_service(signing_config: SigningConfig) -> SigningService:
    return SigningService(SignerFactory.build("hmac", signing_config), signing_config)


@pytest.mark.parametrize(
    "entry,expected",
    (
        (
            {"foo": "hello"},
            "41a0eebf985b2fdff36e6b4471a26e9b1b5ec6bc099ddcba14e04398236952c5",
        ),
        (
            {"foo": {"bar": 2, "fuzz": "value"}},
            "3ef62df35aabc59b154b25116f3f430d7aace45479f9b92097579360d6d9f3ee",
        ),
        (
            {"foo": {"fuzz": "value", "bar": 2}},
            "3ef62df35aabc59b154b25116f3f430d7aace45479f9b92097579360d6d9f3ee",
        ),
    ),
)
def test_hmac_signing_service(
    entry: dict[str, Any], expected: str, signing_service: SigningService
) -> None:
    signature = signing_service.sign(entry)
    assert signature == expected
    assert signing_service.verify(entry, expected)
