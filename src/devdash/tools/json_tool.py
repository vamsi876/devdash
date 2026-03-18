"""JSON formatter, validator, and minifier."""

import json

from devdash.tools.base import DevTool


class JsonTool(DevTool):
    @property
    def name(self) -> str:
        return "JSON Formatter"

    @property
    def keyword(self) -> str:
        return "json"

    @property
    def category(self) -> str:
        return "Formatters"

    @property
    def description(self) -> str:
        return "Paste JSON to format and pretty-print"

    def process(self, input_text: str, **kwargs: object) -> str:
        if not input_text.strip():
            return "Error: Empty input. Please provide a JSON string."

        mode = str(kwargs.get("mode", "format"))

        if mode == "validate":
            return self._validate_json(input_text)
        elif mode == "minify":
            return self._minify(input_text)
        else:
            return self._format(input_text)

    def _format(self, text: str) -> str:
        try:
            parsed = json.loads(text)
            return json.dumps(parsed, indent=2, ensure_ascii=False)
        except json.JSONDecodeError as e:
            return f"Invalid JSON: {e.msg} (line {e.lineno}, column {e.colno})"

    def _minify(self, text: str) -> str:
        try:
            parsed = json.loads(text)
            return json.dumps(parsed, separators=(",", ":"), ensure_ascii=False)
        except json.JSONDecodeError as e:
            return f"Invalid JSON: {e.msg} (line {e.lineno}, column {e.colno})"

    def _validate_json(self, text: str) -> str:
        try:
            json.loads(text)
            return "Valid JSON"
        except json.JSONDecodeError as e:
            return f"Invalid JSON: {e.msg} (line {e.lineno}, column {e.colno})"


def register() -> DevTool:
    return JsonTool()
