"""Tests for PasswordTool - secure password generator."""

import pytest

from gadgetbox.tools.password_tool import PasswordTool


@pytest.fixture
def tool() -> PasswordTool:
    return PasswordTool()


class TestPasswordToolMetadata:
    def test_name(self, tool: PasswordTool) -> None:
        assert tool.name == "Password Generator"

    def test_keyword(self, tool: PasswordTool) -> None:
        assert tool.keyword == "password"


class TestDefaultPassword:
    def test_default_length_is_16(self, tool: PasswordTool) -> None:
        result = tool.process("")
        # Output format: "password  (entropy: X bits)"
        password = result.split("  (entropy:")[0]
        assert len(password) == 16

    def test_default_contains_entropy(self, tool: PasswordTool) -> None:
        result = tool.process("")
        assert "entropy:" in result
        assert "bits" in result


class TestCustomLength:
    def test_length_via_input(self, tool: PasswordTool) -> None:
        result = tool.process("24")
        password = result.split("  (entropy:")[0]
        assert len(password) == 24

    def test_length_via_kwarg(self, tool: PasswordTool) -> None:
        result = tool.process("", length=32)
        password = result.split("  (entropy:")[0]
        assert len(password) == 32

    def test_minimum_length_clamped_to_8(self, tool: PasswordTool) -> None:
        result = tool.process("4")
        password = result.split("  (entropy:")[0]
        assert len(password) == 8

    def test_maximum_length_clamped_to_128(self, tool: PasswordTool) -> None:
        result = tool.process("256")
        password = result.split("  (entropy:")[0]
        assert len(password) == 128


class TestPassphraseMode:
    def test_passphrase_via_input(self, tool: PasswordTool) -> None:
        result = tool.process("passphrase")
        # Passphrase is hyphen-separated words
        passphrase_line = result.split("\n")[0]
        words = passphrase_line.split("-")
        assert len(words) == 4  # default word count

    def test_passphrase_via_mode_kwarg(self, tool: PasswordTool) -> None:
        result = tool.process("", mode="passphrase")
        passphrase_line = result.split("\n")[0]
        words = passphrase_line.split("-")
        assert len(words) == 4

    def test_passphrase_custom_word_count(self, tool: PasswordTool) -> None:
        result = tool.process("passphrase", words=6)
        passphrase_line = result.split("\n")[0]
        words = passphrase_line.split("-")
        assert len(words) == 6

    def test_passphrase_contains_hyphens(self, tool: PasswordTool) -> None:
        result = tool.process("passphrase")
        passphrase_line = result.split("\n")[0]
        assert "-" in passphrase_line

    def test_passphrase_shows_entropy(self, tool: PasswordTool) -> None:
        result = tool.process("passphrase")
        assert "Entropy:" in result
        assert "bits" in result

    def test_passphrase_shows_word_count(self, tool: PasswordTool) -> None:
        result = tool.process("passphrase")
        assert "Words: 4" in result

    def test_passphrase_words_are_lowercase(self, tool: PasswordTool) -> None:
        result = tool.process("passphrase")
        passphrase_line = result.split("\n")[0]
        assert passphrase_line == passphrase_line.lower()


class TestEntropyCalculation:
    def test_entropy_present_in_output(self, tool: PasswordTool) -> None:
        result = tool.process("16")
        assert "entropy:" in result
        assert "bits" in result

    def test_entropy_increases_with_length(self, tool: PasswordTool) -> None:
        result_short = tool.process("8")
        result_long = tool.process("32")
        entropy_short = float(result_short.split("entropy: ")[1].split(" bits")[0])
        entropy_long = float(result_long.split("entropy: ")[1].split(" bits")[0])
        assert entropy_long > entropy_short


class TestPasswordUniqueness:
    def test_ten_passwords_are_unique(self, tool: PasswordTool) -> None:
        passwords = set()
        for _ in range(10):
            result = tool.process("16")
            password = result.split("  (entropy:")[0]
            passwords.add(password)
        assert len(passwords) == 10


class TestMultiplePasswords:
    def test_count_kwarg(self, tool: PasswordTool) -> None:
        result = tool.process("", count=5)
        lines = result.strip().split("\n")
        assert len(lines) == 5
        for line in lines:
            assert "entropy:" in line


class TestSecretsModule:
    def test_source_uses_secrets_not_random(self) -> None:
        """Verify the source file uses the secrets module, not random."""
        import inspect

        import gadgetbox.tools.password_tool as mod

        source = inspect.getsource(mod)
        assert "import secrets" in source
        assert "import random" not in source


class TestCharsetOptions:
    def test_digits_only(self, tool: PasswordTool) -> None:
        result = tool.process(
            "",
            length=16,
            uppercase=False,
            lowercase=False,
            digits=True,
            symbols=False,
        )
        password = result.split("  (entropy:")[0]
        assert password.isdigit()

    def test_letters_only(self, tool: PasswordTool) -> None:
        result = tool.process(
            "",
            length=16,
            uppercase=True,
            lowercase=True,
            digits=False,
            symbols=False,
        )
        password = result.split("  (entropy:")[0]
        assert password.isalpha()
