# GadgetBox

Cross-platform system tray developer utilities at your fingertips.

[![PyPI](https://img.shields.io/pypi/v/gadgetbox.svg)](https://pypi.org/project/gadgetbox)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[GIF PLACEHOLDER - system tray app with tools opening across Windows, macOS, and Linux]

Works on **Windows**, **macOS**, and **Linux**.

## Why GadgetBox?

- **Free & Open Source** — MIT licensed, no ads, no tracking, community-driven
- **Offline First** — All processing happens locally. Nothing is ever sent to external services
- **Pip Installable** — Single command installation. Works with Python 3.10+

## Quick Start

```bash
pip install gadgetbox
gadgetbox
```

Click the wrench icon (🔧) in your system tray to access all tools.

## Tools

GadgetBox includes 12 essential developer utilities:

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

GadgetBox auto-detects your clipboard content and opens the right tool automatically.

**How it works:**
1. Copy anything to your clipboard (JSON, UUID, JWT, URL, etc.)
2. Click "Clipboard: Auto-detect" in the GadgetBox menu
3. The matching tool opens with your content pre-filled

Supports auto-detection for: JSON, JWT, UUID, Base64, URL-encoded text, timestamps, hex colors, and cron expressions.

## Configuration

GadgetBox stores user preferences in `~/.config/gadgetbox/config.yaml` on macOS/Linux, or `%APPDATA%/gadgetbox/config.yaml` on Windows. Edit this file to customize:

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
pip install gadgetbox
gadgetbox
```

### From Source

```bash
git clone https://github.com/vamsi876/gadgetbox.git
cd gadgetbox
pip install -e .
gadgetbox
```

For development setup, see [CONTRIBUTING.md](CONTRIBUTING.md).

## Permissions (macOS)

GadgetBox needs clipboard access to work. On first run, macOS will ask for permission:

> "GadgetBox" would like to access your clipboard.

Click **Allow** to enable clipboard auto-detection. You can revoke this later in System Preferences → Security & Privacy → Accessibility.

## Troubleshooting

**"command not found: gadgetbox"**
- Ensure Python 3.10+ is installed: `python3 --version`
- Reinstall: `pip install --upgrade gadgetbox`

**System tray icon doesn't appear**
- Restart the app: press Ctrl+C to quit, then run `gadgetbox` again

**Clipboard detection not working**
- On macOS, grant clipboard permission: System Preferences → Security & Privacy → Accessibility
- Enable in config: `auto_clipboard_detection: true`

## Contributing

Found a bug? Want a new tool? Head to [CONTRIBUTING.md](CONTRIBUTING.md) to get started.

Quick links:
- [Reporting bugs](CONTRIBUTING.md#reporting-bugs)
- [Suggesting features](CONTRIBUTING.md#suggesting-features)
- [Adding a new tool](docs/adding-tools.md)
- [Architecture overview](docs/architecture.md)

## Built With

- [pystray](https://github.com/moses-palmer/pystray) — System tray application support
- [tkinter](https://docs.python.org/3/library/tkinter.html) — Cross-platform GUI toolkit
- [Pillow](https://python-pillow.org/) — Image processing for tray icons
- [plyer](https://github.com/kivy/plyer) — Platform-independent Python API for accessing hardware features
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

MIT License © 2024-2026 GadgetBox Contributors

See [LICENSE](LICENSE) for details.
