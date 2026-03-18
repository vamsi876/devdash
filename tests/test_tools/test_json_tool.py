"""Tests for JsonTool - JSON formatter, validator, and minifier."""

import json

import pytest

from devdash.tools.json_tool import JsonTool


@pytest.fixture
def tool() -> JsonTool:
    return JsonTool()


class TestJsonToolProperties:
    def test_name(self, tool: JsonTool) -> None:
        assert tool.name == "JSON Formatter"

    def test_keyword(self, tool: JsonTool) -> None:
        assert tool.keyword == "json"

    def test_category(self, tool: JsonTool) -> None:
        assert tool.category == "Formatters"


class TestJsonFormat:
    def test_pretty_print_simple_object(self, tool: JsonTool) -> None:
        result = tool.process('{"name":"test","value":42}')
        parsed = json.loads(result)
        assert parsed == {"name": "test", "value": 42}
        # Should be indented
        assert "\n" in result
        assert "  " in result

    def test_pretty_print_nested_object(self, tool: JsonTool) -> None:
        input_json = '{"a":{"b":{"c":1}}}'
        result = tool.process(input_json)
        parsed = json.loads(result)
        assert parsed == {"a": {"b": {"c": 1}}}
        # Nested indentation
        assert '    "c"' in result

    def test_pretty_print_array(self, tool: JsonTool) -> None:
        result = tool.process("[1,2,3]")
        parsed = json.loads(result)
        assert parsed == [1, 2, 3]

    def test_pretty_print_preserves_unicode(self, tool: JsonTool) -> None:
        input_json = '{"emoji": "\\u2764", "name": "caf\\u00e9"}'
        result = tool.process(input_json)
        # ensure_ascii=False means actual unicode characters should appear
        assert json.loads(result)["name"] == "caf\u00e9"

    def test_pretty_print_null_values(self, tool: JsonTool) -> None:
        result = tool.process('{"key": null}')
        parsed = json.loads(result)
        assert parsed["key"] is None

    def test_pretty_print_boolean_values(self, tool: JsonTool) -> None:
        result = tool.process('{"a": true, "b": false}')
        parsed = json.loads(result)
        assert parsed == {"a": True, "b": False}

    def test_pretty_print_empty_object(self, tool: JsonTool) -> None:
        result = tool.process("{}")
        assert json.loads(result) == {}

    def test_pretty_print_empty_array(self, tool: JsonTool) -> None:
        result = tool.process("[]")
        assert json.loads(result) == []

    def test_format_is_default_mode(self, tool: JsonTool, sample_json_valid: str) -> None:
        explicit = tool.process(sample_json_valid, mode="format")
        default = tool.process(sample_json_valid)
        assert explicit == default


class TestJsonMinify:
    def test_minify_removes_whitespace(self, tool: JsonTool) -> None:
        formatted = '{\n  "name": "test",\n  "value": 42\n}'
        result = tool.process(formatted, mode="minify")
        assert " " not in result.replace('" "', "")  # no extraneous spaces
        assert "\n" not in result

    def test_minify_uses_compact_separators(self, tool: JsonTool) -> None:
        result = tool.process('{"a": 1, "b": 2}', mode="minify")
        assert result == '{"a":1,"b":2}'

    def test_minify_preserves_data(self, tool: JsonTool) -> None:
        original = '{"items": [1, 2, 3], "nested": {"x": null}}'
        result = tool.process(original, mode="minify")
        assert json.loads(result) == json.loads(original)

    def test_minify_invalid_json(self, tool: JsonTool) -> None:
        result = tool.process("{bad json}", mode="minify")
        assert "Invalid JSON" in result


class TestJsonValidate:
    def test_valid_json(self, tool: JsonTool, sample_json_valid: str) -> None:
        result = tool.process(sample_json_valid, mode="validate")
        assert result == "Valid JSON"

    def test_valid_json_array(self, tool: JsonTool) -> None:
        result = tool.process("[1, 2, 3]", mode="validate")
        assert result == "Valid JSON"

    def test_valid_json_string(self, tool: JsonTool) -> None:
        result = tool.process('"hello"', mode="validate")
        assert result == "Valid JSON"

    def test_valid_json_number(self, tool: JsonTool) -> None:
        result = tool.process("42", mode="validate")
        assert result == "Valid JSON"

    def test_invalid_json(self, tool: JsonTool, sample_json_invalid: str) -> None:
        result = tool.process(sample_json_invalid, mode="validate")
        assert "Invalid JSON" in result

    def test_invalid_json_includes_location(self, tool: JsonTool) -> None:
        result = tool.process("{bad}", mode="validate")
        assert "line" in result
        assert "column" in result


class TestJsonErrorHandling:
    def test_empty_input(self, tool: JsonTool) -> None:
        result = tool.process("")
        assert "Error" in result
        assert "Empty input" in result

    def test_whitespace_only_input(self, tool: JsonTool) -> None:
        result = tool.process("   \n\t  ")
        assert "Error" in result
        assert "Empty input" in result

    def test_invalid_json_format_mode(self, tool: JsonTool) -> None:
        result = tool.process("{not: valid}")
        assert "Invalid JSON" in result
        assert "line" in result
        assert "column" in result

    def test_trailing_comma(self, tool: JsonTool) -> None:
        result = tool.process('{"a": 1,}')
        assert "Invalid JSON" in result

    def test_single_quotes(self, tool: JsonTool) -> None:
        result = tool.process("{'key': 'value'}")
        assert "Invalid JSON" in result
