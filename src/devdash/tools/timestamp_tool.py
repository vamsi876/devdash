"""Unix timestamp <-> human date converter."""

import re
from datetime import datetime, timezone

from devdash.tools.base import DevTool


def _relative_time(dt: datetime) -> str:
    """Return human-friendly relative time string."""
    now = datetime.now(timezone.utc)
    diff = now - dt
    seconds = int(diff.total_seconds())

    if seconds < 0:
        return _relative_future(-seconds)

    if seconds < 60:
        return f"{seconds} seconds ago"
    minutes = seconds // 60
    if minutes < 60:
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    hours = minutes // 60
    if hours < 24:
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    days = hours // 24
    if days < 30:
        return f"{days} day{'s' if days != 1 else ''} ago"
    months = days // 30
    if months < 12:
        return f"{months} month{'s' if months != 1 else ''} ago"
    years = days // 365
    return f"{years} year{'s' if years != 1 else ''} ago"


def _relative_future(seconds: int) -> str:
    if seconds < 60:
        return f"in {seconds} seconds"
    minutes = seconds // 60
    if minutes < 60:
        return f"in {minutes} minute{'s' if minutes != 1 else ''}"
    hours = minutes // 60
    if hours < 24:
        return f"in {hours} hour{'s' if hours != 1 else ''}"
    days = hours // 24
    return f"in {days} day{'s' if days != 1 else ''}"


class TimestampTool(DevTool):
    @property
    def name(self) -> str:
        return "Timestamp Converter"

    @property
    def keyword(self) -> str:
        return "timestamp"

    @property
    def category(self) -> str:
        return "Converters"

    @property
    def description(self) -> str:
        return "Convert between Unix timestamps and human-readable dates"

    def process(self, input_text: str, **kwargs: object) -> str:
        if not input_text.strip():
            # Show current timestamp
            now = datetime.now(timezone.utc)
            ts = int(now.timestamp())
            return f"Current time:\nUnix: {ts}\nUTC:  {now.strftime('%Y-%m-%d %H:%M:%S UTC')}"

        text = input_text.strip()

        # Auto-detect: if pure digits, treat as timestamp
        if re.match(r"^\d{10,13}$", text):
            return self._from_timestamp(text)
        else:
            return self._to_timestamp(text)

    def _from_timestamp(self, text: str) -> str:
        ts = int(text)
        is_millis = len(text) == 13
        if is_millis:
            ts_seconds = ts / 1000
        else:
            ts_seconds = float(ts)

        try:
            dt = datetime.fromtimestamp(ts_seconds, tz=timezone.utc)
        except (OSError, OverflowError, ValueError):
            return f"Error: Timestamp {text} is out of valid range."

        local_tz = datetime.now().astimezone().tzinfo
        local_dt = dt.astimezone(local_tz)

        lines = [
            f"Input: {text} ({'milliseconds' if is_millis else 'seconds'})",
            "",
            f"UTC:   {dt.strftime('%Y-%m-%d %H:%M:%S %Z')}",
            f"Local: {local_dt.strftime('%Y-%m-%d %H:%M:%S %Z')}",
            "",
            f"Relative: {_relative_time(dt)}",
            f"ISO 8601: {dt.isoformat()}",
        ]
        return "\n".join(lines)

    def _to_timestamp(self, text: str) -> str:
        formats = [
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%dT%H:%M:%SZ",
            "%Y-%m-%d",
            "%d/%m/%Y %H:%M:%S",
            "%d/%m/%Y",
            "%m/%d/%Y",
        ]

        dt = None
        for fmt in formats:
            try:
                dt = datetime.strptime(text, fmt).replace(tzinfo=timezone.utc)
                break
            except ValueError:
                continue

        if dt is None:
            return f"Error: Could not parse date '{text}'. Supported formats:\n" + "\n".join(
                f"  {f}" for f in formats
            )

        ts = int(dt.timestamp())
        ts_ms = ts * 1000
        return (
            f"Unix (seconds):      {ts}\n"
            f"Unix (milliseconds): {ts_ms}\n"
            f"ISO 8601:            {dt.isoformat()}"
        )


def register() -> DevTool:
    return TimestampTool()
