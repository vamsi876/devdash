"""Hash generator - MD5, SHA-1, SHA-256, SHA-512, BLAKE2b, HMAC."""

import hashlib
import hmac

from devdash.tools.base import DevTool

ALGORITHMS = ["md5", "sha1", "sha256", "sha512", "blake2b"]


class HashTool(DevTool):
    @property
    def name(self) -> str:
        return "Hash Generator"

    @property
    def keyword(self) -> str:
        return "hash"

    @property
    def category(self) -> str:
        return "Encoders / Decoders"

    @property
    def description(self) -> str:
        return "Enter text to generate MD5, SHA-256, and other hashes"

    def process(self, input_text: str, **kwargs: object) -> str:
        if not input_text.strip():
            return "Error: Empty input. Please provide text to hash."

        algorithm = str(kwargs.get("algorithm", "all"))
        hmac_key = kwargs.get("key")

        data = input_text.encode("utf-8")

        if hmac_key:
            return self._hmac_hash(data, str(hmac_key), algorithm)

        if algorithm != "all" and algorithm in ALGORITHMS:
            h = hashlib.new(algorithm, data)
            return f"{algorithm.upper()}: {h.hexdigest()}"

        lines: list[str] = []
        for algo in ALGORITHMS:
            h = hashlib.new(algo, data)
            lines.append(f"{algo.upper():>8}: {h.hexdigest()}")
        return "\n".join(lines)

    def _hmac_hash(self, data: bytes, key: str, algorithm: str) -> str:
        key_bytes = key.encode("utf-8")
        if algorithm == "all":
            algorithm = "sha256"
        if algorithm not in ALGORITHMS:
            return f"Error: Unknown algorithm '{algorithm}'. Use: {', '.join(ALGORITHMS)}"
        if algorithm == "blake2b":
            # HMAC doesn't support blake2b directly, use hashlib
            h = hmac.new(key_bytes, data, hashlib.sha256)
            return f"HMAC-SHA256 (blake2b not supported for HMAC): {h.hexdigest()}"
        h = hmac.new(key_bytes, data, algorithm)
        return f"HMAC-{algorithm.upper()}: {h.hexdigest()}"


def register() -> DevTool:
    return HashTool()
