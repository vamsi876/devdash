"""Tests for HashTool - hash generator."""

import hashlib
import hmac

import pytest

from gadgetbox.tools.hash_tool import HashTool


@pytest.fixture
def tool() -> HashTool:
    return HashTool()


class TestHashToolProperties:
    def test_name(self, tool: HashTool) -> None:
        assert tool.name == "Hash Generator"

    def test_keyword(self, tool: HashTool) -> None:
        assert tool.keyword == "hash"

    def test_category(self, tool: HashTool) -> None:
        assert tool.category == "Encoders / Decoders"


class TestHashKnownValues:
    def test_sha256_of_hello(self, tool: HashTool) -> None:
        result = tool.process("hello", algorithm="sha256")
        expected = "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
        assert expected in result
        assert "SHA256" in result

    def test_md5_of_hello(self, tool: HashTool) -> None:
        result = tool.process("hello", algorithm="md5")
        expected = hashlib.md5(b"hello").hexdigest()
        assert expected in result
        assert "MD5" in result

    def test_sha1_of_hello(self, tool: HashTool) -> None:
        result = tool.process("hello", algorithm="sha1")
        expected = hashlib.sha1(b"hello").hexdigest()
        assert expected in result

    def test_sha512_of_hello(self, tool: HashTool) -> None:
        result = tool.process("hello", algorithm="sha512")
        expected = hashlib.sha512(b"hello").hexdigest()
        assert expected in result

    def test_blake2b_of_hello(self, tool: HashTool) -> None:
        result = tool.process("hello", algorithm="blake2b")
        expected = hashlib.blake2b(b"hello").hexdigest()
        assert expected in result


class TestHashAllAlgorithms:
    def test_all_algorithms_mode_produces_all(self, tool: HashTool) -> None:
        result = tool.process("test data")
        assert "MD5" in result
        assert "SHA1" in result
        assert "SHA256" in result
        assert "SHA512" in result
        assert "BLAKE2B" in result

    def test_all_algorithms_each_line_has_hash(self, tool: HashTool) -> None:
        result = tool.process("test data")
        lines = [line.strip() for line in result.strip().split("\n") if line.strip()]
        assert len(lines) == 5
        for line in lines:
            # Each line should have "ALGO: hexhash"
            assert ":" in line
            algo, hexhash = line.split(":", 1)
            assert len(hexhash.strip()) > 0

    def test_all_is_default_mode(self, tool: HashTool) -> None:
        explicit = tool.process("hello", algorithm="all")
        default = tool.process("hello")
        assert explicit == default


class TestHashSingleAlgorithm:
    @pytest.mark.parametrize("algo", ["md5", "sha1", "sha256", "sha512", "blake2b"])
    def test_single_algorithm_returns_one_line(self, tool: HashTool, algo: str) -> None:
        result = tool.process("test", algorithm=algo)
        assert "\n" not in result.strip()
        assert algo.upper() in result

    def test_unknown_algorithm_falls_back_to_all(self, tool: HashTool) -> None:
        # Unknown algorithm should trigger "all" path since it's not in ALGORITHMS
        result = tool.process("test", algorithm="unknown_algo")
        assert "MD5" in result
        assert "SHA256" in result


class TestHashHmac:
    def test_hmac_sha256_with_key(self, tool: HashTool) -> None:
        result = tool.process("hello", key="secret")
        expected = hmac.new(b"secret", b"hello", hashlib.sha256).hexdigest()
        assert expected in result
        assert "HMAC" in result

    def test_hmac_sha1_with_key(self, tool: HashTool) -> None:
        result = tool.process("hello", algorithm="sha1", key="mykey")
        expected = hmac.new(b"mykey", b"hello", "sha1").hexdigest()
        assert expected in result
        assert "HMAC-SHA1" in result

    def test_hmac_defaults_to_sha256_when_all(self, tool: HashTool) -> None:
        result = tool.process("hello", key="secret")
        assert "HMAC-SHA256" in result

    def test_hmac_blake2b_fallback(self, tool: HashTool) -> None:
        # blake2b is not supported for HMAC, should fallback
        result = tool.process("hello", algorithm="blake2b", key="secret")
        assert "blake2b not supported for HMAC" in result

    def test_hmac_unknown_algorithm(self, tool: HashTool) -> None:
        result = tool.process("hello", algorithm="fakealgo", key="secret")
        assert "Error" in result
        assert "Unknown algorithm" in result


class TestHashErrorHandling:
    def test_empty_input(self, tool: HashTool) -> None:
        result = tool.process("")
        assert "Error" in result
        assert "Empty input" in result

    def test_whitespace_only(self, tool: HashTool) -> None:
        result = tool.process("   \t\n  ")
        assert "Error" in result
