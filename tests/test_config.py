"""Tests for gadgetbox.config - user preferences management."""

from pathlib import Path
from unittest.mock import patch

import pytest
import yaml

import gadgetbox.config as config_mod
from gadgetbox.config import DEFAULT_CONFIG, load_config, save_config


@pytest.fixture()
def config_in_tmp(tmp_path: Path):
    """Patch CONFIG_DIR and CONFIG_FILE to point at a temporary directory."""
    cfg_dir = tmp_path / ".config" / "gadgetbox"
    cfg_file = cfg_dir / "config.yaml"
    with (
        patch.object(config_mod, "CONFIG_DIR", cfg_dir),
        patch.object(config_mod, "CONFIG_FILE", cfg_file),
    ):
        yield cfg_dir, cfg_file


# ---------------------------------------------------------------------------
# load_config
# ---------------------------------------------------------------------------


class TestLoadConfig:
    """Test loading configuration from disk."""

    def test_returns_dict_with_default_keys(self, config_in_tmp) -> None:
        cfg = load_config()
        assert isinstance(cfg, dict)
        for key in DEFAULT_CONFIG:
            assert key in cfg, f"Missing default key: {key}"

    def test_default_values_match(self, config_in_tmp) -> None:
        cfg = load_config()
        for key, value in DEFAULT_CONFIG.items():
            assert cfg[key] == value

    def test_missing_file_creates_defaults(self, config_in_tmp) -> None:
        _cfg_dir, cfg_file = config_in_tmp
        assert not cfg_file.exists()
        load_config()
        assert cfg_file.exists()

    def test_missing_file_content_matches_defaults(self, config_in_tmp) -> None:
        _cfg_dir, cfg_file = config_in_tmp
        load_config()
        with open(cfg_file) as f:
            on_disk = yaml.safe_load(f)
        for key, value in DEFAULT_CONFIG.items():
            assert on_disk[key] == value

    def test_merges_missing_keys_with_defaults(self, config_in_tmp) -> None:
        """If the file has only some keys, the rest come from defaults."""
        cfg_dir, cfg_file = config_in_tmp
        cfg_dir.mkdir(parents=True, exist_ok=True)
        with open(cfg_file, "w") as f:
            yaml.dump({"password_length": 32}, f)
        cfg = load_config()
        assert cfg["password_length"] == 32
        assert cfg["default_hash_algorithm"] == DEFAULT_CONFIG["default_hash_algorithm"]

    def test_invalid_yaml_returns_defaults(self, config_in_tmp) -> None:
        """If the file contains non-dict YAML, defaults are returned."""
        cfg_dir, cfg_file = config_in_tmp
        cfg_dir.mkdir(parents=True, exist_ok=True)
        cfg_file.write_text("just a string\n")
        cfg = load_config()
        assert cfg == DEFAULT_CONFIG


# ---------------------------------------------------------------------------
# save_config
# ---------------------------------------------------------------------------


class TestSaveConfig:
    """Test persisting configuration to disk."""

    def test_creates_config_directory(self, config_in_tmp) -> None:
        cfg_dir, _cfg_file = config_in_tmp
        assert not cfg_dir.exists()
        save_config(DEFAULT_CONFIG)
        assert cfg_dir.exists()

    def test_creates_config_file(self, config_in_tmp) -> None:
        _cfg_dir, cfg_file = config_in_tmp
        save_config(DEFAULT_CONFIG)
        assert cfg_file.exists()

    def test_file_permissions_are_600(self, config_in_tmp) -> None:
        _cfg_dir, cfg_file = config_in_tmp
        save_config(DEFAULT_CONFIG)
        mode = cfg_file.stat().st_mode & 0o777
        assert mode == 0o600

    def test_saved_content_is_valid_yaml(self, config_in_tmp) -> None:
        _cfg_dir, cfg_file = config_in_tmp
        save_config({"custom_key": "custom_value"})
        with open(cfg_file) as f:
            data = yaml.safe_load(f)
        assert data == {"custom_key": "custom_value"}


# ---------------------------------------------------------------------------
# Roundtrip
# ---------------------------------------------------------------------------


class TestConfigRoundtrip:
    """Test save then load produces the same data."""

    def test_save_then_load_roundtrip(self, config_in_tmp) -> None:
        custom = dict(DEFAULT_CONFIG)
        custom["password_length"] = 24
        custom["clipboard_watcher"] = True
        save_config(custom)
        loaded = load_config()
        for key, value in custom.items():
            assert loaded[key] == value

    def test_overwrite_preserves_new_values(self, config_in_tmp) -> None:
        save_config(DEFAULT_CONFIG)
        updated = dict(DEFAULT_CONFIG)
        updated["timestamp_format"] = "%d/%m/%Y"
        save_config(updated)
        loaded = load_config()
        assert loaded["timestamp_format"] == "%d/%m/%Y"
