"""Base64 encode/decode tool."""

import base64
import re

from devdash.tools.base import DevTool

_BASE64_RE = re.compile(r"^[A-Za-z0-9+/\n\r]+=*$")
_BASE64_URLSAFE_RE = re.compile(r"^[A-Za-z0-9_\-\n\r]+=*$")


def _is_base64(text: str) -> bool:
    """Check if text looks like valid Base64."""
    cleaned = text.strip().replace("\n", "").replace("\r", "")
    if len(cleaned) < 4 or len(cleaned) % 4 != 0:
        return False
    return bool(_BASE64_RE.match(cleaned) or _BASE64_URLSAFE_RE.match(cleaned))


class Base64Tool(DevTool):
    @property
    def name(self) -> str:
        return "Base64 Encode / Decode"

    @property
    def keyword(self) -> str:
        return "base64"

    @property
    def category(self) -> str:
        return "Encoders / Decoders"

    @property
    def description(self) -> str:
        return "Encode or decode Base64 (standard and URL-safe)"

    def process(self, input_text: str, **kwargs: object) -> str:
        if not input_text.strip():
            return "Error: Empty input."

        mode = str(kwargs.get("mode", "auto"))
        url_safe = bool(kwargs.get("url_safe", False))

        if mode == "encode":
            return self._encode(input_text, url_safe)
        elif mode == "decode":
            return self._decode(input_text, url_safe)
        else:
            # Auto-detect: try decode if it looks like Base64
            if _is_base64(input_text.strip()):
                decoded = self._decode(input_text, url_safe)
                if not decoded.startswith("Error:"):
                    return f"[Auto-detected Base64 → Decoded]\n{decoded}\n\nBytes: {len(input_text.strip().encode())}"
            return self._encode(input_text, url_safe)

    def _encode(self, text: str, url_safe: bool) -> str:
        data = text.encode("utf-8")
        if url_safe:
            encoded = base64.urlsafe_b64encode(data).decode("ascii")
        else:
            encoded = base64.b64encode(data).decode("ascii")
        return f"{encoded}\n\nOriginal bytes: {len(data)}, Encoded bytes: {len(encoded)}"

    def _decode(self, text: str, url_safe: bool) -> str:
        cleaned = text.strip()
        try:
            if url_safe:
                decoded = base64.urlsafe_b64decode(cleaned)
            else:
                decoded = base64.b64decode(cleaned)
            return f"{decoded.decode('utf-8')}\n\nEncoded bytes: {len(cleaned)}, Decoded bytes: {len(decoded)}"
        except Exception as e:
            return f"Error: Could not decode Base64: {e}"


def register() -> DevTool:
    return Base64Tool()
