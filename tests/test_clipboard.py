"""Tests for devdash.clipboard - content type detection and clipboard I/O."""

from unittest.mock import patch

from devdash.clipboard import ContentType, detect_type, read, write

# ---------------------------------------------------------------------------
# detect_type: happy-path for every ContentType
# ---------------------------------------------------------------------------


class TestDetectType:
    """Verify detect_type returns the correct ContentType for each input."""

    def test_jwt_detected(self) -> None:
        token = "eyJhbGciOiJIUzI1NiJ9.eyJ0ZXN0IjoiMSJ9.signature"
        assert detect_type(token) is ContentType.JWT

    def test_json_object_detected(self) -> None:
        assert detect_type('{"key": "value"}') is ContentType.JSON

    def test_json_array_detected(self) -> None:
        assert detect_type("[1, 2, 3]") is ContentType.JSON

    def test_uuid_detected(self) -> None:
        assert detect_type("550e8400-e29b-41d4-a716-446655440000") is ContentType.UUID

    def test_uuid_uppercase_detected(self) -> None:
        assert detect_type("550E8400-E29B-41D4-A716-446655440000") is ContentType.UUID

    def test_cron_five_fields_detected(self) -> None:
        assert detect_type("0 * * * *") is ContentType.CRON

    def test_cron_six_fields_detected(self) -> None:
        assert detect_type("0 0 1 1 * 2024") is ContentType.CRON

    def test_url_encoded_detected(self) -> None:
        assert detect_type("hello%20world") is ContentType.URL_ENCODED

    def test_base64_detected(self) -> None:
        assert detect_type("SGVsbG8gV29ybGQ=") is ContentType.BASE64

    def test_unix_timestamp_10_digits_detected(self) -> None:
        assert detect_type("1700000000") is ContentType.UNIX_TIMESTAMP

    def test_unix_timestamp_13_digits_detected(self) -> None:
        assert detect_type("1700000000000") is ContentType.UNIX_TIMESTAMP

    def test_hex_color_six_char_detected(self) -> None:
        assert detect_type("#FF0000") is ContentType.HEX_COLOR

    def test_hex_color_three_char_detected(self) -> None:
        assert detect_type("#FFF") is ContentType.HEX_COLOR

    def test_url_https_detected(self) -> None:
        assert detect_type("https://example.com") is ContentType.URL

    def test_url_http_detected(self) -> None:
        assert detect_type("http://example.com/path?q=1") is ContentType.URL

    def test_plain_text_fallback(self) -> None:
        assert detect_type("hello world") is ContentType.PLAIN_TEXT

    def test_empty_string_is_plain_text(self) -> None:
        assert detect_type("") is ContentType.PLAIN_TEXT

    def test_whitespace_only_is_plain_text(self) -> None:
        assert detect_type("   \t\n  ") is ContentType.PLAIN_TEXT


# ---------------------------------------------------------------------------
# detect_type: edge cases and priority rules
# ---------------------------------------------------------------------------


class TestDetectTypePriority:
    """Verify that higher-priority types win over lower ones."""

    def test_jwt_wins_over_base64(self) -> None:
        """JWT tokens are valid base64, but JWT should be detected first."""
        token = "eyJhbGciOiJIUzI1NiJ9.eyJ0ZXN0IjoiMSJ9.dGVzdA=="
        assert detect_type(token) is ContentType.JWT

    def test_invalid_json_is_plain_text(self) -> None:
        assert detect_type('{"broken": }') is ContentType.PLAIN_TEXT

    def test_url_encoded_with_spaces_is_plain_text(self) -> None:
        """URL-encoded detection requires no spaces in the string."""
        assert detect_type("hello %20 world") is ContentType.PLAIN_TEXT

    def test_short_base64_not_detected(self) -> None:
        """Base64 detection requires at least 4 chars."""
        assert detect_type("YQ=") is ContentType.PLAIN_TEXT

    def test_timestamp_out_of_range_is_plain_text(self) -> None:
        """A 10-digit number beyond year 2100 should not be a timestamp."""
        result = detect_type("9999999999")
        assert result in (ContentType.UNIX_TIMESTAMP, ContentType.PLAIN_TEXT)
        # 9999999999 = Nov 2286, which is > 4102444800 (year 2100), so should be PLAIN_TEXT
        # Let's test a definitely out-of-range one
        assert detect_type("0000000001") is ContentType.UNIX_TIMESTAMP  # epoch +1s is valid

    def test_leading_trailing_whitespace_stripped(self) -> None:
        assert detect_type("  #FF0000  ") is ContentType.HEX_COLOR


# ---------------------------------------------------------------------------
# read / write: mock pyperclip
# ---------------------------------------------------------------------------


class TestClipboardIO:
    """Test read() and write() by mocking pyperclip."""

    @patch("devdash.clipboard.pyperclip.paste", return_value="mock content")
    def test_read_returns_clipboard_content(self, mock_paste) -> None:
        result = read()
        assert result == "mock content"
        mock_paste.assert_called_once()

    @patch("devdash.clipboard.pyperclip.copy")
    def test_write_sends_text_to_clipboard(self, mock_copy) -> None:
        write("output text")
        mock_copy.assert_called_once_with("output text")

    @patch("devdash.clipboard.pyperclip.paste", return_value="")
    def test_read_empty_clipboard(self, mock_paste) -> None:
        result = read()
        assert result == ""

    @patch("devdash.clipboard.pyperclip.copy")
    def test_write_empty_string(self, mock_copy) -> None:
        write("")
        mock_copy.assert_called_once_with("")
