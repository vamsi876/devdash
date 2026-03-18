"""JWT decoder - decode header and payload without verification."""

import json
from datetime import datetime, timezone

import jwt

from devdash.tools.base import DevTool


class JwtTool(DevTool):
    @property
    def name(self) -> str:
        return "JWT Decoder"

    @property
    def keyword(self) -> str:
        return "jwt"

    @property
    def category(self) -> str:
        return "Encoders / Decoders"

    @property
    def description(self) -> str:
        return "Decode JWT tokens (header + payload + expiry check)"

    def process(self, input_text: str, **kwargs: object) -> str:
        if not input_text.strip():
            return "Error: Empty input. Please provide a JWT token."

        token = input_text.strip()

        parts = token.split(".")
        if len(parts) != 3:
            return (
                "Error: Invalid JWT format. "
                f"Expected 3 parts (header.payload.signature), got {len(parts)}."
            )

        try:
            header = jwt.get_unverified_header(token)
        except jwt.exceptions.DecodeError as e:
            return f"Error: Could not decode JWT header: {e}"

        try:
            algorithms = [
                "HS256",
                "HS384",
                "HS512",
                "RS256",
                "RS384",
                "RS512",
                "ES256",
                "ES384",
                "ES512",
            ]
            payload = jwt.decode(token, options={"verify_signature": False}, algorithms=algorithms)
        except jwt.exceptions.DecodeError as e:
            return f"Error: Could not decode JWT payload: {e}"

        lines: list[str] = []
        lines.append("=== HEADER ===")
        lines.append(json.dumps(header, indent=2))
        lines.append("")
        lines.append("=== PAYLOAD ===")
        lines.append(json.dumps(payload, indent=2, default=str))

        # Expiration check
        exp = payload.get("exp")
        iat = payload.get("iat")
        now = datetime.now(timezone.utc)

        lines.append("")
        lines.append("=== TOKEN INFO ===")

        if iat:
            issued = datetime.fromtimestamp(iat, tz=timezone.utc)
            lines.append(f"Issued At:  {issued.isoformat()}")

        if exp:
            expiry = datetime.fromtimestamp(exp, tz=timezone.utc)
            is_expired = now > expiry
            lines.append(f"Expires At: {expiry.isoformat()}")
            status = "*** EXPIRED ***" if is_expired else "Valid (not expired)"
            lines.append(f"Status:     {status}")
        else:
            lines.append("Expires At: No expiration set")

        lines.append("")
        lines.append("WARNING: This tool only DECODES the token. It does NOT verify the signature.")

        return "\n".join(lines)


def register() -> DevTool:
    return JwtTool()
