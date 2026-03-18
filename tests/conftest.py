"""Shared test fixtures for DevDash tests."""

import pytest


@pytest.fixture
def sample_json_valid() -> str:
    return '{"name": "test", "value": 42, "nested": {"key": "val"}}'


@pytest.fixture
def sample_json_invalid() -> str:
    return '{"name": "test", value: 42}'


@pytest.fixture
def sample_jwt() -> str:
    # A valid JWT structure (not cryptographically signed for real)
    import base64
    import json
    import time

    header = (
        base64.urlsafe_b64encode(json.dumps({"alg": "HS256", "typ": "JWT"}).encode())
        .rstrip(b"=")
        .decode()
    )
    payload = (
        base64.urlsafe_b64encode(
            json.dumps(
                {
                    "sub": "1234567890",
                    "name": "Test User",
                    "iat": int(time.time()) - 3600,
                    "exp": int(time.time()) + 3600,
                }
            ).encode()
        )
        .rstrip(b"=")
        .decode()
    )
    signature = base64.urlsafe_b64encode(b"fakesignature").rstrip(b"=").decode()
    return f"{header}.{payload}.{signature}"


@pytest.fixture
def sample_jwt_expired() -> str:
    import base64
    import json
    import time

    header = (
        base64.urlsafe_b64encode(json.dumps({"alg": "HS256", "typ": "JWT"}).encode())
        .rstrip(b"=")
        .decode()
    )
    payload = (
        base64.urlsafe_b64encode(
            json.dumps(
                {
                    "sub": "1234567890",
                    "exp": int(time.time()) - 3600,
                }
            ).encode()
        )
        .rstrip(b"=")
        .decode()
    )
    signature = base64.urlsafe_b64encode(b"fakesignature").rstrip(b"=").decode()
    return f"{header}.{payload}.{signature}"


@pytest.fixture
def sample_uuid() -> str:
    return "550e8400-e29b-41d4-a716-446655440000"


@pytest.fixture
def sample_base64() -> str:
    return "SGVsbG8gV29ybGQ="


@pytest.fixture
def sample_cron() -> str:
    return "0 9 * * 1-5"


@pytest.fixture
def sample_url() -> str:
    return "https://example.com/path?key=value&foo=bar#section"
