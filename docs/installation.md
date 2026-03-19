# Installation Guide

GadgetBox requires Python 3.10 or newer and works on Windows, macOS, and Linux.

## Install from PyPI (Recommended)

The easiest way to get GadgetBox is via pip:

```bash
pip install gadgetbox
```

Then launch it:

```bash
gadgetbox
```

The app will appear as a wrench icon (🔧) in your system tray.

## Install from Source

If you want to develop GadgetBox or use the latest unreleased features:

```bash
git clone https://github.com/vamsi876/gadgetbox.git
cd gadgetbox
pip install -e .
```

The `-e` flag installs in "editable" mode, so changes to the source code take effect immediately.

## System Requirements

- **Python 3.10, 3.11, 3.12, or 3.13**
- **Windows 10+**, **macOS 10.13+** (Big Sur, Monterey, Ventura, Sonoma, Sequoia), or **Linux** (Ubuntu 18.04+, Debian 10+, etc.)
- 50MB disk space

### Check Your Python Version

```bash
python3 --version
```

If you need Python 3.10+, install it via:
- [python.org](https://www.python.org/downloads/)
- [Homebrew](https://brew.sh/): `brew install python@3.12`
- [Anaconda](https://www.anaconda.com/): `conda install python=3.12`

## Permissions (macOS Only)

GadgetBox needs permission to access your clipboard for the auto-detect feature. On first run, macOS will show this dialog:

> "GadgetBox" would like to access your clipboard.

Click **Allow**. If you deny this, GadgetBox will still work but clipboard auto-detection won't function.

### Granting Permissions Manually

If you missed the permission prompt, grant access manually:

1. Open System Preferences → Security & Privacy (or System Settings → Privacy & Security)
2. Select **Accessibility** from the left sidebar
3. Click the lock icon to unlock
4. Find and enable "GadgetBox"

## Upgrading

To update GadgetBox to the latest version:

```bash
pip install --upgrade gadgetbox
```

## Uninstalling

```bash
pip uninstall gadgetbox
```

## Troubleshooting

### "command not found: gadgetbox"

The `gadgetbox` command isn't in your PATH. Try:

```bash
python3 -m gadgetbox
```

Or reinstall with:

```bash
pip install --force-reinstall gadgetbox
```

### "No module named gadgetbox"

Python can't find the package. Verify installation:

```bash
pip list | grep gadgetbox
```

If not listed, reinstall:

```bash
pip install gadgetbox
```

### App doesn't appear in system tray

1. The app might be loading. Wait a few seconds.
2. If still not visible, check your system logs for errors.
3. Try restarting the app:
   - Press Ctrl+C in the terminal to quit
   - Run `gadgetbox` again

### Permission denied error

If you get a permission error when running `gadgetbox`:

```bash
pip install --user --upgrade gadgetbox
```

The `--user` flag installs to your home directory instead of system-wide.

### ImportError or missing dependencies

Some dependencies might fail to install. Try:

```bash
pip install --upgrade --force-reinstall gadgetbox
```

If errors persist, file a [GitHub issue](https://github.com/vamsi876/gadgetbox/issues).

## Development Installation

To set up a development environment with testing and linting tools:

```bash
git clone https://github.com/vamsi876/gadgetbox.git
cd gadgetbox
pip install -e ".[dev]"
```

This installs:
- pytest — test runner
- pytest-cov — coverage reports
- ruff — fast Python linter
- mypy — static type checker
- pre-commit — git hooks

To verify the installation:

```bash
pytest                    # Run tests
ruff check src/           # Lint code
mypy src/gadgetbox/       # Type check
```

See [CONTRIBUTING.md](../CONTRIBUTING.md) for more details.
