# Contributing to DevDash

Thanks for your interest in contributing! This guide explains how to report issues, suggest features, and submit code.

## Code of Conduct

We are committed to providing a welcoming and inclusive environment. All contributors must:

- Be respectful and constructive
- Welcome feedback and criticism
- Focus on ideas, not people
- Include people of all backgrounds and experience levels

Unacceptable behavior (harassment, discrimination, hostility) will not be tolerated and may result in removal.

## Reporting Bugs

Found a bug? Help us squash it.

### Before Submitting

1. Check [existing issues](https://github.com/devdash/devdash/issues) to avoid duplicates
2. Check if it's fixed in the latest version: `pip install --upgrade devdash`
3. Test with simple input to isolate the problem

### How to Report

Open a [GitHub issue](https://github.com/devdash/devdash/issues) with:

**Title:** Clear, one-line description
```
JSON Formatter crashes on large files
```

**Description:** Include as much detail as possible

```markdown
## Environment
- macOS version: Sonoma 14.2
- Python version: 3.12.1
- DevDash version: 0.1.0

## Steps to Reproduce
1. Open JSON Formatter
2. Paste a 50MB JSON file
3. Click "Format"

## Expected Behavior
The JSON should format or show an error message

## Actual Behavior
The app crashes silently, no error shown

## Additional Context
The file is valid JSON (tested with jq)
Smaller files (~1MB) work fine
```

### Good Bug Reports

- Minimal reproduction steps
- Expected vs. actual behavior
- Environment details
- Relevant logs or error messages

## Suggesting Features

Have an idea? We'd love to hear it.

### Before Suggesting

1. Check [existing issues](https://github.com/devdash/devdash/issues) for similar ideas
2. Make sure it fits DevDash's scope (developer utilities)
3. Consider if it should be a separate tool or built into existing one

### How to Suggest

Open a [GitHub discussion](https://github.com/devdash/devdash/discussions) or [issue](https://github.com/devdash/devdash/issues) with:

**Title:** Feature request or idea
```
Add YAML formatter tool
```

**Description:**

```markdown
## Use Case
I frequently work with YAML config files and would love to format and validate them without leaving DevDash.

## Proposed Solution
Add a YAML Formatter tool similar to JSON Formatter, with:
- Formatting (pretty-print)
- Validation (syntax check)
- Option to convert to JSON

## Examples
Input: `{name: John, age: 30}`
Output:
```yaml
name: John
age: 30
```

## Alternative Solutions
I could use a separate CLI tool, but it would be nicer to stay in DevDash.

## Additional Context
Popular YAML libraries: pyyaml, ruamel.yaml
```

## Pull Request Process

Ready to contribute code? Follow these steps.

### 1. Fork and Clone

```bash
# Fork on GitHub (click "Fork")
git clone https://github.com/YOUR_USERNAME/devdash.git
cd devdash
git remote add upstream https://github.com/devdash/devdash.git
```

### 2. Create a Branch

```bash
git checkout -b fix/issue-123-json-crash
# or
git checkout -b feature/add-yaml-tool
```

Use descriptive branch names: `fix/`, `feature/`, or `docs/`.

### 3. Make Changes

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Make your changes
# Edit files, add tests, etc.

# Run checks
pytest                    # Test your changes
ruff check src/          # Lint code
ruff format src/         # Auto-format
mypy src/devdash/        # Type check
```

### 4. Add Tests

All code changes should include tests.

**For a new tool:**
```bash
# Create tests/test_tools/test_my_tool.py
pytest tests/test_tools/test_my_tool.py -v
```

**For bug fixes:**
```bash
# Add test that reproduces the bug
# Verify it fails without your fix
# Verify it passes with your fix
pytest tests/ -v
```

**Test coverage:**
```bash
pytest --cov=src/devdash --cov-report=term-missing
```

Aim for >80% coverage on new code.

### 5. Commit

Write clear, concise commit messages:

```bash
git add src/devdash/tools/my_tool.py tests/test_tools/test_my_tool.py

git commit -m "Add YAML Formatter tool

- Formats and validates YAML files
- Supports conversion to JSON
- Includes comprehensive tests

Closes #123"
```

**Commit message guidelines:**
- First line: short description (50 chars max)
- Blank line
- Detailed explanation (if needed)
- Reference issues: "Closes #123" or "Fixes #456"

### 6. Keep Up to Date

Before pushing, sync with upstream:

```bash
git fetch upstream
git rebase upstream/main
```

### 7. Push and Open PR

```bash
git push origin fix/issue-123-json-crash
```

Then open a [pull request on GitHub](https://github.com/devdash/devdash/compare).

**PR Title:** Same as commit, clear and descriptive
```
Add YAML Formatter tool
```

**PR Description:**

```markdown
## Summary
Adds a new YAML Formatter tool for formatting and validating YAML files.

## Changes
- New tool: `src/devdash/tools/yaml_tool.py`
- Supports format, validate, and convert-to-JSON modes
- Comprehensive test coverage

## Testing
- All tests pass: `pytest tests/ -v`
- Manual testing on macOS Sonoma
- Tested with various YAML files (valid, invalid, edge cases)

## Checklist
- [x] Code follows style guidelines (ruff, black)
- [x] Tests added and passing
- [x] Type hints added (mypy strict)
- [x] Documentation updated (if needed)
- [x] No breaking changes

Closes #456
```

### 8. Review and Iterate

A maintainer will review your PR. They may ask for:
- Code style improvements
- Additional tests
- Documentation updates
- Design questions

Respond to feedback promptly. Push additional commits if changes are requested:

```bash
# Make changes
git add .
git commit -m "Address PR feedback: improve error handling"
git push
```

### 9. Merge

Once approved, a maintainer will merge your PR. Congratulations!

## Code Style

DevDash uses strict linting and type checking.

### Ruff (Linting and Formatting)

```bash
# Check
ruff check src/

# Auto-format
ruff format src/

# Fix issues automatically
ruff check --fix src/
```

**Configuration:** See `pyproject.toml`

**Target line length:** 100 characters

**Selected rules:** E (errors), F (PyFlakes), I (imports), N (naming), W (warnings), UP (upgrades)

### Type Hints (mypy)

All functions must have type annotations:

```python
# ✓ Good
def process(self, input_text: str, **kwargs: object) -> str:
    result: str = do_work(input_text)
    return result

# ✗ Bad
def process(self, input_text, kwargs):
    result = do_work(input_text)
    return result
```

Run type checker:

```bash
mypy src/devdash/
```

### Docstrings

Use docstrings for modules, classes, and public functions:

```python
"""Module docstring - one line summary."""

def my_function(arg1: str, arg2: int) -> str:
    """
    Function summary.

    Args:
        arg1: Description of arg1
        arg2: Description of arg2

    Returns:
        Description of return value

    Raises:
        ValueError: When arg2 is negative
    """
    pass
```

## Testing Guidelines

### Fixtures

Use pytest fixtures for reusable test setup:

```python
import pytest
from devdash.tools.my_tool import MyTool

@pytest.fixture
def tool() -> MyTool:
    """Provide a fresh tool instance."""
    return MyTool()

def test_something(tool: MyTool) -> None:
    """Test something with the tool."""
    assert tool.name == "My Tool"
```

### Test Coverage

Aim for high coverage, especially on:
- Happy path (normal usage)
- Error handling (invalid input)
- Edge cases (empty input, large input, special chars)

```bash
pytest --cov=src/devdash --cov-report=term-missing
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_tools/test_my_tool.py

# Run with verbose output
pytest -v

# Run with output on failure
pytest -vvs

# Stop on first failure
pytest -x

# Run specific test function
pytest tests/test_tools/test_my_tool.py::test_process_basic
```

## Documentation

Update documentation for:
- New tools → Add to [docs/usage.md](docs/usage.md) and [README.md](README.md)
- New features → Update relevant docs
- Breaking changes → Update [CHANGELOG.md](CHANGELOG.md)
- Code changes → Update docstrings and inline comments

## Changelog

For user-visible changes, add entry to [CHANGELOG.md](CHANGELOG.md).

Format:

```markdown
## [Unreleased]

### Added
- New YAML Formatter tool with validation support

### Fixed
- JSON Formatter crash on files >50MB (#123)

### Changed
- Improved error messages in all tools
```

Follow [Keep a Changelog](https://keepachangelog.com/) format:
- **Added** — New features
- **Changed** — Behavior changes to existing features
- **Deprecated** — Soon-to-be-removed features
- **Removed** — Deleted features
- **Fixed** — Bug fixes
- **Security** — Security-related changes

## Development Setup

### Requirements

- Python 3.10+
- Git
- macOS (development and testing)

### Install Dev Environment

```bash
git clone https://github.com/devdash/devdash.git
cd devdash
pip install -e ".[dev]"
```

This installs:
- devdash (editable)
- pytest, pytest-cov
- ruff
- mypy
- pre-commit

### Pre-commit Hooks (Optional)

Set up automatic linting/formatting on commit:

```bash
pre-commit install
```

Then on each `git commit`, pre-commit will:
- Run ruff check and format
- Check type hints
- Verify tests pass

## Getting Help

- **Issues:** Open a [GitHub issue](https://github.com/devdash/devdash/issues)
- **Discussions:** Join the [GitHub discussions](https://github.com/devdash/devdash/discussions)
- **Email:** Contact maintainers (see MAINTAINERS.md)

## Recognition

Contributors are recognized in:
- GitHub contributors page
- Release notes
- CONTRIBUTORS.md file (if created)

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).

---

Thanks for contributing to DevDash! 🙌
