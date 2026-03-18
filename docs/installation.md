# Installation Guide

DevDash requires Python 3.10 or newer and runs on macOS only.

## Install from PyPI (Recommended)

The easiest way to get DevDash is via pip:

```bash
pip install devdash-mac
```

Then launch it:

```bash
devdash
```

The app will appear as a wrench icon (🔧) in your macOS menubar.

## Install from Source

If you want to develop DevDash or use the latest unreleased features:

```bash
git clone https://github.com/devdash/devdash.git
cd devdash
pip install -e .
```

The `-e` flag installs in "editable" mode, so changes to the source code take effect immediately.

## System Requirements

- **macOS 10.13+** (Big Sur, Monterey, Ventura, Sonoma, Sequoia)
- **Python 3.10, 3.11, 3.12, or 3.13**
- 50MB disk space

### Check Your Python Version

```bash
python3 --version
```

If you need Python 3.10+, install it via:
- [python.org](https://www.python.org/downloads/)
- [Homebrew](https://brew.sh/): `brew install python@3.12`
- [Anaconda](https://www.anaconda.com/): `conda install python=3.12`

## macOS Permissions

DevDash needs permission to access your clipboard for the auto-detect feature. On first run, macOS will show this dialog:

> "DevDash" would like to access your clipboard.

Click **Allow**. If you deny this, DevDash will still work but clipboard auto-detection won't function.

### Granting Permissions Manually

If you missed the permission prompt, grant access manually:

1. Open System Preferences → Security & Privacy (or System Settings → Privacy & Security)
2. Select **Accessibility** from the left sidebar
3. Click the lock icon to unlock
4. Find and enable "DevDash"

## Upgrading

To update DevDash to the latest version:

```bash
pip install --upgrade devdash
```

## Uninstalling

```bash
pip uninstall devdash
```

## Troubleshooting

### "command not found: devdash"

The `devdash` command isn't in your PATH. Try:

```bash
python3 -m devdash
```

Or reinstall with:

```bash
pip install --force-reinstall devdash
```

### "No module named devdash"

Python can't find the package. Verify installation:

```bash
pip list | grep devdash
```

If not listed, reinstall:

```bash
pip install devdash-mac
```

### App doesn't appear in menubar

1. The app might be loading. Wait a few seconds.
2. If still not visible, check Console.app for errors:
   - Open Console.app
   - Search for "devdash" or "DevDash"
3. Try restarting the app:
   - Press Ctrl+C in the terminal to quit
   - Run `devdash` again

### Permission denied error

If you get a permission error when running `devdash`:

```bash
pip install --user --upgrade devdash
```

The `--user` flag installs to your home directory instead of system-wide.

### ImportError or missing dependencies

Some dependencies might fail to install. Try:

```bash
pip install --upgrade --force-reinstall devdash
```

If errors persist, file a [GitHub issue](https://github.com/devdash/devdash/issues).

## Development Installation

To set up a development environment with testing and linting tools:

```bash
git clone https://github.com/devdash/devdash.git
cd devdash
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
mypy src/devdash/         # Type check
```

See [CONTRIBUTING.md](../CONTRIBUTING.md) for more details.
