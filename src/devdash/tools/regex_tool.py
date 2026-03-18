"""Regex tester with match highlighting and common presets."""

import re

from devdash.tools.base import DevTool

PRESETS: dict[str, str] = {
    "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
    "url": r"https?://[^\s<>\"]+",
    "ipv4": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
    "phone": r"\+?[\d\s\-().]{7,15}",
    "date": r"\d{4}-\d{2}-\d{2}",
}


class RegexTool(DevTool):
    @property
    def name(self) -> str:
        return "Regex Tester"

    @property
    def keyword(self) -> str:
        return "regex"

    @property
    def category(self) -> str:
        return "Testers"

    @property
    def description(self) -> str:
        return "Enter pattern and test string separated by ---"

    def process(self, input_text: str, **kwargs: object) -> str:
        # Check kwargs first
        pattern = str(kwargs.get("pattern", ""))
        test_string = str(kwargs.get("test_string", ""))

        if not input_text.strip() and not pattern:
            return "Error: Empty input. Provide pattern and test string separated by \\n---\\n"

        if not pattern:
            parts = input_text.split("\n---\n", maxsplit=1)
            if len(parts) == 2:
                pattern = parts[0].strip()
                test_string = parts[1]
            else:
                # Try first line as pattern, rest as test string
                lines = input_text.split("\n", maxsplit=1)
                pattern = lines[0].strip()
                test_string = lines[1] if len(lines) > 1 else ""

        if not pattern:
            return "Error: No regex pattern provided."
        if not test_string:
            return "Error: No test string provided."

        # Check for preset
        if pattern.lower() in PRESETS:
            pattern = PRESETS[pattern.lower()]

        try:
            compiled = re.compile(pattern)
        except re.error as e:
            return f"Error: Invalid regex pattern: {e}"

        matches = list(compiled.finditer(test_string))

        if not matches:
            return f"Pattern: {pattern}\nNo matches found."

        lines = [f"Pattern: {pattern}", f"Matches: {len(matches)}", ""]

        for i, match in enumerate(matches, 1):
            lines.append(f"Match {i}: '{match.group()}' (position {match.start()}-{match.end()})")
            groups = match.groups()
            if groups:
                for j, g in enumerate(groups, 1):
                    lines.append(f"  Group {j}: '{g}'")
            named = match.groupdict()
            if named:
                for name, val in named.items():
                    lines.append(f"  Named '{name}': '{val}'")

        return "\n".join(lines)


def register() -> DevTool:
    return RegexTool()
