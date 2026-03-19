"""Tests for gadgetbox.app - cross-platform system tray application.

These tests mock pystray, PIL, and tkinter so they can run in CI
environments that do not have GUI frameworks available.
"""

import sys
import types
from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture(autouse=True)
def mock_gui_libs():
    """Replace pystray, PIL, and tkinter with mocks for headless testing."""
    # Mock pystray
    fake_pystray = types.ModuleType("pystray")
    fake_pystray.Icon = MagicMock()  # type: ignore[attr-defined]
    fake_pystray.MenuItem = MagicMock()  # type: ignore[attr-defined]
    fake_pystray.Menu = MagicMock()  # type: ignore[attr-defined]
    fake_pystray.Menu.SEPARATOR = "---"  # type: ignore[attr-defined]

    # Mock PIL
    fake_pil = types.ModuleType("PIL")
    fake_image = types.ModuleType("PIL.Image")
    fake_image.new = MagicMock(return_value=MagicMock())  # type: ignore[attr-defined]
    fake_draw_mod = types.ModuleType("PIL.ImageDraw")
    fake_draw_mod.Draw = MagicMock(return_value=MagicMock())  # type: ignore[attr-defined]
    fake_pil.Image = fake_image  # type: ignore[attr-defined]
    fake_pil.ImageDraw = fake_draw_mod  # type: ignore[attr-defined]

    originals = {}
    for mod_name, fake in [
        ("pystray", fake_pystray),
        ("PIL", fake_pil),
        ("PIL.Image", fake_image),
        ("PIL.ImageDraw", fake_draw_mod),
    ]:
        originals[mod_name] = sys.modules.get(mod_name)
        sys.modules[mod_name] = fake

    # Clear cached gadgetbox.app so it reimports with mocks
    mods_to_remove = [k for k in sys.modules if k.startswith("gadgetbox.app")]
    saved = {k: sys.modules.pop(k) for k in mods_to_remove}

    yield

    # Restore original modules
    for mod_name, orig in originals.items():
        if orig is not None:
            sys.modules[mod_name] = orig
        else:
            sys.modules.pop(mod_name, None)
    for k, v in saved.items():
        sys.modules[k] = v


class TestMainFunction:
    """Verify that the main() entry point exists and is callable."""

    def test_main_is_callable(self) -> None:
        from gadgetbox.app import main

        assert callable(main)

    @patch("gadgetbox.app.discover_tools", return_value=[])
    def test_main_creates_app_and_runs(self, mock_discover) -> None:
        """main() should instantiate GadgetBoxApp and call run()."""
        from gadgetbox.app import main

        with patch("gadgetbox.app.GadgetBoxApp") as mock_app_cls:
            mock_instance = MagicMock()
            mock_app_cls.return_value = mock_instance
            main()
            mock_app_cls.assert_called_once()
            mock_instance.run.assert_called_once()


class TestGadgetBoxApp:
    """Verify the GadgetBoxApp class has expected structure."""

    def test_class_exists(self) -> None:
        from gadgetbox.app import GadgetBoxApp

        assert GadgetBoxApp is not None

    def test_class_has_build_menu_method(self) -> None:
        from gadgetbox.app import GadgetBoxApp

        assert hasattr(GadgetBoxApp, "_build_menu")

    def test_class_has_on_auto_detect_method(self) -> None:
        from gadgetbox.app import GadgetBoxApp

        assert hasattr(GadgetBoxApp, "_on_auto_detect")

    def test_class_has_on_about_method(self) -> None:
        from gadgetbox.app import GadgetBoxApp

        assert hasattr(GadgetBoxApp, "_on_about")

    def test_class_has_on_quit_method(self) -> None:
        from gadgetbox.app import GadgetBoxApp

        assert hasattr(GadgetBoxApp, "_on_quit")
