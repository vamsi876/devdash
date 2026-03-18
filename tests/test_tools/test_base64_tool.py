"""Tests for Base64Tool - Base64 encode/decode."""

import base64

import pytest

from devdash.tools.base64_tool import Base64Tool


@pytest.fixture
def tool() -> Base64Tool:
    return Base64Tool()


class TestBase64ToolProperties:
    def test_name(self, tool: Base64Tool) -> None:
        assert tool.name == "Base64 Encode / Decode"

    def test_keyword(self, tool: Base64Tool) -> None:
        assert tool.keyword == "base64"

    def test_category(self, tool: Base64Tool) -> None:
        assert tool.category == "Encoders / Decoders"


class TestBase64Encode:
    def test_encode_simple_string(self, tool: Base64Tool) -> None:
        result = tool.process("Hello World", mode="encode")
        assert "SGVsbG8gV29ybGQ=" in result

    def test_encode_includes_byte_counts(self, tool: Base64Tool) -> None:
        result = tool.process("Hello", mode="encode")
        assert "Original bytes: 5" in result
        assert "Encoded bytes:" in result

    def test_encode_empty_after_strip_is_error(self, tool: Base64Tool) -> None:
        result = tool.process("", mode="encode")
        assert "Error" in result

    def test_encode_unicode(self, tool: Base64Tool) -> None:
        result = tool.process("caf\u00e9", mode="encode")
        # Verify the encoded value is correct
        expected = base64.b64encode("caf\u00e9".encode("utf-8")).decode("ascii")
        assert expected in result


class TestBase64Decode:
    def test_decode_simple_string(self, tool: Base64Tool) -> None:
        result = tool.process("SGVsbG8gV29ybGQ=", mode="decode")
        assert "Hello World" in result

    def test_decode_includes_byte_counts(self, tool: Base64Tool) -> None:
        result = tool.process("SGVsbG8=", mode="decode")
        assert "Decoded bytes: 5" in result
        assert "Encoded bytes:" in result

    def test_decode_invalid_base64(self, tool: Base64Tool) -> None:
        result = tool.process("!!!not-base64!!!", mode="decode")
        assert "Error" in result

    def test_decode_sample_fixture(self, tool: Base64Tool, sample_base64: str) -> None:
        result = tool.process(sample_base64, mode="decode")
        assert "Hello World" in result


class TestBase64Roundtrip:
    def test_encode_then_decode(self, tool: Base64Tool) -> None:
        original = "The quick brown fox jumps over the lazy dog"
        encoded_result = tool.process(original, mode="encode")
        # Extract the encoded string (first line)
        encoded_str = encoded_result.split("\n")[0]
        decoded_result = tool.process(encoded_str, mode="decode")
        assert original in decoded_result

    def test_roundtrip_with_special_chars(self, tool: Base64Tool) -> None:
        original = "line1\nline2\ttab"
        encoded_result = tool.process(original, mode="encode")
        encoded_str = encoded_result.split("\n")[0]
        decoded_result = tool.process(encoded_str, mode="decode")
        assert original in decoded_result


class TestBase64AutoDetect:
    def test_auto_detects_base64_and_decodes(self, tool: Base64Tool) -> None:
        # "SGVsbG8gV29ybGQ=" is valid Base64 for "Hello World"
        result = tool.process("SGVsbG8gV29ybGQ=")
        assert "Auto-detected" in result
        assert "Hello World" in result

    def test_auto_encodes_plain_text(self, tool: Base64Tool) -> None:
        # Short text that does not look like base64
        result = tool.process("Hi!")
        # Should encode it (not auto-detect as base64)
        assert "Auto-detected" not in result
        expected_b64 = base64.b64encode(b"Hi!").decode("ascii")
        assert expected_b64 in result

    def test_auto_is_default_mode(self, tool: Base64Tool) -> None:
        # No mode kwarg should use auto
        result_auto = tool.process("SGVsbG8gV29ybGQ=", mode="auto")
        result_default = tool.process("SGVsbG8gV29ybGQ=")
        assert result_auto == result_default


class TestBase64UrlSafe:
    def test_url_safe_encode(self, tool: Base64Tool) -> None:
        # Data that would produce + or / in standard base64
        data = b"\xfb\xff\xfe"
        text = data.decode("latin-1")
        result = tool.process(text, mode="encode", url_safe=True)
        # URL-safe should not contain + or /
        encoded_line = result.split("\n")[0]
        assert "+" not in encoded_line
        assert "/" not in encoded_line

    def test_url_safe_decode(self, tool: Base64Tool) -> None:
        # URL-safe encoded "Hello World"
        encoded = base64.urlsafe_b64encode(b"Hello World").decode("ascii")
        result = tool.process(encoded, mode="decode", url_safe=True)
        assert "Hello World" in result


class TestBase64ErrorHandling:
    def test_empty_input(self, tool: Base64Tool) -> None:
        result = tool.process("")
        assert "Error" in result
        assert "Empty input" in result

    def test_whitespace_only(self, tool: Base64Tool) -> None:
        result = tool.process("   \n  ")
        assert "Error" in result

    def test_decode_non_utf8_gives_error(self, tool: Base64Tool) -> None:
        # Encode raw bytes that are not valid UTF-8
        raw = base64.b64encode(b"\xff\xfe\xfd\xfc").decode("ascii")
        result = tool.process(raw, mode="decode")
        assert "Error" in result
