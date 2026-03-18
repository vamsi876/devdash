"""UUID v4/v7 and ULID generator."""

import re
import secrets
import sys
import time
import uuid

from devdash.tools.base import DevTool

_UUID_PATTERN = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.IGNORECASE
)

# ULID encoding alphabet (Crockford's Base32)
_ULID_ALPHABET = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"


def _generate_uuid_v7() -> str:
    """Generate UUID v7 (timestamp-based)."""
    if sys.version_info >= (3, 12):
        # Not available in stdlib until hypothetical future; use manual
        pass
    # Manual UUID v7 implementation
    timestamp_ms = int(time.time() * 1000)
    rand_bytes = secrets.token_bytes(10)

    # Build 16 bytes: 6 bytes timestamp + 2 bytes ver/rand + 8 bytes rand
    ts_bytes = timestamp_ms.to_bytes(6, "big")
    uuid_bytes = bytearray(16)
    uuid_bytes[0:6] = ts_bytes
    uuid_bytes[6:16] = rand_bytes

    # Set version (0111 = 7) in bits 48-51
    uuid_bytes[6] = (uuid_bytes[6] & 0x0F) | 0x70
    # Set variant (10xx) in bits 64-65
    uuid_bytes[8] = (uuid_bytes[8] & 0x3F) | 0x80

    hex_str = uuid_bytes.hex()
    return f"{hex_str[:8]}-{hex_str[8:12]}-{hex_str[12:16]}-{hex_str[16:20]}-{hex_str[20:]}"


def _generate_ulid() -> str:
    """Generate a ULID (Universally Unique Lexicographically Sortable Identifier)."""
    timestamp_ms = int(time.time() * 1000)
    rand_bytes = secrets.token_bytes(10)

    # Encode timestamp (48 bits) as 10 Crockford Base32 chars
    chars: list[str] = []
    t = timestamp_ms
    for _ in range(10):
        chars.append(_ULID_ALPHABET[t & 0x1F])
        t >>= 5
    time_part = "".join(reversed(chars))

    # Encode randomness (80 bits) as 16 Crockford Base32 chars
    rand_int = int.from_bytes(rand_bytes, "big")
    chars = []
    for _ in range(16):
        chars.append(_ULID_ALPHABET[rand_int & 0x1F])
        rand_int >>= 5
    rand_part = "".join(reversed(chars))

    return time_part + rand_part


class UuidTool(DevTool):
    @property
    def name(self) -> str:
        return "UUID / ULID Generator"

    @property
    def keyword(self) -> str:
        return "uuid"

    @property
    def category(self) -> str:
        return "Generators"

    @property
    def description(self) -> str:
        return "Enter 'v4', 'v7', or 'ulid' to generate. Paste a UUID to validate."

    def process(self, input_text: str, **kwargs: object) -> str:
        text = input_text.strip()

        # If input looks like a UUID, validate it
        if text and _UUID_PATTERN.match(text):
            try:
                parsed = uuid.UUID(text)
                return f"Valid UUID (version {parsed.version}): {parsed}"
            except ValueError:
                return "Invalid UUID format"

        version = str(kwargs.get("version", "v4"))
        count = int(kwargs.get("count", 1))
        uppercase = bool(kwargs.get("uppercase", False))
        count = max(1, min(count, 100))

        results: list[str] = []
        for _ in range(count):
            if version == "v7":
                val = _generate_uuid_v7()
            elif version == "ulid":
                val = _generate_ulid()
            else:
                val = str(uuid.uuid4())

            if uppercase:
                val = val.upper()
            else:
                val = val.lower()
            results.append(val)

        return "\n".join(results)


def register() -> DevTool:
    return UuidTool()
