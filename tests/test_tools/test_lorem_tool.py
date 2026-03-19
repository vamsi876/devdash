"""Tests for LoremTool - lorem ipsum generator."""

import pytest

from gadgetbox.tools.lorem_tool import LoremTool


@pytest.fixture
def tool() -> LoremTool:
    return LoremTool()


class TestLoremToolMetadata:
    def test_name(self, tool: LoremTool) -> None:
        assert tool.name == "Lorem Ipsum Generator"

    def test_keyword(self, tool: LoremTool) -> None:
        assert tool.keyword == "lorem"


class TestWordCount:
    def test_five_words(self, tool: LoremTool) -> None:
        result = tool.process("5 words")
        # Output ends with a period, so strip it and count words
        words = result.rstrip(".").split()
        assert len(words) == 5

    def test_one_word(self, tool: LoremTool) -> None:
        result = tool.process("1 word")
        words = result.rstrip(".").split()
        assert len(words) == 1

    def test_ten_words(self, tool: LoremTool) -> None:
        result = tool.process("10 words")
        words = result.rstrip(".").split()
        assert len(words) == 10

    def test_word_output_starts_capitalized(self, tool: LoremTool) -> None:
        result = tool.process("3 words")
        assert result[0].isupper()

    def test_word_output_ends_with_period(self, tool: LoremTool) -> None:
        result = tool.process("5 words")
        assert result.endswith(".")


class TestSentenceCount:
    def test_three_sentences(self, tool: LoremTool) -> None:
        result = tool.process("3 sentences")
        # Sentences end with periods followed by space (except the last)
        sentences = [s.strip() for s in result.split(".") if s.strip()]
        assert len(sentences) == 3

    def test_one_sentence(self, tool: LoremTool) -> None:
        result = tool.process("1 sentence")
        sentences = [s.strip() for s in result.split(".") if s.strip()]
        assert len(sentences) == 1

    def test_sentences_contain_latin_text(self, tool: LoremTool) -> None:
        result = tool.process("2 sentences")
        # Should contain some recognizable latin-ish words
        result_lower = result.lower()
        latin_words = ["lorem", "ipsum", "dolor", "amet", "sed", "elit"]
        assert any(w in result_lower for w in latin_words)


class TestParagraphCount:
    def test_two_paragraphs(self, tool: LoremTool) -> None:
        result = tool.process("2 paragraphs")
        paragraphs = result.split("\n\n")
        assert len(paragraphs) == 2

    def test_one_paragraph(self, tool: LoremTool) -> None:
        result = tool.process("1 paragraph")
        paragraphs = result.split("\n\n")
        assert len(paragraphs) == 1

    def test_each_paragraph_has_content(self, tool: LoremTool) -> None:
        result = tool.process("3 paragraphs")
        for paragraph in result.split("\n\n"):
            assert len(paragraph) > 20


class TestDefaultOutput:
    def test_empty_input_returns_three_paragraphs(self, tool: LoremTool) -> None:
        result = tool.process("")
        paragraphs = result.split("\n\n")
        assert len(paragraphs) == 3

    def test_default_output_is_nonempty(self, tool: LoremTool) -> None:
        result = tool.process("")
        assert len(result) > 50


class TestLatinContent:
    def test_output_contains_latin_words(self, tool: LoremTool) -> None:
        result = tool.process("5 words")
        result_lower = result.lower()
        latin_words = [
            "lorem",
            "ipsum",
            "dolor",
            "sit",
            "amet",
            "consectetur",
            "adipiscing",
            "elit",
            "sed",
            "eiusmod",
            "tempor",
        ]
        assert any(w in result_lower for w in latin_words)

    def test_paragraphs_contain_latin(self, tool: LoremTool) -> None:
        result = tool.process("1 paragraph")
        result_lower = result.lower()
        assert any(w in result_lower for w in ["lorem", "dolor", "enim", "duis", "excepteur"])


class TestEdgeCases:
    def test_count_clamped_to_max_100(self, tool: LoremTool) -> None:
        # 200 words should be clamped to 100
        result = tool.process("200 words")
        words = result.rstrip(".").split()
        assert len(words) == 100

    def test_zero_defaults_to_one(self, tool: LoremTool) -> None:
        result = tool.process("0 words")
        words = result.rstrip(".").split()
        assert len(words) >= 1

    def test_negative_defaults_to_one(self, tool: LoremTool) -> None:
        result = tool.process("-5 words")
        # -5 can't be parsed as int via parts[0], so count stays 1
        assert len(result) > 0
