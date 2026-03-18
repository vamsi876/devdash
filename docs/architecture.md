# Architecture Guide

DevDash is built with simplicity and extensibility in mind. This guide explains the design and how components fit together.

## High-Level Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     DevDash Application                      │
├─────────────────────────────────────────────────────────────┤
│                        rumps (macOS UI)                      │
├─────────────────────────────────────────────────────────────┤
│                      Plugin System                           │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│   │ JSON Formatter│  │ UUID Generator│  │ ... (9 more) │     │
│   └──────────────┘  └──────────────┘  └──────────────┘     │
├─────────────────────────────────────────────────────────────┤
│          Shared Services: Clipboard, Config, UI             │
└─────────────────────────────────────────────────────────────┘
```

## Core Modules

### app.py — Main Application

The entry point and UI controller:

```python
class DevDashApp(rumps.App):
    """macOS menubar developer utilities app."""
```

Responsibilities:
- Initialize the rumps App
- Build the menubar menu from discovered tools
- Handle menu callbacks
- Implement "Clipboard: Auto-detect" logic
- Show "About" and "Quit" options

**Key Method:**
- `_build_menu()` — Constructs menubar dropdown, groups tools by category
- `_make_tool_callback()` — Creates a callback closure for each tool
- `_on_auto_detect()` — Detects clipboard content type and opens matching tool

### Plugin System (plugin_loader.py)

Dynamic tool discovery and registration:

```python
def discover_tools() -> list[DevTool]:
    """Scan tools/ directory and return registered tool instances."""
```

**How it works:**
1. Imports `devdash.tools` package
2. Iterates over all modules in `tools/` directory
3. Skips modules starting with `_` and the `base.py` module
4. Calls the `register()` function in each module
5. Returns sorted list by category then name

**Why dynamic discovery?**
- Adding a new tool requires only creating a new file
- No central registry to update
- Tools can be added, removed, or disabled easily

### tools/base.py — Tool Interface

Abstract base class that all tools inherit from:

```python
class DevTool(ABC):
    """Base class for all DevDash tools."""
```

**Required to implement:**

| Property/Method | Type | Purpose |
|-----------------|------|---------|
| `name` | property | Display name in menu |
| `keyword` | property | Short identifier for CLI/detection |
| `process()` | method | Core processing logic |

**Optional to implement:**

| Property/Method | Type | Purpose |
|-----------------|------|---------|
| `category` | property | Menu grouping (default: "General") |
| `description` | property | Tooltip text (default: "") |
| `validate()` | method | Pre-validation (default: None) |

### clipboard.py — Clipboard Integration

Reading, writing, and detecting clipboard content:

```python
class ContentType(Enum):
    JWT, JSON, UUID, BASE64, UNIX_TIMESTAMP, URL, ...
