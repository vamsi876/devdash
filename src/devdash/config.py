"""User preferences management with YAML config."""

import os
import threading
from pathlib import Path
from typing import Any

import yaml

CONFIG_DIR = Path.home() / ".config" / "devdash"
CONFIG_FILE = CONFIG_DIR / "config.yaml"

_lock = threading.Lock()

DEFAULT_CONFIG: dict[str, Any] = {
    "default_hash_algorithm": "sha256",
    "timestamp_format": "%Y-%m-%d %H:%M:%S",
    "password_length": 16,
    "uuid_version": "v4",
    "auto_clipboard_detection": True,
    "clipboard_watcher": False,
}


def _ensure_config_dir() -> None:
    """Create config directory if it doesn't exist."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def load_config() -> dict[str, Any]:
    """Load config from file, creating defaults on first run."""
    with _lock:
        if not CONFIG_FILE.exists():
            save_config(DEFAULT_CONFIG)
            return dict(DEFAULT_CONFIG)
        with open(CONFIG_FILE) as f:
            data = yaml.safe_load(f)
        if not isinstance(data, dict):
            return dict(DEFAULT_CONFIG)
        # Merge with defaults for any missing keys
        merged = dict(DEFAULT_CONFIG)
        merged.update(data)
        return merged


def save_config(config: dict[str, Any]) -> None:
    """Save config to file with restricted permissions."""
    _ensure_config_dir()
    with open(CONFIG_FILE, "w") as f:
        yaml.dump(config, f, default_flow_style=False)
    os.chmod(CONFIG_FILE, 0o600)
