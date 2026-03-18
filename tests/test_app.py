"""Tests for devdash.app - macOS menubar application.

These tests mock the rumps module entirely so they can run in CI
environments that do not have macOS GUI frameworks available.
"""

import sys
import types
from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture(autouse=True)
def mock_rumps():
    """Replace the rumps module with a mock so tests work without macOS GUI.

    This fixture injects a fake rumps module into sys.modules before
    devdash.app is imported, then cleans up afterwards.
    """
    fake_rumps = types.ModuleType("rumps")
    fake_rumps.App = MagicMock  # type: ignore[attr-defined]
    fake_rumps.MenuItem = MagicMock  # type: ignore[attr-defined]
    fake_rumps.alert = MagicMock()  # type: ignore[attr-defined]
    fake_rumps.quit_application = MagicMock()  # type: ignore[attr-defined]

    original = sys.modules.get("rumps")
    sys.modules["rumps"] = fake_rumps

    # Also ensure devdash.app is reloaded with the mock
    mods_to_remove = [k for k in sys.modules if k.startswith("devdash.app")]
    saved = {k: sys.modules.pop(k) for k in mods_to_remove}

    yield fake_rumps

    # Restore original modules
    if original is not None:
        sys.modules["rumps"] = original
    else:
        sys.modules.pop("rumps", None)
    for k, v in saved.items():
        sys.modules[k] = v


class TestMainFunction:
    """Verify that the main() entry point exists and is callable."""

    def test_main_is_callable(self, mock_rumps) -> None:
        from devdash.app import main

        assert callable(main)

    @patch("devdash.app.discover_tools", return_value=[])
    def test_main_creates_app_and_runs(self, mock_discover, mock_rumps) -> None:
        """main() should instantiate DevDashApp and call run()."""
        from devdash.app import main

        with patch("devdash.app.DevDashApp") as MockApp:
            mock_instance = MagicMock()
            MockApp.return_value = mock_instance
            main()
            MockApp.assert_called_once()
            mock_instance.run.assert_called_once()


class TestDevDashApp:
    """Verify the DevDashApp class can be referenced and has expected structure."""

    def test_class_exists(self, mock_rumps) -> None:
        from devdash.app import DevDashApp

        assert DevDashApp is not None

    def test_class_has_build_menu_method(self, mock_rumps) -> None:
        from devdash.app import DevDashApp

        assert hasattr(DevDashApp, "_build_menu")

    def test_class_has_on_auto_detect_method(self, mock_rumps) -> None:
        from devdash.app import DevDashApp

        assert hasattr(DevDashApp, "_on_auto_detect")

    def test_class_has_on_about_method(self, mock_rumps) -> None:
        from devdash.app import DevDashApp

        assert hasattr(DevDashApp, "_on_about")

    def test_class_has_on_quit_method(self, mock_rumps) -> None:
        from devdash.app import DevDashApp

        assert hasattr(DevDashApp, "_on_quit")
