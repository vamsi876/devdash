# Adding a New Tool

DevDash uses a plugin system that makes adding new tools straightforward. This guide walks you through creating a tool from scratch.

## Overview

Each tool is a Python module in `src/devdash/tools/` that:
1. Extends `DevTool` base class
2. Implements required properties and methods
3. Exports a `register()` function

The plugin loader automatically discovers and loads all tools.

## Step 1: Create the Tool File

Create a new file in `src/devdash/tools/` named after your tool, like `src/devdash/tools/my_tool.py`.

## Step 2: Extend DevTool

Import the base class and create your tool:

```python
"""My Tool - A super useful developer tool."""

from devdash.tools.base import DevTool


class MyTool(DevTool):
    """Description of what this tool does."""

    @property
    def name(self) -> str:
        """Display name shown in the menu."""
        return "My Tool"

    @property
    def keyword(self) -> str:
        """Short identifier for auto-detection and CLI."""
        return "mytool"

    @property
    def category(self) -> str:
        """Menu category. Examples: Formatters, Generators, Converters."""
        return "Utilities"

    @property
    def description(self) -> str:
        """Optional one-line description shown in tooltips."""
        return "Does something useful"

    def process(self, input_text: str, **kwargs: object) -> str:
        """
        Process input and return output string.

        Args:
            input_text: User input text
            **kwargs: Optional parameters (e.g., mode, format, count)

        Returns:
            Processed result or error message
        """
        if not input_text.strip():
            return "Error: Please provide input"

        # Your processing logic here
        result = input_text.upper()
        return result

    def validate(self, input_text: str) -> str | None:
        """
        Optional validation before processing.

        Return error message if invalid, None if valid.
        """
        if not input_text:
            return "Input cannot be empty"
        return None


def register() -> DevTool:
    """Required: Return an instance of your tool."""
    return MyTool()
```

## Step 3: Implement Required Methods

### `name` property

The display name users see in the menu. Keep it short and descriptive.

```python
@property
def name(self) -> str:
    return "JSON Formatter"
```

### `keyword` property

A short identifier used for:
- Auto-detection matching
- CLI invocation (future feature)
- Internal tool identification

Use lowercase, no spaces or special characters.

```python
@property
def keyword(self) -> str:
    return "json"
```

### `category` property (Optional)

Group related tools in the menu. Examples:
- "Formatters" — JSON, YAML formatting
- "Generators" — UUID, Password generation
- "Converters" — Timestamp, Color conversion
- "Utilities" — Regex, Cron parsing

```python
@property
def category(self) -> str:
    return "Formatters"
```

Default is "General" if not overridden.

### `description` property (Optional)

A one-line description for tooltips and help text.

```python
@property
def description(self) -> str:
    return "Format, validate, or minify JSON"
```

### `process()` method

The core logic. Takes input and returns output.

```python
def process(self, input_text: str, **kwargs: object) -> str:
    """
    Args:
        input_text: The user's input
        **kwargs: Optional parameters from the UI

    Returns:
        Output string. Can include error messages.
    """
    # Handle empty input
    if not input_text.strip():
        return "Error: Empty input"

    # Process
    try:
        result = do_something(input_text)
        return result
    except Exception as e:
        return f"Error: {str(e)}"
```

**Best practices:**
- Always handle empty input gracefully
- Return clear error messages (start with "Error: ")
- Support multiple modes via `kwargs` (e.g., `kwargs.get("mode")`)
- Return results as plain text (the UI handles display)

### `validate()` method (Optional)

Pre-validate input before processing. Useful for expensive operations.

```python
def validate(self, input_text: str) -> str | None:
    """
    Return error message if invalid, None if valid.
    """
    if not json.valid(input_text):
        return "Invalid JSON format"
    return None
```

### `register()` function

Export your tool for discovery:

```python
def register() -> DevTool:
    return MyTool()
```

The plugin loader calls this to get your tool instance.

## Complete Example: Simple Text Reverser

Here's a minimal working tool:

```python
"""Text Reverser - Reverse input text."""

from devdash.tools.base import DevTool


class TextReverserTool(DevTool):
    """Reverses input text."""

    @property
    def name(self) -> str:
        return "Text Reverser"

    @property
    def keyword(self) -> str:
        return "reverse"

    @property
    def category(self) -> str:
        return "Text Tools"

    @property
    def description(self) -> str:
        return "Reverse input text"

    def process(self, input_text: str, **kwargs: object) -> str:
        """Reverse the input text."""
        if not input_text.strip():
            return "Error: Empty input"

        preserve_case = bool(kwargs.get("preserve_case", False))
        text = input_text.strip()

        if preserve_case:
            reversed_text = text[::-1]
        else:
            reversed_text = text[::-1].lower()

        return reversed_text

    def validate(self, input_text: str) -> str | None:
        """Input is valid if non-empty."""
        if not input_text.strip():
            return "Please provide text to reverse"
        return None


def register() -> DevTool:
    return TextReverserTool()
```

