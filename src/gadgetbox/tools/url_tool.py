"""URL encode/decode and parser."""

from urllib.parse import parse_qs, quote, unquote, urlparse

from gadgetbox.tools.base import DevTool


class UrlTool(DevTool):
    @property
    def name(self) -> str:
        return "URL Encode / Decode"

    @property
    def keyword(self) -> str:
        return "url"

    @property
    def category(self) -> str:
        return "Encoders / Decoders"

    @property
    def description(self) -> str:
        return "Paste a URL to parse, or enter text to URL-encode"

    def process(self, input_text: str, **kwargs: object) -> str:
        if not input_text.strip():
            return "Error: Empty input."

        text = input_text.strip()
        mode = str(kwargs.get("mode", "auto"))

        if mode == "encode":
            return self._encode(text)
        elif mode == "decode":
            return self._decode(text)
        elif mode == "parse":
            return self._parse(text)
        else:
            # Auto-detect
            if text.startswith(("http://", "https://")):
                return self._parse(text)
            if "%" in text:
                return f"[Decoded]\n{self._decode(text)}"
            return f"[Encoded]\n{self._encode(text)}"

    def _encode(self, text: str) -> str:
        return quote(text, safe="")

    def _decode(self, text: str) -> str:
        return unquote(text)

    def _parse(self, text: str) -> str:
        parsed = urlparse(text)
        params = parse_qs(parsed.query)

        lines = [
            f"Scheme:   {parsed.scheme or '(none)'}",
            f"Host:     {parsed.hostname or '(none)'}",
            f"Port:     {parsed.port or '(default)'}",
            f"Path:     {parsed.path or '/'}",
            f"Query:    {parsed.query or '(none)'}",
            f"Fragment: {parsed.fragment or '(none)'}",
        ]

        if params:
            lines.append("\nQuery Parameters:")
            for key, values in params.items():
                for val in values:
                    lines.append(f"  {key} = {val}")

        return "\n".join(lines)


def register() -> DevTool:
    return UrlTool()
