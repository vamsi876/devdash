# DevDash: Open-Source macOS Menubar Developer Utilities

## Project Overview

Build **DevDash**, an open-source macOS menubar app built with Python (using the `rumps` library) that gives developers instant access to everyday utilities without leaving their workflow. Think of it as the **open-source alternative to DevUtils ($14 paid app)**, installable via `pip install devdash`.

The app sits in the macOS menubar as a single icon. Clicking it reveals a dropdown menu of developer tools. Each tool opens a small `rumps.Window` dialog for input/output. Everything runs offline, uses Python standard libraries, and requires zero API keys or accounts.

---

## Architecture

```
devdash/
├── pyproject.toml              # Package config (pip installable)
├── setup.cfg
├── README.md                   # GitHub README with GIF demo
├── LICENSE                     # MIT License
├── CONTRIBUTING.md
├── docs/
│   ├── installation.md
│   ├── usage.md
│   ├── adding-tools.md         # Guide for contributors
│   └── architecture.md
├── src/
│   └── devdash/
│       ├── __init__.py         # Version and package metadata
│       ├── __main__.py         # Entry point: `python -m devdash`
│       ├── app.py              # Main rumps.App class, menubar setup
│       ├── config.py           # User preferences (YAML based)
│       ├── clipboard.py        # Clipboard read/write + auto-detection
│       ├── plugin_loader.py    # Dynamic tool discovery and registration
│       ├── tools/
│       │   ├── __init__.py     # Tool registry
│       │   ├── base.py         # Abstract base class for all tools
│       │   ├── json_tool.py    # JSON formatter / validator / minifier
│       │   ├── jwt_tool.py     # JWT decoder (header + payload + expiry check)
│       │   ├── uuid_tool.py    # UUID v4 / v7 / ULID generator
│       │   ├── base64_tool.py  # Base64 encode / decode
│       │   ├── hash_tool.py    # MD5, SHA-1, SHA-256, SHA-512 generator
│       │   ├── timestamp_tool.py   # Unix timestamp <-> human date converter
│       │   ├── url_tool.py     # URL encode / decode
│       │   ├── regex_tool.py   # Regex tester with live match highlighting
│       │   ├── color_tool.py   # HEX <-> RGB <-> HSL converter
│       │   ├── lorem_tool.py   # Lorem ipsum generator (words/sentences/paragraphs)
│       │   ├── password_tool.py    # Secure password generator (configurable)
│       │   └── cron_tool.py    # Cron expression to human-readable converter
│       └── ui/
│           ├── __init__.py
│           ├── windows.py      # Custom rumps.Window wrappers
│           └── notifications.py # macOS native notifications helper
├── tests/
│   ├── conftest.py             # Shared fixtures
│   ├── test_tools/
│   │   ├── test_json_tool.py
│   │   ├── test_jwt_tool.py
│   │   ├── test_uuid_tool.py
│   │   ├── test_base64_tool.py
│   │   ├── test_hash_tool.py
│   │   ├── test_timestamp_tool.py
│   │   ├── test_url_tool.py
│   │   ├── test_regex_tool.py
│   │   ├── test_color_tool.py
│   │   ├── test_lorem_tool.py
│   │   ├── test_password_tool.py
│   │   └── test_cron_tool.py
│   ├── test_clipboard.py
│   ├── test_plugin_loader.py
│   ├── test_config.py
│   └── test_app.py             # Integration tests for menubar
├── .github/
│   └── workflows/
│       ├── ci.yml              # Run tests on every PR
│       ├── release.yml         # Auto-publish to PyPI on tag
│       └── lint.yml            # Ruff + mypy checks
├── .gitignore
├── .pre-commit-config.yaml
└── Makefile                    # dev commands: make test, make lint, make run
```

---

## Agent Task Assignments

### @orchestrator

You are the project lead. Coordinate all agents below. Follow this execution order:

**Phase 1: Foundation (parallel)**

1. Tell `@package-agent` to set up pyproject.toml, dependencies, and the pip-installable package structure
2. Tell `@backend-agent` to build the core app framework (app.py, plugin_loader.py, base tool class, clipboard module)
3. Tell `@devops-agent` to set up GitHub Actions CI/CD, pre-commit hooks, Makefile, and linting config