## Step 4: Write Tests

Create `tests/test_tools/test_mytool.py`:

```python
"""Tests for MyTool."""

import pytest
from devdash.tools.my_tool import MyTool


@pytest.fixture
def tool() -> MyTool:
    """Fixture providing a tool instance."""
    return MyTool()


def test_name(tool: MyTool) -> None:
    """Tool has correct name."""
    assert tool.name == "My Tool"


def test_keyword(tool: MyTool) -> None:
    """Tool has correct keyword."""
    assert tool.keyword == "mytool"


def test_process_basic(tool: MyTool) -> None:
    """Basic processing works."""
    result = tool.process("hello")
    assert result == "HELLO"


def test_process_empty(tool: MyTool) -> None:
    """Empty input returns error."""
    result = tool.process("")
    assert "Error" in result


def test_validate_empty(tool: MyTool) -> None:
    """Validation rejects empty input."""
    error = tool.validate("")
    assert error is not None


def test_validate_valid(tool: MyTool) -> None:
    """Validation accepts valid input."""
    error = tool.validate("hello")
    assert error is None
```

Run tests:

```bash
pytest tests/test_tools/test_mytool.py -v
```

## Step 5: Verify Discovery

The plugin loader should automatically find your tool. Test it:

```bash
python3 -c "from devdash.plugin_loader import discover_tools; print([t.name for t in discover_tools()])"
```

Your tool's name should appear in the list.

## Advanced Patterns

### Supporting Multiple Modes

Tools can support different operations via kwargs:

```python
def process(self, input_text: str, **kwargs: object) -> str:
    mode = str(kwargs.get("mode", "default"))

    if mode == "format":
        return self._format(input_text)
    elif mode == "minify":
        return self._minify(input_text)
    elif mode == "validate":
        return self._validate(input_text)
    else:
        return "Error: Unknown mode"

def _format(self, text: str) -> str:
    # Implementation
    pass

def _minify(self, text: str) -> str:
    # Implementation
    pass

def _validate(self, text: str) -> str:
    # Implementation
    pass
```

### Using Configuration

Access user config via `devdash.config`:

```python
from devdash.config import load_config

def process(self, input_text: str, **kwargs: object) -> str:
    config = load_config()
    algorithm = config.get("default_hash_algorithm", "sha256")
    # Use algorithm
    pass
```

### Handling Large Input

For expensive operations, provide feedback:

```python
def process(self, input_text: str, **kwargs: object) -> str:
    if len(input_text) > 10_000_000:
        return "Error: Input too large (>10MB)"

    # Process...
    pass
```

## Type Hints

DevDash uses strict type checking. Always annotate parameters and returns:

```python
from typing import Any

def process(self, input_text: str, **kwargs: Any) -> str:
    # ✓ Good - explicitly typed
    pass

def process(self, input_text, kwargs):
    # ✗ Bad - no type hints
    pass
```

Run the type checker:

```bash
mypy src/devdash/tools/my_tool.py
```

## Code Style

DevDash uses [ruff](https://github.com/charliermarsh/ruff) for linting. Format your code:

```bash
ruff format src/devdash/tools/my_tool.py
ruff check --fix src/devdash/tools/my_tool.py
```

Target line length: 100 characters.

## Publishing Your Tool

To contribute your tool to DevDash:

1. Create a fork: `git clone https://github.com/devdash/devdash.git`
2. Create a branch: `git checkout -b add-mytool`
3. Write the tool + tests
4. Submit a pull request

See [CONTRIBUTING.md](../CONTRIBUTING.md) for the full process.

## Troubleshooting

### Tool doesn't appear in menu

1. Check that `register()` function exists
2. Verify the module name doesn't start with underscore
3. Check for import errors:
   ```bash
   python3 -c "from devdash.tools.my_tool import register; register()"
   ```

### Tests fail

- Ensure fixtures are properly defined
- Use `pytest -v` for detailed output
- Check type annotations with mypy

### Performance issues

- Optimize expensive operations (caching, lazy loading)
- Test with large inputs
- Consider adding input size limits

## See Also

- [Architecture Guide](architecture.md) — How DevDash works internally
- [CONTRIBUTING.md](../CONTRIBUTING.md) — Code style and PR process
- [Existing Tools](../src/devdash/tools/) — Reference implementations
