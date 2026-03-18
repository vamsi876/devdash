"""Main DevDash application - macOS menubar app."""

from __future__ import annotations

import rumps

from devdash import __app_name__, __version__, clipboard
from devdash.config import load_config
from devdash.plugin_loader import discover_tools
from devdash.tools.base import DevTool
from devdash.ui.notifications import notify
from devdash.ui.windows import show_tool_dialog

# Content type display names for notifications
_TYPE_NAMES: dict[clipboard.ContentType, str] = {
    clipboard.ContentType.JSON: "JSON",
    clipboard.ContentType.JWT: "JWT token",
    clipboard.ContentType.UUID: "UUID",
    clipboard.ContentType.BASE64: "Base64",
    clipboard.ContentType.UNIX_TIMESTAMP: "Unix timestamp",
    clipboard.ContentType.URL: "URL",
    clipboard.ContentType.URL_ENCODED: "URL-encoded text",
    clipboard.ContentType.HEX_COLOR: "HEX color",
    clipboard.ContentType.CRON: "Cron expression",
}


class DevDashApp(rumps.App):
    """macOS menubar developer utilities app."""

    def __init__(self) -> None:
        super().__init__(name=__app_name__, title="\U0001f527", quit_button=None)
        self._tools: list[DevTool] = discover_tools()
        self._last_clipboard: str = ""
        self._build_menu()
        # Start clipboard watcher if enabled in config
        config = load_config()
        if config.get("clipboard_watcher", False):
            self._start_clipboard_watcher()

    def _build_menu(self) -> None:
        """Build the menubar dropdown from discovered tools."""
        menu_items: list[rumps.MenuItem | None] = []

        # Auto-detect clipboard item
        auto_detect = rumps.MenuItem("Clipboard: Auto-detect", callback=self._on_auto_detect)
        menu_items.append(auto_detect)
        menu_items.append(None)  # separator

        # Group tools by category
        current_category = ""
        for tool in self._tools:
            if tool.category != current_category:
                if current_category:
                    menu_items.append(None)  # separator between categories
                current_category = tool.category
            item = rumps.MenuItem(tool.name, callback=self._make_tool_callback(tool))
            menu_items.append(item)

        menu_items.append(None)  # separator

        # About and Quit
        about = rumps.MenuItem(f"About {__app_name__}", callback=self._on_about)
        quit_item = rumps.MenuItem("Quit", callback=self._on_quit)
        menu_items.append(about)
        menu_items.append(quit_item)

        self.menu = menu_items

    def _make_tool_callback(self, tool: DevTool):  # type: ignore[no-untyped-def]
        """Create a callback closure for a specific tool."""

        def callback(_: rumps.MenuItem) -> None:
            show_tool_dialog(tool)

        return callback

    def _on_auto_detect(self, _: rumps.MenuItem) -> None:
        """Read clipboard, detect content type, open matching tool."""
        content = clipboard.read()
        if not content.strip():
            notify("DevDash", "Clipboard is empty")
            return

        detected = clipboard.detect_type(content)
        # Find matching tool by keyword
        keyword_map = {
            clipboard.ContentType.JSON: "json",
            clipboard.ContentType.JWT: "jwt",
            clipboard.ContentType.UUID: "uuid",
            clipboard.ContentType.BASE64: "base64",
            clipboard.ContentType.UNIX_TIMESTAMP: "timestamp",
            clipboard.ContentType.URL: "url",
            clipboard.ContentType.URL_ENCODED: "url",
            clipboard.ContentType.HEX_COLOR: "color",
            clipboard.ContentType.CRON: "cron",
        }
        keyword = keyword_map.get(detected)
        if keyword:
            for tool in self._tools:
                if tool.keyword == keyword:
                    show_tool_dialog(tool, input_text=content)
                    return
        notify("DevDash", f"Detected: {detected.name}. No matching tool found.")

    def _on_about(self, _: rumps.MenuItem) -> None:
        """Show about dialog."""
        rumps.alert(
            title=f"About {__app_name__}",
            message=f"{__app_name__} v{__version__}\n\n"
            "Open-source macOS menubar developer utilities.\n"
            "https://github.com/devdash/devdash",
        )

    def _on_quit(self, _: rumps.MenuItem) -> None:
        """Quit the app."""
        rumps.quit_application()

    def _start_clipboard_watcher(self) -> None:
        """Start background clipboard polling (opt-in, privacy conscious)."""

        @rumps.timer(2)
        def _watch_clipboard(timer: rumps.Timer) -> None:
            try:
                content = clipboard.read()
                if not content or content == self._last_clipboard:
                    return
                self._last_clipboard = content
                detected = clipboard.detect_type(content)
                if detected != clipboard.ContentType.PLAIN_TEXT:
                    type_name = _TYPE_NAMES.get(detected, detected.name)
                    notify(
                        "DevDash",
                        f"Detected {type_name} in your clipboard. Click to process.",
                    )
            except Exception:
                pass  # Never crash the watcher

        _watch_clipboard.start()  # type: ignore[attr-defined]


def main() -> None:
    """Entry point for the application."""
    app = DevDashApp()
    app.run()
