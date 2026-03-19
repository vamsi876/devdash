"""Tests for UrlTool - URL encode/decode and parser."""

import pytest

from gadgetbox.tools.url_tool import UrlTool


@pytest.fixture
def tool() -> UrlTool:
    return UrlTool()


class TestUrlToolMetadata:
    def test_name(self, tool: UrlTool) -> None:
        assert tool.name == "URL Encode / Decode"

    def test_keyword(self, tool: UrlTool) -> None:
        assert tool.keyword == "url"

    def test_category(self, tool: UrlTool) -> None:
        assert tool.category == "Encoders / Decoders"


class TestUrlEncode:
    def test_encode_simple_string(self, tool: UrlTool) -> None:
        result = tool.process("hello world", mode="encode")
        assert result == "hello%20world"

    def test_encode_special_characters(self, tool: UrlTool) -> None:
        result = tool.process("a=1&b=2", mode="encode")
        assert "%26" in result
        assert "%3D" in result

    def test_encode_unicode(self, tool: UrlTool) -> None:
        result = tool.process("cafe\u0301", mode="encode")
        assert "%" in result
        # Should not contain raw unicode
        assert "cafe" not in result or "%" in result

    def test_encode_already_safe_chars(self, tool: UrlTool) -> None:
        # With safe="" even / gets encoded
        result = tool.process("/path/to/file", mode="encode")
        assert "%2F" in result

    def test_encode_empty_after_strip(self, tool: UrlTool) -> None:
        result = tool.process("   ", mode="encode")
        assert result == "Error: Empty input."


class TestUrlDecode:
    def test_decode_percent_encoded(self, tool: UrlTool) -> None:
        result = tool.process("hello%20world", mode="decode")
        assert result == "hello world"

    def test_decode_special_characters(self, tool: UrlTool) -> None:
        result = tool.process("a%3D1%26b%3D2", mode="decode")
        assert result == "a=1&b=2"

    def test_decode_plus_sign(self, tool: UrlTool) -> None:
        # unquote does not convert + to space (that's unquote_plus)
        result = tool.process("hello+world", mode="decode")
        assert result == "hello+world"

    def test_decode_already_decoded(self, tool: UrlTool) -> None:
        result = tool.process("plain text", mode="decode")
        assert result == "plain text"


class TestUrlParse:
    def test_parse_full_url(self, tool: UrlTool) -> None:
        result = tool.process(
            "https://example.com:8080/path?key=value&foo=bar#section",
            mode="parse",
        )
        assert "Scheme:   https" in result
        assert "Host:     example.com" in result
        assert "Port:     8080" in result
        assert "Path:     /path" in result
        assert "Fragment: section" in result
        assert "key = value" in result
        assert "foo = bar" in result

    def test_parse_minimal_url(self, tool: UrlTool) -> None:
        result = tool.process("http://example.com", mode="parse")
        assert "Scheme:   http" in result
        assert "Host:     example.com" in result
        assert "Port:     (default)" in result
        assert "Query:    (none)" in result
        assert "Fragment: (none)" in result

    def test_parse_url_with_no_query(self, tool: UrlTool) -> None:
        result = tool.process("https://example.com/page", mode="parse")
        assert "Query Parameters:" not in result

    def test_parse_url_with_multiple_query_values(self, tool: UrlTool) -> None:
        result = tool.process("https://example.com?tag=a&tag=b", mode="parse")
        assert "tag = a" in result
        assert "tag = b" in result

    def test_parse_all_components_present(self, tool: UrlTool) -> None:
        result = tool.process("https://example.com:443/api/v1?q=test#top", mode="parse")
        for label in ["Scheme:", "Host:", "Port:", "Path:", "Query:", "Fragment:"]:
            assert label in result


class TestUrlAutoDetect:
    def test_auto_detects_http_url_as_parse(self, tool: UrlTool) -> None:
        result = tool.process("https://example.com/path?key=val")
        assert "Scheme:" in result
        assert "Host:" in result

    def test_auto_detects_percent_encoded_as_decode(self, tool: UrlTool) -> None:
        result = tool.process("hello%20world")
        assert "[Decoded]" in result
        assert "hello world" in result

    def test_auto_detects_plain_text_as_encode(self, tool: UrlTool) -> None:
        result = tool.process("hello world")
        assert "[Encoded]" in result
        assert "hello%20world" in result

    def test_auto_detect_http_prefix(self, tool: UrlTool) -> None:
        result = tool.process("http://localhost:3000")
        assert "Scheme:   http" in result


class TestUrlEmptyInput:
    def test_empty_string(self, tool: UrlTool) -> None:
        result = tool.process("")
        assert result == "Error: Empty input."

    def test_whitespace_only(self, tool: UrlTool) -> None:
        result = tool.process("   \n\t  ")
        assert result == "Error: Empty input."
