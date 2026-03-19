"""Clipboard utilities with content type auto-detection."""

import json
import re
from enum import Enum, auto

import pyperclip


class ContentType(Enum):
    """Detected content types for clipboard auto-detection."""

    JWT = auto()
    JSON = auto()
    UUID = auto()
    CRON = auto()
    URL_ENCODED = auto()
    BASE64 = auto()
    UNIX_TIMESTAMP = auto()
    HEX_COLOR = auto()
    URL = auto()
    PLAIN_TEXT = auto()


_UUID_RE = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.IGNORECASE
)
_CRON_FIELD = r"[\d*,/\-LW#?]+"
_CRON_RE = re.compile(rf"^{_CRON_FIELD}(\s+{_CRON_FIELD}){{4,5}}$")
_URL_ENCODED_RE = re.compile(r"%[0-9A-Fa-f]{2}")
_BASE64_RE = re.compile(r"^[A-Za-z0-9+/\n\r]+=*$")
_HEX_COLOR_RE = re.compile(r"^#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$")


def read() -> str:
    """Get current clipboard content as string."""
    return pyperclip.paste()


def write(text: str) -> None:
    """Write string to clipboard."""
    pyperclip.copy(text)


def detect_type(text: str) -> ContentType:
    """Auto-detect content type with priority-based detection."""
    if not text or not text.strip():
        return ContentType.PLAIN_TEXT

    stripped = text.strip()

    # 1. JWT: starts with "eyJ" and has exactly 2 dots
    if stripped.startswith("eyJ") and stripped.count(".") == 2:
        return ContentType.JWT

    # 2. JSON: starts with { or [ and is valid JSON
    if stripped.startswith(("{", "[")):
        try:
            json.loads(stripped)
            return ContentType.JSON
        except (json.JSONDecodeError, ValueError):
            pass

    # 3. UUID: matches 8-4-4-4-12 hex pattern
    if _UUID_RE.match(stripped):
        return ContentType.UUID

    # 4. Cron: 5-6 space-separated fields
    if _CRON_RE.match(stripped):
        return ContentType.CRON

    # 5. URL-encoded: contains %XX patterns
    if _URL_ENCODED_RE.search(stripped) and " " not in stripped:
        return ContentType.URL_ENCODED

    # 6. Base64: matches charset and length multiple of 4
    if len(stripped) >= 4 and len(stripped) % 4 == 0 and _BASE64_RE.match(stripped):
        return ContentType.BASE64

    # 7. Unix timestamp: pure digits, 10 or 13 chars, reasonable range
    if stripped.isdigit() and len(stripped) in (10, 13):
        ts = int(stripped)
        if len(stripped) == 13:
            ts = ts // 1000
        # Reasonable range: 1970 to 2100
        if 0 <= ts <= 4102444800:
            return ContentType.UNIX_TIMESTAMP

    # 8. HEX color: starts with # + 3 or 6 hex chars
    if _HEX_COLOR_RE.match(stripped):
        return ContentType.HEX_COLOR

    # 9. URL: starts with http:// or https://
    if stripped.startswith(("http://", "https://")):
        return ContentType.URL

    # 10. Fallback
    return ContentType.PLAIN_TEXT