**Phase 2: Tools (parallel, after Phase 1)**
4. Tell `@backend-agent` to implement all 12 tools in src/devdash/tools/ following the base class pattern
5. Tell `@testing-agent` to write comprehensive tests for every tool as they are completed
6. Tell `@codebase-auditor` to review code quality, consistency, and architecture after each batch

**Phase 3: Polish (parallel, after Phase 2)**
7. Tell `@docs-agent` to generate all documentation (README, installation guide, usage guide, contributor guide, architecture doc)
8. Tell `@elite-recruiter-reviewer` to do a final full code review as if evaluating a senior engineer's portfolio piece
9. Tell `@devops-agent` to finalize the PyPI release workflow and ensure `pip install devdash` works end-to-end

**Phase 4: Bonus**
10. Tell `@frontend-agent` to create a stunning GitHub landing page (static HTML) for the project at docs/index.html
11. Tell `@extension-agent` to implement the smart clipboard detection feature (auto-detect if clipboard has JSON, JWT, timestamp, UUID and suggest the right tool)

After each phase, ask `@codebase-auditor` to audit the new code before moving to the next phase.

---

### @package-agent

Set up the Python package structure for a pip-installable macOS menubar app:

- Create `pyproject.toml` with:
  - Project name: `devdash`
  - Python version: `>=3.10`
  - Dependencies: `rumps>=0.4.0`, `pyperclip>=1.8.0`, `PyJWT>=2.8.0`, `pyyaml>=6.0`, `croniter>=1.3.0`
  - Dev dependencies: `pytest>=7.0`, `pytest-cov`, `ruff`, `mypy`, `pre-commit`
  - Entry point console script: `devdash = devdash.__main__:main`
  - Classifiers for macOS, Python 3.10-3.13, Development Status 4 - Beta, MIT License
- Create `setup.cfg` with tool configs for ruff (line-length=100, target Python 3.10), mypy (strict mode), pytest (testpaths=tests, cov=src/devdash)
- Create `.gitignore` for Python (include .eggs, dist, build, **pycache**, .mypy_cache, .pytest_cache, .venv, *.egg-info)
- Create `Makefile` with targets: `install`, `dev`, `run`, `test`, `lint`, `format`, `clean`, `build`, `publish`
- Ensure the package can be installed with `pip install -e .` for development and `pip install devdash` from PyPI

---

### @backend-agent

Build the core application framework and all developer tools:

**Core Framework:**

1. `src/devdash/__init__.py`: Package metadata with `__version__ = "0.1.0"` and `__app_name__ = "DevDash"`
2. `src/devdash/__main__.py`: Entry point that creates and starts the rumps App
3. `src/devdash/app.py`: Main application class extending `rumps.App`:
  - Title icon: Use a wrench emoji or unicode character as the menubar icon
  - Dynamic menu built from discovered tools via plugin_loader
  - Each tool appears as a menu item with a keyboard-style label
  - "Clipboard: Auto-detect" option at the top that reads clipboard and opens the matching tool
  - "Settings" submenu for user preferences
  - "About DevDash" and "Quit" at the bottom
  - Use `rumps.timer` for any periodic tasks (like clipboard watching)
  - All callbacks should be non-blocking
4. `src/devdash/plugin_loader.py`: Dynamic tool discovery:
  - Scan the `tools/` directory for modules
  - Each module registers itself via a `register()` function returning a tool instance
  - Tools are sorted by category for menu organization
  - Support for future user-created plugin directories
5. `src/devdash/clipboard.py`: Clipboard utilities:
  - `read()`: Get current clipboard content as string
  - `write(text)`: Write string to clipboard
  - `detect_type(text)`: Auto-detect if content is JSON, JWT, UUID, Base64, URL, Unix timestamp, or cron expression
  - Return a `ContentType` enum
6. `src/devdash/config.py`: User preferences:
  - YAML config file at `~/.config/devdash/config.yaml`
  - Settings: default_hash_algorithm, timestamp_format, password_length, uuid_version, auto_clipboard_detection (bool)
  - Create default config on first run
  - Thread-safe read/write

**Tool Base Class (`src/devdash/tools/base.py`):**

