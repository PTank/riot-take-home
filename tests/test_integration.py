from typing import Any

import pytest
from fastapi.testclient import TestClient
from pydantic import SecretStr

from app.api import config
from app.api.app import app


@pytest.fixture(autouse=True)
def patch_configuration(monkeypatch: pytest.MonkeyPatch) -> None:
    def get_config():
        return config.Config(
            signing=config.SigningConfig(secret_key=SecretStr("fake_token"))
        )

    monkeypatch.setattr(config, "get_config", get_config)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.mark.parametrize(
    "payload",
    [
        {
            "name": "John Doe",
            "age": 30,
            "contact": {"email": "john@example.com", "phone": "123-456-7890"},
        },
        {"message": "Hello World", "timestamp": 1616161616},
        {"simple": "value", "nested": {"key": "val"}},
    ],
)
def test_encrypt_decrypt(client: TestClient, payload: dict[str, Any]) -> None:
    # Encrypt
    encrypt_response = client.post("/encrypt", json=payload)
    assert encrypt_response.status_code == 200
    encrypted_data = encrypt_response.json()

    # Decrypt
    decrypt_response = client.post("/decrypt", json=encrypted_data)
    assert decrypt_response.status_code == 200
    decrypted_data = decrypt_response.json()

    assert decrypted_data == payload


@pytest.mark.parametrize(
    "payload,reordered_payload",
    [
        (
            {"message": "Hello World", "timestamp": 1616161616},
            {"timestamp": 1616161616, "message": "Hello World"},
        ),
        (
            {"simple": "value", "nested": {"key": "val"}},
            {"nested": {"key": "val"}, "simple": "value"},
        ),
    ],
)
def test_sign(
    client: TestClient, payload: dict[str, Any], reordered_payload: dict[str, Any]
) -> None:
    response = client.post("/sign", json=payload)

    assert response.status_code == 200
    result = response.json()

    response_reordered = client.post("/sign", json=reordered_payload)

    assert response_reordered.status_code == 200
    result_reordered = response_reordered.json()

    assert result["signature"] == result_reordered["signature"]


@pytest.mark.parametrize(
    "payload,tampered_payload,expected_status",
    [
        ({"message": "Hello World", "timestamp": 1616161616}, None, 204),
        ({"simple": "value", "nested": {"key": "val"}}, None, 204),
        (
            {"message": "Hello World", "timestamp": 1616161616},
            {"message": "Goodbye World", "timestamp": 1616161616},
            400,
        ),
        (
            {"simple": "value", "nested": {"key": "val"}},
            {"simple": "changed", "nested": {"key": "val"}},
            400,
        ),
    ],
)
def test_verify(
    client: TestClient,
    payload: dict[str, Any],
    tampered_payload: dict[str, Any] | None,
    expected_status: int,
) -> None:
    sign_response = client.post("/sign", json=payload)
    signature = sign_response.json()["signature"]

    verify_payload = {
        "signature": signature,
        "data": tampered_payload if tampered_payload else payload,
    }

    response = client.post("/verify", json=verify_payload)

    assert response.status_code == expected_status
