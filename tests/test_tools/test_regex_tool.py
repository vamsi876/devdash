"""Tests for RegexTool - regex tester with match highlighting."""

import pytest

from devdash.tools.regex_tool import RegexTool


@pytest.fixture
def tool() -> RegexTool:
    return RegexTool()


class TestRegexToolMetadata:
    def test_name(self, tool: RegexTool) -> None:
        assert tool.name == "Regex Tester"

    def test_keyword(self, tool: RegexTool) -> None:
        assert tool.keyword == "regex"


class TestSimplePatternMatching:
    def test_single_match(self, tool: RegexTool) -> None:
        result = tool.process("", pattern=r"\d+", test_string="abc 123 def")
        assert "Matches: 1" in result
        assert "'123'" in result

    def test_multiple_matches(self, tool: RegexTool) -> None:
        result = tool.process("", pattern=r"\d+", test_string="a1 b22 c333")
        assert "Matches: 3" in result
        assert "'1'" in result
        assert "'22'" in result
        assert "'333'" in result

    def test_match_position_reported(self, tool: RegexTool) -> None:
        result = tool.process("", pattern=r"world", test_string="hello world")
        assert "position 6-11" in result

    def test_literal_match(self, tool: RegexTool) -> None:
        result = tool.process("", pattern="hello", test_string="say hello there")
        assert "Matches: 1" in result
        assert "'hello'" in result


class TestGroupCaptures:
    def test_numbered_groups(self, tool: RegexTool) -> None:
        result = tool.process(
            "", pattern=r"(\d{3})-(\d{4})", test_string="call 555-1234 now"
        )
        assert "Group 1: '555'" in result
        assert "Group 2: '1234'" in result

    def test_no_groups(self, tool: RegexTool) -> None:
        result = tool.process("", pattern=r"\d+", test_string="abc 42")
        assert "Group" not in result


class TestNamedGroups:
    def test_named_groups_reported(self, tool: RegexTool) -> None:
        result = tool.process(
            "",
            pattern=r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})",
            test_string="date: 2025-03-17",
        )
        assert "Named 'year': '2025'" in result
        assert "Named 'month': '03'" in result
        assert "Named 'day': '17'" in result


class TestInvalidRegex:
    def test_invalid_pattern_returns_error(self, tool: RegexTool) -> None:
        result = tool.process("", pattern=r"[invalid", test_string="test")
        assert result.startswith("Error: Invalid regex pattern:")

    def test_invalid_pattern_does_not_crash(self, tool: RegexTool) -> None:
        # Should not raise any exception
        result = tool.process("", pattern=r"(unclosed", test_string="test")
        assert "Error" in result

    def test_unbalanced_braces(self, tool: RegexTool) -> None:
        result = tool.process("", pattern=r"a{", test_string="aaa")
        # Depending on regex engine this may or may not error; just ensure no crash
        assert isinstance(result, str)


class TestNoMatchesFound:
    def test_no_matches(self, tool: RegexTool) -> None:
        result = tool.process("", pattern=r"\d+", test_string="no digits here")
        assert "No matches found" in result

    def test_no_matches_shows_pattern(self, tool: RegexTool) -> None:
        result = tool.process("", pattern=r"xyz", test_string="abc")
        assert "Pattern: xyz" in result


class TestSeparatorFormat:
    def test_pattern_separator_test_string(self, tool: RegexTool) -> None:
        input_text = r"\d+" + "\n---\n" + "abc 42 def"
        result = tool.process(input_text)
        assert "Matches: 1" in result
        assert "'42'" in result

    def test_first_line_pattern_rest_test_string(self, tool: RegexTool) -> None:
        input_text = r"\w+" + "\nhello world"
        result = tool.process(input_text)
        assert "Matches: 2" in result

    def test_separator_with_multiline_test(self, tool: RegexTool) -> None:
        input_text = r"\d+" + "\n---\n" + "line1: 10\nline2: 20"
        result = tool.process(input_text)
        assert "Matches: 4" in result


class TestEmptyInput:
    def test_empty_string(self, tool: RegexTool) -> None:
        result = tool.process("")
        assert "Error" in result

    def test_whitespace_only(self, tool: RegexTool) -> None:
        result = tool.process("   ")
        assert "Error" in result

    def test_pattern_but_no_test_string(self, tool: RegexTool) -> None:
        result = tool.process("", pattern=r"\d+", test_string="")
        assert "Error: No test string provided." in result

    def test_no_pattern_provided(self, tool: RegexTool) -> None:
        result = tool.process("", pattern="", test_string="hello")
        assert "Error" in result


class TestPresets:
    def test_email_preset(self, tool: RegexTool) -> None:
        result = tool.process(
            "", pattern="email", test_string="contact user@example.com today"
        )
        assert "user@example.com" in result

    def test_ipv4_preset(self, tool: RegexTool) -> None:
        result = tool.process(
            "", pattern="ipv4", test_string="server at 192.168.1.1 is down"
        )
        assert "192.168.1.1" in result
