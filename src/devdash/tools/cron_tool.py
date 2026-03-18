"""Cron expression parser and scheduler."""

from datetime import datetime, timezone

from croniter import croniter

from devdash.tools.base import DevTool

PRESETS: dict[str, str] = {
    "every minute": "* * * * *",
    "hourly": "0 * * * *",
    "daily": "0 0 * * *",
    "weekly": "0 0 * * 1",
    "monthly": "0 0 1 * *",
    "yearly": "0 0 1 1 *",
}

_FIELD_NAMES = ["minute", "hour", "day of month", "month", "day of week"]


class CronTool(DevTool):
    @property
    def name(self) -> str:
        return "Cron Expression Parser"

    @property
    def keyword(self) -> str:
        return "cron"

    @property
    def category(self) -> str:
        return "Converters"

    @property
    def description(self) -> str:
        return "Enter a cron expression (e.g. '*/5 * * * *') or leave empty for presets"

    def process(self, input_text: str, **kwargs: object) -> str:
        if not input_text.strip():
            lines = ["Common cron presets:"]
            for name, expr in PRESETS.items():
                lines.append(f"  {expr:15s}  {name}")
            return "\n".join(lines)

        text = input_text.strip()

        # Check if it's a preset name
        if text.lower() in PRESETS:
            text = PRESETS[text.lower()]

        # Validate cron expression
        if not croniter.is_valid(text):
            return (
                f"Error: Invalid cron expression '{text}'.\n\n"
                "Format: minute hour day-of-month month day-of-week\n"
                "Example: 0 9 * * 1-5 (9 AM on weekdays)"
            )

        # Human-readable description
        desc = self._describe(text)

        # Next 5 run times
        now = datetime.now(timezone.utc)
        cron = croniter(text, now)
        next_runs: list[str] = []
        for _ in range(5):
            next_dt = cron.get_next(datetime)
            next_runs.append(f"  {next_dt.strftime('%Y-%m-%d %H:%M:%S UTC')}")

        lines = [
            f"Expression:  {text}",
            f"Description: {desc}",
            "",
            "Next 5 runs:",
            *next_runs,
        ]
        return "\n".join(lines)

    def _describe(self, expr: str) -> str:
        """Generate a human-readable description of a cron expression."""
        parts = expr.split()
        if len(parts) < 5:
            return expr

        minute, hour, dom, month, dow = parts[0], parts[1], parts[2], parts[3], parts[4]

        # Common patterns
        if expr == "* * * * *":
            return "Every minute"
        if minute != "*" and hour == "*" and dom == "*" and month == "*" and dow == "*":
            return f"Every hour at minute {minute}"
        if minute != "*" and hour != "*" and dom == "*" and month == "*" and dow == "*":
            return f"At {hour.zfill(2)}:{minute.zfill(2)} every day"
        if minute != "*" and hour != "*" and dom == "*" and month == "*" and dow != "*":
            dow_name = self._dow_name(dow)
            return f"At {hour.zfill(2)}:{minute.zfill(2)} on {dow_name}"
        if minute != "*" and hour != "*" and dom != "*" and month == "*" and dow == "*":
            return f"At {hour.zfill(2)}:{minute.zfill(2)} on day {dom} of every month"

        # Generic fallback
        desc_parts: list[str] = []
        if minute == "*":
            desc_parts.append("every minute")
        else:
            desc_parts.append(f"at minute {minute}")
        if hour != "*":
            desc_parts.append(f"past hour {hour}")
        if dom != "*":
            desc_parts.append(f"on day {dom}")
        if month != "*":
            desc_parts.append(f"in month {month}")
        if dow != "*":
            desc_parts.append(f"on {self._dow_name(dow)}")

        return ", ".join(desc_parts).capitalize()

    def _dow_name(self, dow: str) -> str:
        names = {
            "0": "Sunday",
            "1": "Monday",
            "2": "Tuesday",
            "3": "Wednesday",
            "4": "Thursday",
            "5": "Friday",
            "6": "Saturday",
            "7": "Sunday",
        }
        if dow in names:
            return names[dow]
        if "-" in dow:
            start, end = dow.split("-", 1)
            return f"{names.get(start, start)} to {names.get(end, end)}"
        return dow


def register() -> DevTool:
    return CronTool()