```

**Key Functions:**

| Function | Purpose |
|----------|---------|
| `read()` | Get clipboard as string |
| `write(text)` | Write to clipboard |
| `detect_type(text)` | Identify content format |

**Detection Algorithm:**

The `detect_type()` function uses priority-based detection:

1. **JWT** — Starts with `eyJ` + exactly 2 dots
2. **JSON** — Starts with `{` or `[` + valid JSON parse
3. **UUID** — Matches 8-4-4-4-12 hex pattern
4. **Cron** — 5-6 space-separated numeric fields
5. **URL-Encoded** — Contains `%XX` patterns + no spaces
6. **Base64** — Matches charset + length is multiple of 4
7. **Unix Timestamp** — 10 or 13 digits in reasonable range (1970-2100)
8. **Hex Color** — Starts with `#` + 3 or 6 hex digits
9. **URL** — Starts with `http://` or `https://`
10. **Plain Text** — Fallback

**Why priority matters:**
- Base64 is generic (could match many things), so check specific formats first
- Timestamps are numeric, but so is other data, so detect context
- URL-encoded requires no spaces to avoid false positives

### config.py — Configuration Management

User preferences stored in YAML:

```python
CONFIG_FILE = Path.home() / ".config" / "devdash" / "config.yaml"
```

**Key Functions:**

| Function | Purpose |
|----------|---------|
| `load_config()` | Load YAML, merge with defaults |
| `save_config(dict)` | Write YAML with restricted permissions (0o600) |

**Default Configuration:**

```python
DEFAULT_CONFIG = {
    "default_hash_algorithm": "sha256",
    "timestamp_format": "%Y-%m-%d %H:%M:%S",
    "password_length": 16,
    "uuid_version": "v4",
    "auto_clipboard_detection": True,
    "clipboard_watcher": False,
}
```

**Thread Safety:**
- Config reads/writes use a threading lock
- Safe for concurrent access

### ui/ — User Interface

#### windows.py — Tool Dialogs

Opens tool dialogs with input/output:

```python
def show_tool_dialog(tool: DevTool, input_text: str = "") -> None:
    """Open a dialog for the given tool."""
```

Currently uses rumps native dialogs. Could be extended with custom windows.

#### notifications.py — Notifications

Show system notifications:

```python
def notify(title: str, message: str) -> None:
    """Show macOS notification."""
```

Used for clipboard auto-detect feedback, errors, etc.

## Data Flow

### Basic Tool Usage

```
User clicks menu
        ↓
Tool callback triggered
        ↓
show_tool_dialog(tool) called
        ↓
User enters input + clicks "Run"
        ↓
tool.process(input) called
        ↓
Result shown in dialog
        ↓
User can copy to clipboard or close
```

### Clipboard Auto-Detect

```
User copies something
        ↓
User clicks "Clipboard: Auto-detect"
        ↓
_on_auto_detect() called
        ↓
clipboard.read() gets content
        ↓
clipboard.detect_type() identifies format
        ↓
Keyword mapped to tool name
        ↓
Tool found in _tools list
        ↓
show_tool_dialog(tool, input_text=content)
        ↓
Tool opens with pre-filled content
```

## Dependency Graph

```
app.py
  ├── rumps                    (macOS UI framework)
  ├── clipboard.py
  ├── plugin_loader.py
  │   └── tools/base.py
  │       └── tools/*.py       (individual tools)
  └── ui/
      ├── windows.py
      └── notifications.py

Tools depend on:
  ├── base.py                  (abstract class)
  ├── config.py                (for preferences)
  └── External libs: PyJWT, croniter, etc.

clipboard.py depends on:
  └── pyperclip                (cross-platform clipboard)

config.py depends on:
  └── pyyaml                   (YAML parsing)
```

## Rumps Explanation

DevDash uses [rumps](https://github.com/jmorey/rumps) — "Ridiculously Uncomplicated macOS Python Statusbar applications."

**Why rumps?**
- Simple API for macOS menubar apps
- No need for Cocoa/Objective-C
- Pure Python with minimal dependencies
- Handles system integration (accessibility, permissions, etc.)

**Core Rumps Concepts:**

```python
class DevDashApp(rumps.App):
    def __init__(self):
        # Create app with title (emoji shows in menubar)
        super().__init__(name="DevDash", title="🔧", quit_button=None)

    # Menu items
    self.menu = [
        rumps.MenuItem("Item 1", callback=self.callback1),
        None,  # Separator
        rumps.MenuItem("Item 2", callback=self.callback2),
    ]

    # Dialogs
    rumps.alert(title, message)
    rumps.password_ask(title, message)
    rumps.save_request(title, message)
```

## Extension Points

### Adding a New Tool

See [docs/adding-tools.md](adding-tools.md). The plugin system makes this easy:

1. Create `src/devdash/tools/mytool.py`
2. Extend `DevTool`
3. Implement required properties/methods
4. Export `register()` function
5. Plugin loader automatically finds it

### Customizing UI

Modify `ui/windows.py` to change tool dialog appearance, or extend `ui/notifications.py` for different notification styles.

### Changing Config Storage

Currently uses YAML in `~/.config/devdash/config.yaml`. To change:
- Edit `config.py` to use different format or location
- Update `DEFAULT_CONFIG` values
- Tools read via `load_config()`, so changes are transparent

### Adding System Tray Menu

Modify `_build_menu()` in `app.py` to add new menu items, separators, or nested menus.

## Type Safety

DevDash uses strict type checking:

- All function parameters have type hints
- All return types are annotated
- `mypy` runs with `strict = true` in pyproject.toml

This catches bugs at development time and makes the code more maintainable.

## Testing Strategy

Tests are organized by module:

```
tests/
├── test_app.py              # Application tests
├── test_clipboard.py        # Clipboard detection tests
├── test_config.py           # Configuration tests
├── test_plugin_loader.py    # Discovery tests
└── test_tools/
    ├── test_json_tool.py
    ├── test_uuid_tool.py
    └── ... (one per tool)
```

Each tool has its own test file with:
- Fixture providing tool instance
- Tests for name, keyword, category
- Tests for process() with valid/invalid input
- Tests for validate() method

Run all tests:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=src/devdash --cov-report=term-missing
```

## Performance Considerations

### Startup Time

- Plugin discovery is fast (only imports module names)
- Tools are lazily instantiated when first clicked
- Config loads once at app start

### Memory

- Each tool kept in memory (12 tools ≈ negligible)
- Clipboard content kept during auto-detect only
- Config cached in memory

### Clipboard Detection

Detection is O(n) where n = clipboard length. Most content is <100KB, detection is <1ms.

## Security Considerations

### Clipboard Handling

- Data only read when user clicks "Auto-detect"
- Not continuously monitored (unless `clipboard_watcher` enabled)
- Not logged or stored anywhere
- Discarded after tool opens

### Config Permissions

- Config file created with mode `0o600` (read/write by owner only)
- Contains no secrets (just preferences)

### Input Processing

- All input is treated as untrusted user data
- Tools validate input before processing
- No code execution or shell commands from user input

## Future Improvements

Potential enhancements:
- Clipboard watcher (optional, currently experimental)
- Custom UI framework (beyond rumps)
- Plugin system with external tools
- Settings GUI instead of YAML editing
- Keyboard shortcuts for each tool
- Search/filter tools in menu
- Tool history/favorites

## See Also

- [docs/adding-tools.md](adding-tools.md) — Creating new tools
- [docs/usage.md](usage.md) — User guide
- [CONTRIBUTING.md](../CONTRIBUTING.md) — Development guidelines
