# DevDash

Open-source macOS menubar developer utilities at your fingertips.

[![PyPI](https://img.shields.io/pypi/v/devdash.svg)](https://pypi.org/project/devdash)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[GIF PLACEHOLDER - menubar app with tools opening in macOS]

## Why DevDash?

- **Free & Open Source** — MIT licensed, no ads, no tracking, community-driven
- **Offline First** — All processing happens locally. Nothing is ever sent to external services
- **Pip Installable** — Single command installation. Works with Python 3.10+

## Quick Start

```bash
pip install devdash
devdash
```

Click the wrench icon (🔧) in your macOS menubar to access all tools.

## Tools

DevDash includes 12 essential developer utilities:

| Tool | What it does |
|------|-------------|
| 📝 **JSON Formatter** | Format, validate, and minify JSON |
| 🔐 **JWT Decoder** | Decode and inspect JSON Web Tokens |
| 🆔 **UUID / ULID Generator** | Generate UUID v4, v7, or ULID identifiers |
| 📄 **Base64 Encode/Decode** | Encode text to Base64 or decode back |
| #️⃣ **Hash Generator** | Generate MD5, SHA256, SHA512 hashes |
| ⏰ **Timestamp Converter** | Convert between Unix timestamps and readable dates |
| 🔗 **URL Encode/Decode** | Encode and decode URL-safe strings |
| 🔍 **Regex Tester** | Test regular expressions with live matches |
| 🎨 **Color Converter** | Convert between hex, RGB, and HSL colors |
| 📚 **Lorem Ipsum Generator** | Generate placeholder text and paragraphs |
| 🔑 **Password Generator** | Create secure random passwords |
| ⏱️ **Cron Parser** | Parse and explain cron expressions |

## Smart Clipboard

DevDash auto-detects your clipboard content and opens the right tool automatically.

**How it works:**
1. Copy anything to your clipboard (JSON, UUID, JWT, URL, etc.)
2. Click "Clipboard: Auto-detect" in the DevDash menu
3. The matching tool opens with your content pre-filled

Supports auto-detection for: JSON, JWT, UUID, Base64, URL-encoded text, timestamps, hex colors, and cron expressions.

## Configuration

DevDash stores user preferences in `~/.config/devdash/config.yaml`. Edit this file to customize:

```yaml
# Default hash algorithm: md5, sha256, sha512
default_hash_algorithm: sha256

# Timestamp format (Python strftime)
timestamp_format: "%Y-%m-%d %H:%M:%S"

# Password generator length
password_length: 16

# UUID version: v4, v7
uuid_version: v4

# Enable clipboard auto-detection
auto_clipboard_detection: true

# Watch clipboard for changes (experimental)
clipboard_watcher: false
```

The config file is created automatically on first run with sensible defaults.

## Installation

### From PyPI (Recommended)

```bash
pip install devdash
devdash
```

### From Source

```bash
git clone https://github.com/devdash/devdash.git
cd devdash
pip install -e .
devdash
```

For development setup, see [CONTRIBUTING.md](CONTRIBUTING.md).

## macOS Permissions

DevDash needs clipboard access to work. On first run, macOS will ask for permission:

> "DevDash" would like to access your clipboard.

Click **Allow** to enable clipboard auto-detection. You can revoke this later in System Preferences → Security & Privacy → Accessibility.

## Troubleshooting

**"command not found: devdash"**
- Ensure Python 3.10+ is installed: `python3 --version`
- Reinstall: `pip install --upgrade devdash`

**Menubar icon doesn't appear**
- Restart the app: press Ctrl+C to quit, then run `devdash` again
- Check that you have a menubar (not in fullscreen)

**Clipboard detection not working**
- Grant clipboard permission: System Preferences → Security & Privacy → Accessibility
- Enable in config: `auto_clipboard_detection: true`

## Contributing

Found a bug? Want a new tool? Head to [CONTRIBUTING.md](CONTRIBUTING.md) to get started.

Quick links:
- [Reporting bugs](CONTRIBUTING.md#reporting-bugs)
- [Suggesting features](CONTRIBUTING.md#suggesting-features)
- [Adding a new tool](docs/adding-tools.md)
- [Architecture overview](docs/architecture.md)

## Built With

- [rumps](https://github.com/jmorey/rumps) — Ridiculously Uncomplicated macOS Python Statusbar applications
- [pyperclip](https://github.com/asweigart/pyperclip) — Cross-platform clipboard support
- [PyJWT](https://pyjwt.readthedocs.io/) — JWT encoding and decoding
- [pyyaml](https://pyyaml.org/) — YAML configuration parsing
- [croniter](https://github.com/taichino/croniter) — Cron expression parsing

## Security

All data processing happens locally on your machine:
- Input is never sent to external services
- Clipboard content is not logged or stored
- No telemetry or analytics

See [LICENSE](LICENSE) for full details.

## License

MIT License © 2024 DevDash Contributors

See [LICENSE](LICENSE) for details.
