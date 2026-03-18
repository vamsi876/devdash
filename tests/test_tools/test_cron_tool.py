"""Tests for CronTool - cron expression parser and scheduler."""

import pytest

from devdash.tools.cron_tool import CronTool


@pytest.fixture
def tool() -> CronTool:
    return CronTool()


class TestCronToolMetadata:
    def test_name(self, tool: CronTool) -> None:
        assert tool.name == "Cron Expression Parser"

    def test_keyword(self, tool: CronTool) -> None:
        assert tool.keyword == "cron"


class TestHourlyExpression:
    def test_every_hour_description(self, tool: CronTool) -> None:
        result = tool.process("0 * * * *")
        assert "Every hour" in result or "every hour" in result

    def test_every_hour_shows_expression(self, tool: CronTool) -> None:
        result = tool.process("0 * * * *")
        assert "Expression:  0 * * * *" in result


class TestCommonExpressions:
    def test_every_minute(self, tool: CronTool) -> None:
        result = tool.process("* * * * *")
        assert "Every minute" in result

    def test_daily_at_midnight(self, tool: CronTool) -> None:
        result = tool.process("0 0 * * *")
        assert "00:00" in result
        assert "every day" in result

    def test_specific_time_on_weekday(self, tool: CronTool) -> None:
        result = tool.process("0 9 * * 1-5")
        assert "09:00" in result
        assert "Monday" in result
        assert "Friday" in result

    def test_monthly(self, tool: CronTool) -> None:
        result = tool.process("0 0 1 * *")
        assert "day 1" in result


class TestInvalidExpression:
    def test_invalid_cron_returns_error(self, tool: CronTool) -> None:
        result = tool.process("not a cron")
        assert "Error: Invalid cron expression" in result

    def test_invalid_shows_format_help(self, tool: CronTool) -> None:
        result = tool.process("invalid")
        assert "minute hour day-of-month month day-of-week" in result

    def test_too_few_fields(self, tool: CronTool) -> None:
        result = tool.process("* *")
        assert "Error" in result

    def test_out_of_range_values(self, tool: CronTool) -> None:
        result = tool.process("99 99 99 99 99")
        assert "Error" in result


class TestNextRunTimes:
    def test_next_runs_shown(self, tool: CronTool) -> None:
        result = tool.process("0 * * * *")
        assert "Next 5 runs:" in result

    def test_five_next_runs(self, tool: CronTool) -> None:
        result = tool.process("0 12 * * *")
        assert "Next 5 runs:" in result
        # Count the UTC timestamps after "Next 5 runs:"
        lines_after = result.split("Next 5 runs:\n")[1].strip().split("\n")
        assert len(lines_after) == 5

    def test_next_runs_contain_utc(self, tool: CronTool) -> None:
        result = tool.process("30 6 * * *")
        assert "UTC" in result

    def test_next_runs_are_in_future(self, tool: CronTool) -> None:
        from datetime import datetime, timezone

        result = tool.process("0 0 * * *")
        now = datetime.now(timezone.utc)
        # Extract a date from the output
        lines = result.split("Next 5 runs:\n")[1].strip().split("\n")
        first_run = lines[0].strip()
        # Parse "2025-03-18 00:00:00 UTC"
        date_str = first_run.replace(" UTC", "")
        run_dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").replace(
            tzinfo=timezone.utc
        )
        assert run_dt > now


class TestPresetNames:
    def test_hourly_preset(self, tool: CronTool) -> None:
        result = tool.process("hourly")
        assert "Expression:  0 * * * *" in result
        assert "Next 5 runs:" in result

    def test_daily_preset(self, tool: CronTool) -> None:
        result = tool.process("daily")
        assert "Expression:  0 0 * * *" in result

    def test_weekly_preset(self, tool: CronTool) -> None:
        result = tool.process("weekly")
        assert "Expression:  0 0 * * 1" in result

    def test_monthly_preset(self, tool: CronTool) -> None:
        result = tool.process("monthly")
        assert "Expression:  0 0 1 * *" in result

    def test_yearly_preset(self, tool: CronTool) -> None:
        result = tool.process("yearly")
        assert "Expression:  0 0 1 1 *" in result

    def test_every_minute_preset(self, tool: CronTool) -> None:
        result = tool.process("every minute")
        assert "Expression:  * * * * *" in result

    def test_preset_case_insensitive(self, tool: CronTool) -> None:
        result = tool.process("Hourly")
        assert "Expression:  0 * * * *" in result


class TestEmptyInput:
    def test_empty_shows_presets(self, tool: CronTool) -> None:
        result = tool.process("")
        assert "Common cron presets:" in result

    def test_empty_lists_all_presets(self, tool: CronTool) -> None:
        result = tool.process("")
        assert "hourly" in result
        assert "daily" in result
        assert "weekly" in result
        assert "monthly" in result
        assert "yearly" in result
        assert "every minute" in result

    def test_whitespace_only_shows_presets(self, tool: CronTool) -> None:
        result = tool.process("   ")
        assert "Common cron presets:" in result
