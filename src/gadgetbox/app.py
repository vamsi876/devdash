"""Main GadgetBox application — cross-platform system tray app."""

from __future__ import annotations

import sys
import threading
import tkinter as tk
from tkinter import messagebox
from typing import Any

import pystray
from PIL import Image, ImageDraw

from gadgetbox import __app_name__, __version__, clipboard
from gadgetbox.config import load_config
from gadgetbox.plugin_loader import discover_tools
from gadgetbox.tools.base import DevTool
from gadgetbox.ui.notifications import notify
from gadgetbox.ui.windows import show_tool_dialog

_IS_MACOS = sys.platform == "darwin"

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


def _create_icon_image() -> Image.Image:
    """Create a simple tray icon using Pillow."""
    size = 64
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse([4, 4, size - 4, size - 4], fill=(70, 130, 180))
    draw.text((size // 2 - 8, size // 2 - 10), "G", fill="white")
    return img


def _run_tk_dialog(func: Any) -> None:
    """Run a tkinter dialog in a temporary root window (macOS) or scheduled on existing root."""
    root = tk.Tk()
    root.withdraw()
    try:
        func(root)
    finally:
        root.destroy()


class GadgetBoxApp:
    """Cross-platform system tray developer utilities app."""

    def __init__(self) -> None:
        self._tools: list[DevTool] = discover_tools()
        self._tool_map: dict[str, DevTool] = {}
        self._last_clipboard: str = ""
        self._icon: pystray.Icon | None = None
        self._root: tk.Tk | None = None
        self._clipboard_timer: threading.Timer | None = None

        config = load_config()
        self._clipboard_watcher_enabled = config.get("clipboard_watcher", False)

    def _build_menu(self) -> pystray.Menu:
        """Build the system tray menu from discovered tools."""
        items: list[Any] = []

        items.append(pystray.MenuItem("Clipboard: Auto-detect", self._on_auto_detect))
        items.append(pystray.Menu.SEPARATOR)

        current_category = ""
        for tool in self._tools:
            if tool.category != current_category:
                if current_category:
                    items.append(pystray.Menu.SEPARATOR)
                current_category = tool.category
            self._tool_map[tool.name] = tool
            items.append(pystray.MenuItem(tool.name, self._make_tool_callback(tool.name)))

        items.append(pystray.Menu.SEPARATOR)
        items.append(pystray.MenuItem(f"About {__app_name__}", self._on_about))
        items.append(pystray.MenuItem("Quit", self._on_quit))

        return pystray.Menu(*items)

    def _show_dialog(self, func: Any) -> None:
        """Show a tkinter dialog, handling macOS vs other platforms."""
        if _IS_MACOS:
            # macOS: pystray owns the main thread; create temporary tk root
            _run_tk_dialog(func)
        else:
            # Windows/Linux: schedule on the persistent tk main thread
            if self._root:
                self._root.after(0, lambda: func(self._root))

    def _make_tool_callback(self, tool_name: str) -> Any:
        """Create a callback for a specific tool menu item."""
        def callback(icon: Any, item: Any) -> None:
            tool = self._tool_map.get(tool_name)
            if tool:
                self._show_dialog(lambda root: show_tool_dialog(tool))
        return callback

    def _on_auto_detect(self, icon: Any, item: Any) -> None:
        """Read clipboard, detect content type, open matching tool."""
        self._show_dialog(lambda root: self._auto_detect_impl())

    def _auto_detect_impl(self) -> None:
        """Auto-detect implementation."""
        content = clipboard.read()
        if not content.strip():
            messagebox.showinfo("GadgetBox", "Clipboard is empty")
            return

        detected = clipboard.detect_type(content)
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
        messagebox.showinfo(
            "GadgetBox", f"Detected: {detected.name}. No matching tool found."
        )

    def _on_about(self, icon: Any, item: Any) -> None:
        """Show about dialog."""
        self._show_dialog(
            lambda root: messagebox.showinfo(
                f"About {__app_name__}",
                (
                    f"{__app_name__} v{__version__}\n\n"
                    "Cross-platform system tray developer utilities.\n"
                    "https://github.com/vamsi876/gadgetbox"
                ),
            )
        )

    def _on_quit(self, icon: Any, item: Any) -> None:
        """Quit the app."""
        self._stop_clipboard_watcher()
        if self._icon:
            self._icon.stop()
        if self._root:
            self._root.after(0, self._root.quit)

    def _start_clipboard_watcher(self) -> None:
        """Start background clipboard polling (opt-in, privacy conscious)."""
        def poll() -> None:
            try:
                content = clipboard.read()
                if content and content != self._last_clipboard:
                    self._last_clipboard = content
                    detected = clipboard.detect_type(content)
                    if detected != clipboard.ContentType.PLAIN_TEXT:
                        type_name = _TYPE_NAMES.get(detected, detected.name)
                        notify(
                            "GadgetBox",
                            f"Detected {type_name} in your clipboard. Click to process.",
                        )
            except Exception:
                pass
            self._clipboard_timer = threading.Timer(2.0, poll)
            self._clipboard_timer.daemon = True
            self._clipboard_timer.start()

        self._clipboard_timer = threading.Timer(2.0, poll)
        self._clipboard_timer.daemon = True
        self._clipboard_timer.start()

    def _stop_clipboard_watcher(self) -> None:
        """Stop the clipboard polling timer."""
        if self._clipboard_timer:
            self._clipboard_timer.cancel()
            self._clipboard_timer = None

    def run(self) -> None:
        """Start the application."""
        menu = self._build_menu()
        self._icon = pystray.Icon(
            name="gadgetbox",
            icon=_create_icon_image(),
            title=__app_name__,
            menu=menu,
        )

        if self._clipboard_watcher_enabled:
            self._start_clipboard_watcher()

        if _IS_MACOS:
            # macOS: pystray (AppKit) must own the main thread.
            # tkinter dialogs are created on-demand in callbacks.
            self._icon.run()
        else:
            # Windows/Linux: tkinter mainloop on main thread,
            # pystray in a daemon thread.
            self._root = tk.Tk()
            self._root.withdraw()
            tray_thread = threading.Thread(target=self._icon.run, daemon=True)
            tray_thread.start()
            self._root.mainloop()


def main() -> None:
    """Entry point for the application."""
    app = GadgetBoxApp()
    app.run()
