"""Tests for gadgetbox.plugin_loader - dynamic tool discovery."""

from unittest.mock import MagicMock, patch

import pytest

from gadgetbox.plugin_loader import discover_tools
from gadgetbox.tools.base import DevTool


class TestDiscoverTools:
    """Test that discover_tools finds and returns valid DevTool instances."""

    def test_returns_a_list(self) -> None:
        result = discover_tools()
        assert isinstance(result, list)

    def test_all_items_are_devtool_instances(self) -> None:
        tools = discover_tools()
        for tool in tools:
            assert isinstance(tool, DevTool), f"{tool!r} is not a DevTool instance"

    def test_tools_sorted_by_category_then_name(self) -> None:
        tools = discover_tools()
        if len(tools) < 2:
            pytest.skip("Need at least 2 tools to verify sort order")
        sort_keys = [(t.category, t.name) for t in tools]
        assert sort_keys == sorted(sort_keys)

    def test_each_tool_has_required_attributes(self) -> None:
        tools = discover_tools()
        for tool in tools:
            assert isinstance(tool.name, str) and tool.name, f"{tool!r} has empty name"
            assert isinstance(tool.keyword, str) and tool.keyword, f"{tool!r} has empty keyword"
            assert callable(tool.process), f"{tool!r}.process is not callable"

    def test_each_tool_has_category_string(self) -> None:
        tools = discover_tools()
        for tool in tools:
            assert isinstance(tool.category, str)


class TestDiscoverToolsEdgeCases:
    """Test edge cases for the plugin loader."""

    @patch("gadgetbox.plugin_loader.importlib.import_module", side_effect=ImportError("boom"))
    def test_returns_empty_list_when_package_missing(self, mock_import) -> None:
        result = discover_tools()
        assert result == []

    @patch("gadgetbox.plugin_loader.importlib.import_module")
    def test_returns_empty_list_when_no_path(self, mock_import) -> None:
        """If the package has no __path__, we get an empty list."""
        mock_pkg = MagicMock(spec=[])  # no __path__ attribute
        del mock_pkg.__path__
        mock_import.return_value = mock_pkg
        result = discover_tools()
        assert result == []

    @patch("gadgetbox.plugin_loader.pkgutil.iter_modules")
    @patch("gadgetbox.plugin_loader.importlib.import_module")
    def test_skips_modules_starting_with_underscore(self, mock_import, mock_iter) -> None:
        """Modules starting with _ or named 'base' should be skipped."""
        mock_pkg = MagicMock()
        mock_pkg.__path__ = ["/fake/path"]
        mock_import.return_value = mock_pkg
        mock_iter.return_value = [
            (None, "_private", False),
            (None, "base", False),
            (None, "__init__", False),
        ]
        result = discover_tools()
        assert result == []

    @patch("gadgetbox.plugin_loader.pkgutil.iter_modules")
    @patch("gadgetbox.plugin_loader.importlib.import_module")
    def test_handles_module_with_no_register(self, mock_import, mock_iter) -> None:
        """Modules without a register() function should be silently skipped."""
        mock_pkg = MagicMock()
        mock_pkg.__path__ = ["/fake/path"]

        no_register_mod = MagicMock(spec=[])  # no register attribute
        del no_register_mod.register

        def import_side_effect(name: str):
            if name == "gadgetbox.tools":
                return mock_pkg
            return no_register_mod

        mock_import.side_effect = import_side_effect
        mock_iter.return_value = [(None, "some_tool", False)]

        result = discover_tools()
        assert result == []

    @patch("gadgetbox.plugin_loader.pkgutil.iter_modules")
    @patch("gadgetbox.plugin_loader.importlib.import_module")
    def test_handles_register_raising_exception(self, mock_import, mock_iter) -> None:
        """If register() raises, the tool is skipped and others still load."""
        mock_pkg = MagicMock()
        mock_pkg.__path__ = ["/fake/path"]

        bad_mod = MagicMock()
        bad_mod.register.side_effect = RuntimeError("broken tool")

        def import_side_effect(name: str):
            if name == "gadgetbox.tools":
                return mock_pkg
            return bad_mod

        mock_import.side_effect = import_side_effect
        mock_iter.return_value = [(None, "broken_tool", False)]

        result = discover_tools()
        assert result == []
