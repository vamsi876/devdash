"""Tests for TimestampTool - Unix timestamp and human date converter."""

from datetime import datetime, timezone

import pytest

from gadgetbox.tools.timestamp_tool import TimestampTool


@pytest.fixture
def tool() -> TimestampTool:
    return TimestampTool()


class TestTimestampToolProperties:
    def test_name(self, tool: TimestampTool) -> None:
        assert tool.name == "Timestamp Converter"

    def test_keyword(self, tool: TimestampTool) -> None:
        assert tool.keyword == "timestamp"

    def test_category(self, tool: TimestampTool) -> None:
        assert tool.category == "Converters"


class TestTimestampEpochZero:
    def test_epoch_zero_is_1970(self, tool: TimestampTool) -> None:
        result = tool.process("0000000000")
        assert "1970-01-01" in result
        assert "00:00:00" in result

    def test_epoch_zero_utc(self, tool: TimestampTool) -> None:
        result = tool.process("0000000000")
        assert "UTC" in result

    def test_epoch_zero_detected_as_seconds(self, tool: TimestampTool) -> None:
        result = tool.process("0000000000")
        assert "seconds" in result


class TestTimestampMilliseconds:
    def test_13_digit_detected_as_milliseconds(self, tool: TimestampTool) -> None:
        # 1700000000000 ms = 2023-11-14 22:13:20 UTC
        result = tool.process("1700000000000")
        assert "milliseconds" in result

    def test_millisecond_timestamp_correct_date(self, tool: TimestampTool) -> None:
        # 0 ms in epoch = 1970-01-01
        result = tool.process("0000000000000")
        assert "1970-01-01" in result

    def test_known_millisecond_timestamp(self, tool: TimestampTool) -> None:
        # 1000000000000 ms = 2001-09-09 01:46:40 UTC
        result = tool.process("1000000000000")
        assert "2001-09-09" in result


class TestTimestampFromSeconds:
    def test_known_timestamp_seconds(self, tool: TimestampTool) -> None:
        # 1000000000 = 2001-09-09 01:46:40 UTC
        result = tool.process("1000000000")
        assert "2001-09-09" in result

    def test_timestamp_shows_relative_time(self, tool: TimestampTool) -> None:
        result = tool.process("0000000000")
        assert "Relative:" in result
        assert "ago" in result

    def test_timestamp_shows_iso8601(self, tool: TimestampTool) -> None:
        result = tool.process("1000000000")
        assert "ISO 8601:" in result
        assert "T" in result  # ISO 8601 contains T separator


class TestTimestampDateToUnix:
    def test_date_string_to_timestamp(self, tool: TimestampTool) -> None:
        result = tool.process("2024-01-01")
        assert "Unix (seconds):" in result
        assert "Unix (milliseconds):" in result
        # 2024-01-01 00:00:00 UTC = 1704067200
        assert "1704067200" in result

    def test_datetime_string_to_timestamp(self, tool: TimestampTool) -> None:
        result = tool.process("2024-01-01 12:00:00")
        assert "Unix (seconds):" in result
        # 2024-01-01 12:00:00 UTC = 1704110400
        assert "1704110400" in result

    def test_iso_format_with_t(self, tool: TimestampTool) -> None:
        result = tool.process("2024-01-01T12:00:00")
        assert "1704110400" in result

    def test_iso_format_with_z(self, tool: TimestampTool) -> None:
        result = tool.process("2024-01-01T00:00:00Z")
        assert "1704067200" in result

    def test_date_to_timestamp_shows_iso8601(self, tool: TimestampTool) -> None:
        result = tool.process("2024-01-01")
        assert "ISO 8601:" in result


class TestTimestampEmptyInput:
    def test_empty_input_shows_current_time(self, tool: TimestampTool) -> None:
        result = tool.process("")
        assert "Current time:" in result
        assert "Unix:" in result
        assert "UTC" in result

    def test_whitespace_only_shows_current_time(self, tool: TimestampTool) -> None:
        result = tool.process("   \n  ")
        assert "Current time:" in result

    def test_current_time_is_reasonable(self, tool: TimestampTool) -> None:
        result = tool.process("")
        # Extract the unix timestamp from the output
        for line in result.split("\n"):
            if line.startswith("Unix:"):
                ts = int(line.split(":")[1].strip())
                # Should be after 2024 and before 2030
                assert 1704067200 < ts < 1893456000


class TestTimestampInvalidInput:
    def test_invalid_date_string(self, tool: TimestampTool) -> None:
        result = tool.process("not-a-date")
        assert "Error" in result
        assert "Could not parse" in result

    def test_invalid_date_shows_supported_formats(self, tool: TimestampTool) -> None:
        result = tool.process("January 1st 2024")
        assert "Error" in result
        assert "Supported formats" in result
        assert "%Y-%m-%d" in result

    def test_partial_date_string(self, tool: TimestampTool) -> None:
        result = tool.process("2024-13")
        assert "Error" in result


class TestTimestampRelativeTime:
    def test_relative_time_past_years(self, tool: TimestampTool) -> None:
        result = tool.process("0000000000")
        assert "year" in result
        assert "ago" in result

    def test_relative_time_recent_past(self, tool: TimestampTool) -> None:
        # Use a timestamp from roughly 1 hour ago
        now = int(datetime.now(timezone.utc).timestamp())
        one_hour_ago = str(now - 3600)
        result = tool.process(one_hour_ago)
        assert "Relative:" in result
        # Could be "1 hour ago" or close
        assert "hour" in result or "minute" in result