```python
from abc import ABC, abstractmethod
from typing import Optional

class DevTool(ABC):
    """Base class for all DevDash tools."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Display name in the menu."""
        ...

    @property
    @abstractmethod
    def keyword(self) -> str:
        """Short identifier for CLI and auto-detection."""
        ...

    @property
    def category(self) -> str:
        """Menu category grouping."""
        return "General"

    @property
    def description(self) -> str:
        """One-line description shown in tooltip."""
        return ""

    @abstractmethod
    def process(self, input_text: str) -> str:
        """Process input and return output string."""
        ...

    def validate(self, input_text: str) -> Optional[str]:
        """Validate input. Return error message or None if valid."""
        return None
```

**Implement these 12 tools:**

1. **json_tool.py**: JSON Formatter / Validator / Minifier
  - `process()` with mode param: format (pretty-print with 2-space indent), validate (check syntax and report errors with line numbers), minify (compact single line)
  - Handle common issues: trailing commas, single quotes, unquoted keys (provide helpful error messages)
  - Use `json` standard library
2. **jwt_tool.py**: JWT Decoder
  - Decode header and payload without verification (using PyJWT's decode with verify=False)
  - Display: header (algorithm, type), payload (all claims), and importantly: issued-at, expiration, and whether the token is expired
  - Color-code or mark expired tokens clearly
  - Handle malformed JWTs gracefully with clear error messages
3. **uuid_tool.py**: UUID / ULID Generator
  - Generate UUID v4 (random), UUID v7 (timestamp-based, if Python 3.12+, else fallback implementation), and ULID
  - Option to generate multiple at once (1, 5, 10)
  - Option to output uppercase or lowercase
  - Validate if a given string is a valid UUID
4. **base64_tool.py**: Base64 Encode / Decode
  - Encode string to Base64
  - Decode Base64 to string
  - Auto-detect direction (if input is valid Base64, offer to decode; otherwise encode)
  - Handle URL-safe Base64 variant
  - Show byte length of encoded/decoded content
5. **hash_tool.py**: Hash Generator
  - Support: MD5, SHA-1, SHA-256, SHA-512, BLAKE2b
  - Input: any text string
  - Output: all hashes at once, or single selected algorithm
  - Option for HMAC hashing with a key
  - Use `hashlib` standard library
6. **timestamp_tool.py**: Unix Timestamp Converter
  - Unix timestamp (seconds or milliseconds) to human-readable date
  - Human-readable date to Unix timestamp
  - Auto-detect if input is a timestamp or a date string
  - Show result in multiple timezones: UTC, local, and user-configurable
  - Show relative time ("3 days ago", "in 2 hours")
  - Use `datetime` and `zoneinfo` standard libraries
7. **url_tool.py**: URL Encode / Decode
  - URL-encode a string (for query params)
  - URL-decode an encoded string
  - Parse URL into components (scheme, host, path, query params, fragment)
  - Auto-detect direction
  - Use `urllib.parse` standard library
8. **regex_tool.py**: Regex Tester
  - Input: regex pattern + test string
  - Output: all matches with group captures, match positions
  - Validate the regex pattern and show clear errors for invalid patterns
  - Show named groups if present
  - Common regex presets: email, URL, IPv4, phone number, date
  - Use `re` standard library
9. **color_tool.py**: Color Converter
  - Convert between HEX, RGB, HSL, and HSV
  - Input any format, auto-detect and convert to all others
  - Validate color values (hex must be 3 or 6 chars, RGB 0-255, etc.)
  - Show complementary color
  - Use `colorsys` standard library
10. **lorem_tool.py**: Lorem Ipsum Generator
  - Generate by: words (count), sentences (count), or paragraphs (count)
    - Classic Lorem Ipsum text, not random gibberish
    - Option for "shorter" sentences for UI mockup text
    - Copy directly to clipboard on generate
11. **password_tool.py**: Password Generator
  - Configurable: length (8-128), include uppercase, lowercase, digits, symbols
    - Passphrase mode: generate 4-8 random dictionary words separated by hyphens
    - Show password strength estimate (entropy bits)
    - Generate multiple at once
    - Use `secrets` module (cryptographically secure)
12. **cron_tool.py**: Cron Expression Parser
  - Parse cron expression to human-readable description ("At 03:00 on every Monday")
    - Show next 5 scheduled run times
    - Validate cron syntax with clear error messages
    - Common presets: every minute, hourly, daily at midnight, weekly on Monday, monthly on 1st
    - Use `croniter` library

**UI Module (`src/devdash/ui/`):**

1. `windows.py`: Custom window helpers:
  - `ToolWindow`: A wrapper around `rumps.Window` with consistent styling, title, input field, and output display
  - `MultiInputWindow`: For tools needing multiple inputs (regex: pattern + test string)
  - Handle copy-to-clipboard button on all output windows
2. `notifications.py`: macOS notification helper:
  - Wrapper around `rumps.notification()` for consistent notification style
  - "Copied to clipboard" notifications
  - Error notifications

---

### @testing-agent

Write comprehensive tests for every component. Target **95%+ code coverage**.

**Testing Strategy:**

- Use `pytest` as the test runner
- Use `pytest-cov` for coverage reporting
- Mock `rumps` components since tests run in CI without macOS GUI
- Mock clipboard operations with `unittest.mock.patch`
- Each tool gets its own test file with edge cases

**Test Requirements per Tool:**

For EVERY tool test file, include:

1. **Happy path tests**: Valid input produces correct output
2. **Edge cases**: Empty string, very long input, unicode characters, special characters
3. **Error handling**: Invalid input produces helpful error message (not a crash)
4. **Roundtrip tests** (where applicable): encode then decode returns original

**Specific test scenarios:**

- `test_json_tool.py`: Valid JSON formatting, invalid JSON with helpful error, nested objects, arrays, unicode strings, numbers with precision, null values, empty objects/arrays, JSON with comments (should error gracefully), extremely large JSON (10MB+), minification removes all whitespace
- `test_jwt_tool.py`: Valid JWT with all standard claims, expired JWT detection, JWT with custom claims, malformed JWT (missing parts, bad base64), JWT with different algorithms in header, token with no expiration
- `test_uuid_tool.py`: UUID v4 format validation (8-4-4-4-12), UUID v4 uniqueness (generate 1000 and check no duplicates), valid UUID string detection, invalid UUID detection, uppercase/lowercase options
- `test_base64_tool.py`: Encode/decode roundtrip, URL-safe variant, binary-like content, empty string, padding edge cases, invalid Base64 detection
- `test_hash_tool.py`: Known hash values (hash of "hello" with SHA-256 should equal known digest), all algorithms produce different outputs, empty string hashing, HMAC with key, very long input
- `test_timestamp_tool.py`: Known timestamp conversions (0 = 1970-01-01), millisecond vs second detection, future dates, negative timestamps (before 1970), timezone conversions, relative time strings
- `test_url_tool.py`: Encode/decode roundtrip, URL parsing with all components, URLs with unicode, empty query params, URLs with fragments, malformed URLs
- `test_regex_tool.py`: Simple patterns, group captures, named groups, invalid regex patterns (should return error not crash), common presets produce valid regex, backtracking edge cases
- `test_color_tool.py`: HEX to RGB known values (#FF0000 = 255,0,0), RGB to HSL roundtrip, invalid hex values, 3-char hex expansion, case insensitivity
- `test_lorem_tool.py`: Word count accuracy, sentence count, paragraph count, output is actual Latin-ish text not random chars
- `test_password_tool.py`: Length is correct, character sets are respected, entropy calculation is correct, passphrase word count is correct, passwords are unique across generations, cryptographic randomness (no `random` module, only `secrets`)
- `test_cron_tool.py`: Standard expressions ("0 * * * *" = "Every hour at minute 0"), invalid expressions, next run time calculation, edge cases (Feb 29, DST transitions)

**Also write:**

- `test_clipboard.py`: Content type detection (JSON, JWT, UUID, Base64, URL, timestamp, cron), empty clipboard, binary content
- `test_plugin_loader.py`: Discovers all tools in directory, handles missing tools gracefully, tool ordering by category
- `test_config.py`: Default config creation, config read/write, missing config file handling, corrupt YAML handling
- `test_app.py`: Integration test that the app initializes, menu items are correct, tool callbacks work
- `conftest.py`: Shared fixtures for common test data (sample JWTs, JSON strings, UUIDs, etc.)

---

### @devops-agent

Set up the full CI/CD pipeline and development tooling:

1. `**.github/workflows/ci.yml`**: Run on every push and PR to main:
  - Matrix: Python 3.10, 3.11, 3.12, 3.13
  - OS: macos-latest (primary), ubuntu-latest (for non-GUI unit tests)
  - Steps: install deps, run ruff lint, run mypy type check, run pytest with coverage, upload coverage to codecov
  - Fail if coverage drops below 90%
2. `**.github/workflows/release.yml**`: Triggered on git tag push (v*):
  - Build sdist and wheel
  - Publish to PyPI using trusted publishing (OIDC)
  - Create GitHub Release with auto-generated changelog
3. `**.github/workflows/lint.yml*`*: Run ruff and mypy on every PR:
  - Annotate PR with linting errors
  - Block merge if linting fails
4. `**.pre-commit-config.yaml**`: Pre-commit hooks:
  - ruff (lint + format)
  - mypy
  - check-yaml
  - end-of-file-fixer
  - trailing-whitespace
  - check-added-large-files
5. `**Makefile**` with these targets:
  ```makefile
   install:      pip install -e .
   dev:          pip install -e ".[dev]"
   run:          python -m devdash
   test:         pytest --cov=src/devdash --cov-report=term-missing
   lint:         ruff check src/ tests/
   format:       ruff format src/ tests/
   typecheck:    mypy src/devdash
   clean:        rm -rf build dist *.egg-info .pytest_cache .mypy_cache
   build:        python -m build
   publish-test: twine upload --repository testpypi dist/*
   publish:      twine upload dist/*
   all:          lint typecheck test
  ```

---

### @docs-agent

Write all project documentation:

1. `**README.md**`: This is THE most important file for GitHub stars. Structure:
  - Hero section: Project name, one-line description, badges (PyPI version, Python versions, CI status, license, stars)
  - **[PLACEHOLDER FOR GIF]**: Note where a demo GIF should go showing the menubar in action
  - "Why DevDash?" section: 3 bullet points on the problem it solves
  - Quick install: `pip install devdash` then `devdash` to run
  - Tool list with emoji icons and one-line descriptions for each of the 12 tools
  - "Smart Clipboard" feature explanation
  - Configuration section
  - Contributing section (link to CONTRIBUTING.md)
  - "Built With" section: rumps, Python standard library
  - License: MIT
  - "Star History" placeholder
  - Keep it scannable, no walls of text
2. `**docs/installation.md`**: Installation guide:
  - pip install (recommended)
  - Install from source (git clone + pip install -e .)
  - Homebrew (future, add placeholder)
  - macOS permissions (accessibility permissions for clipboard, if needed)
  - Troubleshooting common install issues
3. `**docs/usage.md**`: Usage guide:
  - Starting the app
  - Each tool with example input/output
  - Smart clipboard auto-detection
  - Configuration options
  - Keyboard shortcuts (if applicable)
4. `**docs/adding-tools.md**`: Contributor guide for adding new tools:
  - Step-by-step: create file in tools/, extend DevTool base class, implement required methods
  - Example tool implementation (complete code)
  - Testing requirements
  - PR checklist
5. `**docs/architecture.md**`: Technical architecture:
  - System overview diagram (text-based)
  - Plugin system explanation
  - How rumps works
  - Config management
  - Clipboard detection algorithm
6. `**CONTRIBUTING.md**`: Standard contributing guide:
  - Code of conduct
  - How to report bugs
  - How to suggest features
  - PR process
  - Code style (ruff config)
  - Testing requirements
7. `**LICENSE**`: MIT License

---

### @codebase-auditor

After each phase, audit the codebase for:

1. **Code consistency**: All tools follow the same pattern, naming conventions are consistent, imports are organized
2. **Type safety**: All functions have type hints, mypy passes with strict mode
3. **Error handling**: No bare except clauses, all user-facing errors are descriptive, no crashes on bad input
4. **Security**: Password generation uses `secrets` not `random`, no eval/exec on user input, clipboard data is treated as untrusted
5. **Performance**: No blocking operations in the main thread, tools that process large input handle it efficiently
6. **DRY**: No duplicated logic between tools, shared utilities are extracted
7. **Architecture**: Plugin system is clean, circular imports are avoided, separation of concerns is maintained
8. **Python best practices**: Dataclasses where appropriate, enums for fixed choices, context managers for resources

Store findings in project memory for tracking across phases.

---

### @frontend-agent

Create a beautiful static landing page at `docs/index.html` for the GitHub Pages site:

- Design aesthetic: Clean, developer-focused, dark theme with syntax-highlighting inspired accents
- Hero: Large project name, one-liner, animated terminal showing `pip install devdash` and the app launching
- Features grid: Icon + title + description for each tool category
- Installation section with copy-to-clipboard code blocks
- Footer with GitHub link, stars badge, license
- Fully responsive, single HTML file with embedded CSS
- No external dependencies (no Tailwind CDN, no React, pure HTML/CSS/JS)
- Must feel premium and polished, not generic

---

### @extension-agent

Implement the "Smart Clipboard" feature, the key differentiator:

Build the auto-detection system in `src/devdash/clipboard.py`:

```
Detection priority order:
1. JWT: Starts with "eyJ" and has exactly 2 dots
2. JSON: Starts with { or [ and is valid JSON
3. UUID: Matches UUID regex pattern (8-4-4-4-12 hex)
4. Cron: Matches cron pattern (5 or 6 space-separated fields with * or numbers)
5. URL-encoded: Contains %XX patterns
6. Base64: Matches Base64 character set and length is multiple of 4
7. Unix Timestamp: Pure digits, 10 or 13 chars, within reasonable range
8. HEX Color: Starts with # followed by 3 or 6 hex chars
9. URL: Starts with http:// or https://
10. Fallback: Plain text (no auto-suggestion)
```

When the user clicks "Clipboard: Auto-detect" in the menu:

1. Read clipboard content
2. Run detection algorithm
3. Open the matching tool with content pre-filled
4. If multiple types match, show a submenu letting the user choose

Also implement a background clipboard watcher (optional, disabled by default):

- Poll clipboard every 2 seconds via `rumps.timer`
- When developer content is detected, show a subtle notification: "DevDash detected JSON in your clipboard. Click to format."
- Must be opt-in only (privacy conscious)

---

### @auth-agent

This project has no authentication layer. However, contribute by:

1. Ensure the `password_tool.py` uses `secrets` module exclusively (never `random`)
2. Ensure the `hash_tool.py` HMAC implementation is cryptographically correct
3. Review the `config.py` to ensure config files have proper file permissions (0o600 for files containing any user preferences)
4. Review the JWT decoder to ensure it NEVER attempts to verify signatures (it's a decoder, not a validator, and should explicitly warn users about this)
5. Ensure clipboard data is never logged or persisted to disk
6. Add security notes to the README about what DevDash does and does NOT do with user data

---

### @database-agent

This project uses no database. However, contribute by:

1. If any tool needs persistent storage (like "recent conversions" or "favorite regex patterns"), design a lightweight SQLite schema in `src/devdash/storage.py`
2. Keep it optional and off by default
3. Storage location: `~/.config/devdash/history.db`
4. Tables: `tool_history` (id, tool_name, input_preview, output_preview, timestamp), `favorites` (id, tool_name, label, content)
5. Auto-cleanup: keep only last 100 entries per tool
6. Implement as a mixin that tools can optionally use

---

## Success Criteria

The project is DONE when:

- `pip install devdash` works and launches a menubar app
- All 12 tools work correctly with proper error handling
- Smart clipboard detection works for all supported types
- Test coverage is above 90%
- CI passes on Python 3.10, 3.11, 3.12, 3.13
- README is polished and GitHub-star-worthy
- All docs are complete and accurate
- Code passes ruff lint and mypy strict mode
- `@elite-recruiter-reviewer` rates every category 8/10 or above
- A contributor can add a new tool by following the guide in under 15 minutes

---

## Important Notes

- **Never use `random` module for anything security-related.** Always use `secrets`.
- **All tools must handle empty string input gracefully** (not crash, show helpful message).
- **All tools must handle extremely large input** (10MB+) without freezing the menubar.
- **rumps.Window has limitations**: It's a simple text input/output dialog. Don't try to build complex UIs. Keep tool interactions to: input text -> click OK -> see output.
- **macOS specific**: This app only runs on macOS. Make this clear in docs and package classifiers.
- **Keep dependencies minimal**: Only add a pip dependency if there's no reasonable stdlib alternative.

