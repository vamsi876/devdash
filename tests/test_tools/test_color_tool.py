"""Tests for ColorTool - color converter between HEX, RGB, HSL, HSV."""

import pytest

from devdash.tools.color_tool import ColorTool


@pytest.fixture
def tool() -> ColorTool:
    return ColorTool()


class TestColorToolMetadata:
    def test_name(self, tool: ColorTool) -> None:
        assert tool.name == "Color Converter"

    def test_keyword(self, tool: ColorTool) -> None:
        assert tool.keyword == "color"


class TestHexInput:
    def test_hex_red(self, tool: ColorTool) -> None:
        result = tool.process("#FF0000")
        assert "HEX:           #FF0000" in result
        assert "RGB:           rgb(255, 0, 0)" in result

    def test_hex_without_hash(self, tool: ColorTool) -> None:
        result = tool.process("FF0000")
        assert "HEX:           #FF0000" in result
        assert "rgb(255, 0, 0)" in result

    def test_hex_black(self, tool: ColorTool) -> None:
        result = tool.process("#000000")
        assert "rgb(0, 0, 0)" in result

    def test_hex_white(self, tool: ColorTool) -> None:
        result = tool.process("#FFFFFF")
        assert "rgb(255, 255, 255)" in result

    def test_hex_lowercase(self, tool: ColorTool) -> None:
        result = tool.process("#ff0000")
        assert "HEX:           #FF0000" in result


class TestThreeCharHex:
    def test_three_char_red(self, tool: ColorTool) -> None:
        result = tool.process("#F00")
        assert "HEX:           #FF0000" in result
        assert "rgb(255, 0, 0)" in result

    def test_three_char_white(self, tool: ColorTool) -> None:
        result = tool.process("#FFF")
        assert "HEX:           #FFFFFF" in result

    def test_three_char_without_hash(self, tool: ColorTool) -> None:
        result = tool.process("ABC")
        assert "HEX:           #AABBCC" in result


class TestRgbInput:
    def test_rgb_red(self, tool: ColorTool) -> None:
        result = tool.process("rgb(255, 0, 0)")
        assert "HEX:           #FF0000" in result

    def test_rgb_no_spaces(self, tool: ColorTool) -> None:
        result = tool.process("rgb(0,128,255)")
        assert "HEX:           #0080FF" in result

    def test_rgb_case_insensitive(self, tool: ColorTool) -> None:
        result = tool.process("RGB(100, 200, 50)")
        assert "HEX:" in result

    def test_rgb_out_of_range(self, tool: ColorTool) -> None:
        result = tool.process("rgb(300, 0, 0)")
        assert "Error" in result
        assert "RGB values must be between 0 and 255" in result

    def test_plain_rgb_numbers(self, tool: ColorTool) -> None:
        result = tool.process("255, 0, 0")
        assert "HEX:           #FF0000" in result

    def test_plain_rgb_space_separated(self, tool: ColorTool) -> None:
        result = tool.process("0 128 255")
        assert "HEX:           #0080FF" in result


class TestHslInput:
    def test_hsl_red(self, tool: ColorTool) -> None:
        result = tool.process("hsl(0, 100, 50)")
        assert "HEX:" in result
        assert "RGB:" in result

    def test_hsl_with_percent(self, tool: ColorTool) -> None:
        result = tool.process("hsl(0, 100%, 50%)")
        assert "HEX:" in result

    def test_hsl_case_insensitive(self, tool: ColorTool) -> None:
        result = tool.process("HSL(120, 100, 50)")
        assert "HEX:" in result

    def test_hsl_blue(self, tool: ColorTool) -> None:
        result = tool.process("hsl(240, 100, 50)")
        assert "RGB:" in result


class TestComplementaryColor:
    def test_complement_of_red_is_cyan(self, tool: ColorTool) -> None:
        result = tool.process("#FF0000")
        assert "Complementary: #00FFFF" in result

    def test_complement_of_white_is_black(self, tool: ColorTool) -> None:
        result = tool.process("#FFFFFF")
        assert "Complementary: #000000" in result

    def test_complement_of_black_is_white(self, tool: ColorTool) -> None:
        result = tool.process("#000000")
        assert "Complementary: #FFFFFF" in result

    def test_complement_present_in_output(self, tool: ColorTool) -> None:
        result = tool.process("#336699")
        assert "Complementary:" in result


class TestOutputFormats:
    def test_all_formats_present(self, tool: ColorTool) -> None:
        result = tool.process("#FF0000")
        assert "HEX:" in result
        assert "RGB:" in result
        assert "HSL:" in result
        assert "HSV:" in result
        assert "Complementary:" in result

    def test_hsl_values_for_pure_red(self, tool: ColorTool) -> None:
        result = tool.process("#FF0000")
        assert "hsl(0, 100%, 50%)" in result

    def test_hsv_values_for_pure_red(self, tool: ColorTool) -> None:
        result = tool.process("#FF0000")
        assert "hsv(0, 100%, 100%)" in result


class TestInvalidInput:
    def test_unrecognized_format(self, tool: ColorTool) -> None:
        result = tool.process("not a color")
        assert "Error: Unrecognized color format" in result

    def test_invalid_hex_chars(self, tool: ColorTool) -> None:
        result = tool.process("#GGGGGG")
        assert "Error" in result

    def test_too_many_digits(self, tool: ColorTool) -> None:
        result = tool.process("#FF00001")
        assert "Error" in result


class TestEmptyInput:
    def test_empty_string(self, tool: ColorTool) -> None:
        result = tool.process("")
        assert "Error: Empty input" in result

    def test_whitespace_only(self, tool: ColorTool) -> None:
        result = tool.process("   ")
        assert "Error: Empty input" in result
