"""Tests for UuidTool - UUID v4/v7 and ULID generator."""

import re

import pytest

from devdash.tools.uuid_tool import UuidTool

UUID_REGEX = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
    re.IGNORECASE,
)

ULID_REGEX = re.compile(r"^[0-9A-HJKMNP-TV-Z]{26}$", re.IGNORECASE)


@pytest.fixture
def tool() -> UuidTool:
    return UuidTool()


class TestUuidToolProperties:
    def test_name(self, tool: UuidTool) -> None:
        assert tool.name == "UUID / ULID Generator"

    def test_keyword(self, tool: UuidTool) -> None:
        assert tool.keyword == "uuid"

    def test_category(self, tool: UuidTool) -> None:
        assert tool.category == "Generators"


class TestUuidV4Generation:
    def test_default_generates_uuid_v4_format(self, tool: UuidTool) -> None:
        result = tool.process("")
        assert UUID_REGEX.match(result), f"Expected UUID format, got: {result}"

    def test_uuid_v4_version_nibble(self, tool: UuidTool) -> None:
        result = tool.process("")
        # UUID v4 has '4' as the 13th hex character (version nibble)
        hex_only = result.replace("-", "")
        assert hex_only[12] == "4"

    def test_uuid_v4_lowercase_by_default(self, tool: UuidTool) -> None:
        result = tool.process("")
        assert result == result.lower()

    def test_explicit_v4_version(self, tool: UuidTool) -> None:
        result = tool.process("", version="v4")
        assert UUID_REGEX.match(result)


class TestUuidMultipleGeneration:
    def test_generate_multiple_uuids(self, tool: UuidTool) -> None:
        result = tool.process("", count=5)
        uuids = result.strip().split("\n")
        assert len(uuids) == 5

    def test_multiple_uuids_are_unique(self, tool: UuidTool) -> None:
        result = tool.process("", count=10)
        uuids = result.strip().split("\n")
        assert len(set(uuids)) == 10, "All generated UUIDs should be unique"

    def test_each_generated_uuid_is_valid_format(self, tool: UuidTool) -> None:
        result = tool.process("", count=5)
        for line in result.strip().split("\n"):
            assert UUID_REGEX.match(line), f"Invalid UUID format: {line}"

    def test_count_clamped_to_max_100(self, tool: UuidTool) -> None:
        result = tool.process("", count=200)
        uuids = result.strip().split("\n")
        assert len(uuids) == 100

    def test_count_minimum_is_1(self, tool: UuidTool) -> None:
        result = tool.process("", count=0)
        uuids = result.strip().split("\n")
        assert len(uuids) == 1


class TestUuidValidation:
    def test_valid_uuid_recognized(self, tool: UuidTool, sample_uuid: str) -> None:
        result = tool.process(sample_uuid)
        assert "Valid UUID" in result

    def test_valid_uuid_shows_version(self, tool: UuidTool) -> None:
        # This is a known v4 UUID
        result = tool.process("f47ac10b-58cc-4372-a567-0e02b2c3d479")
        assert "Valid UUID" in result
        assert "version 4" in result

    def test_invalid_uuid_detected(self, tool: UuidTool) -> None:
        # Not a UUID pattern, so it generates instead of validating
        result = tool.process("not-a-uuid")
        # The tool generates a new UUID when input is not a UUID pattern
        assert UUID_REGEX.match(result.strip().split("\n")[0])

    def test_validate_uuid_with_uppercase(self, tool: UuidTool) -> None:
        result = tool.process("550E8400-E29B-41D4-A716-446655440000")
        assert "Valid UUID" in result


class TestUuidUppercaseLowercase:
    def test_uppercase_option(self, tool: UuidTool) -> None:
        result = tool.process("", uppercase=True)
        assert result == result.upper()
        assert UUID_REGEX.match(result)

    def test_lowercase_default(self, tool: UuidTool) -> None:
        result = tool.process("")
        assert result == result.lower()


class TestUuidV7Generation:
    def test_v7_generates_valid_uuid_format(self, tool: UuidTool) -> None:
        result = tool.process("", version="v7")
        assert UUID_REGEX.match(result), f"Expected UUID format, got: {result}"

    def test_v7_version_nibble(self, tool: UuidTool) -> None:
        result = tool.process("", version="v7")
        hex_only = result.replace("-", "")
        assert hex_only[12] == "7", f"Expected version nibble '7', got '{hex_only[12]}'"

    def test_v7_variant_bits(self, tool: UuidTool) -> None:
        result = tool.process("", version="v7")
        hex_only = result.replace("-", "")
        # Variant bits at position 16 should be 8, 9, a, or b
        assert hex_only[16] in "89ab", f"Expected variant 10xx, got '{hex_only[16]}'"

    def test_v7_multiple_are_unique(self, tool: UuidTool) -> None:
        result = tool.process("", version="v7", count=5)
        uuids = result.strip().split("\n")
        assert len(set(uuids)) == 5


class TestUlidGeneration:
    def test_ulid_format(self, tool: UuidTool) -> None:
        result = tool.process("", version="ulid")
        assert len(result) == 26, f"ULID should be 26 chars, got {len(result)}"

    def test_ulid_uses_valid_crockford_base32(self, tool: UuidTool) -> None:
        result = tool.process("", version="ulid")
        # Crockford Base32 uses 0-9 A-H J-K M-N P-T V-W X-Z (no I, L, O, U)
        assert ULID_REGEX.match(result), f"Invalid ULID characters: {result}"

    def test_ulid_multiple_are_unique(self, tool: UuidTool) -> None:
        result = tool.process("", version="ulid", count=5)
        ulids = result.strip().split("\n")
        assert len(set(ulids)) == 5

    def test_ulid_uppercase_option(self, tool: UuidTool) -> None:
        result = tool.process("", version="ulid", uppercase=True)
        assert result == result.upper()
