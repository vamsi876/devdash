"""Tests for JwtTool - JWT decoder."""

import base64
import json
import time

import pytest

from devdash.tools.jwt_tool import JwtTool


@pytest.fixture
def tool() -> JwtTool:
    return JwtTool()


def _make_jwt(header: dict, payload: dict) -> str:
    """Build a fake JWT token from header and payload dicts."""
    h = base64.urlsafe_b64encode(json.dumps(header).encode()).rstrip(b"=").decode()
    p = base64.urlsafe_b64encode(json.dumps(payload).encode()).rstrip(b"=").decode()
    s = base64.urlsafe_b64encode(b"fakesignaturedata").rstrip(b"=").decode()
    return f"{h}.{p}.{s}"


class TestJwtToolProperties:
    def test_name(self, tool: JwtTool) -> None:
        assert tool.name == "JWT Decoder"

    def test_keyword(self, tool: JwtTool) -> None:
        assert tool.keyword == "jwt"

    def test_category(self, tool: JwtTool) -> None:
        assert tool.category == "Encoders / Decoders"


class TestJwtDecode:
    def test_decode_valid_jwt(self, tool: JwtTool, sample_jwt: str) -> None:
        result = tool.process(sample_jwt)
        assert "=== HEADER ===" in result
        assert "=== PAYLOAD ===" in result
        assert "HS256" in result
        assert "Test User" in result

    def test_decode_shows_header_fields(self, tool: JwtTool) -> None:
        token = _make_jwt(
            {"alg": "RS256", "typ": "JWT", "kid": "key-id-123"},
            {"sub": "user1"},
        )
        result = tool.process(token)
        assert "RS256" in result
        assert "key-id-123" in result

    def test_decode_shows_payload_fields(self, tool: JwtTool) -> None:
        token = _make_jwt(
            {"alg": "HS256", "typ": "JWT"},
            {"sub": "42", "role": "admin", "email": "test@example.com"},
        )
        result = tool.process(token)
        assert "admin" in result
        assert "test@example.com" in result

    def test_valid_token_not_expired(self, tool: JwtTool) -> None:
        future_exp = int(time.time()) + 7200
        token = _make_jwt(
            {"alg": "HS256", "typ": "JWT"},
            {"sub": "1", "exp": future_exp},
        )
        result = tool.process(token)
        assert "Valid (not expired)" in result

    def test_issued_at_displayed(self, tool: JwtTool) -> None:
        iat = int(time.time()) - 600
        token = _make_jwt(
            {"alg": "HS256", "typ": "JWT"},
            {"sub": "1", "iat": iat},
        )
        result = tool.process(token)
        assert "Issued At:" in result


class TestJwtExpired:
    def test_expired_jwt_detected(self, tool: JwtTool, sample_jwt_expired: str) -> None:
        result = tool.process(sample_jwt_expired)
        assert "EXPIRED" in result

    def test_recently_expired_jwt(self, tool: JwtTool) -> None:
        past_exp = int(time.time()) - 60
        token = _make_jwt(
            {"alg": "HS256", "typ": "JWT"},
            {"sub": "1", "exp": past_exp},
        )
        result = tool.process(token)
        assert "EXPIRED" in result
        assert "Expires At:" in result


class TestJwtNoExpiration:
    def test_no_expiration_field(self, tool: JwtTool) -> None:
        token = _make_jwt(
            {"alg": "HS256", "typ": "JWT"},
            {"sub": "1", "name": "No Expiry User"},
        )
        result = tool.process(token)
        assert "No expiration set" in result

    def test_no_expiration_no_expired_status(self, tool: JwtTool) -> None:
        token = _make_jwt(
            {"alg": "HS256", "typ": "JWT"},
            {"sub": "1"},
        )
        result = tool.process(token)
        assert "EXPIRED" not in result


class TestJwtErrorHandling:
    def test_empty_input(self, tool: JwtTool) -> None:
        result = tool.process("")
        assert "Error" in result
        assert "Empty input" in result

    def test_whitespace_only(self, tool: JwtTool) -> None:
        result = tool.process("   \n  ")
        assert "Error" in result

    def test_malformed_one_part(self, tool: JwtTool) -> None:
        result = tool.process("justonepart")
        assert "Error" in result
        assert "got 1" in result

    def test_malformed_two_parts(self, tool: JwtTool) -> None:
        result = tool.process("part1.part2")
        assert "Error" in result
        assert "got 2" in result

    def test_malformed_four_parts(self, tool: JwtTool) -> None:
        result = tool.process("a.b.c.d")
        assert "Error" in result
        assert "got 4" in result


class TestJwtSignatureWarning:
    def test_warning_present(self, tool: JwtTool, sample_jwt: str) -> None:
        result = tool.process(sample_jwt)
        assert "WARNING" in result
        assert "signature" in result.lower()

    def test_warning_mentions_decode_only(self, tool: JwtTool) -> None:
        token = _make_jwt(
            {"alg": "HS256", "typ": "JWT"},
            {"sub": "1"},
        )
        result = tool.process(token)
        assert "DECODES" in result
        assert "NOT verify" in result
