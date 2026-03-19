"""User preferences management with YAML config."""

import logging
import os
import platform
import threading
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger(__name__)

# Cross-platform config directory candidates
_PRIMARY_DIR = Path.home() / ".config" / "gadgetbox"

if platform.system() == "Windows":
    _FALLBACK_DIR = Path(os.environ.get("APPDATA", str(Path.home()))) / "gadgetbox"
elif platform.system() == "Darwin":
    _FALLBACK_DIR = Path.home() / "Library" / "Application Support" / "gadgetbox"
else:
    # Linux/other: XDG already covered by _PRIMARY_DIR
    _FALLBACK_DIR = Path.home() / ".local" / "share" / "gadgetbox"

_lock = threading.Lock()

DEFAULT_CONFIG: dict[str, Any] = {
    "default_hash_algorithm": "sha256",
    "timestamp_format": "%Y-%m-%d %H:%M:%S",
    "password_length": 16,
    "uuid_version": "v4",
    "auto_clipboard_detection": True,
    "clipboard_watcher": False,
}


def _resolve_config_dir() -> Path:
    """Find a writable config directory."""
    for candidate in (_PRIMARY_DIR, _FALLBACK_DIR):
        try:
            candidate.mkdir(parents=True, exist_ok=True)
            return candidate
        except PermissionError:
            continue
    # Last resort: use home directory directly
    return Path.home() / ".gadgetbox"


CONFIG_DIR = _resolve_config_dir()
CONFIG_FILE = CONFIG_DIR / "config.yaml"


def load_config() -> dict[str, Any]:
    """Load config from file, creating defaults on first run."""
    with _lock:
        if not CONFIG_FILE.exists():
            try:
                save_config(DEFAULT_CONFIG)
            except PermissionError:
                logger.warning("Cannot create config file at %s", CONFIG_FILE)
            return dict(DEFAULT_CONFIG)
        try:
            with open(CONFIG_FILE) as f:
                data = yaml.safe_load(f)
        except (PermissionError, OSError):
            return dict(DEFAULT_CONFIG)
        if not isinstance(data, dict):
            return dict(DEFAULT_CONFIG)
        merged = dict(DEFAULT_CONFIG)
        merged.update(data)
        return merged


def save_config(config: dict[str, Any]) -> None:
    """Save config to file with restricted permissions."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        yaml.dump(config, f, default_flow_style=False)
    if platform.system() != "Windows":
        os.chmod(CONFIG_FILE, 0o600)
