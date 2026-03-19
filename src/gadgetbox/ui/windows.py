"""Cross-platform dialog wrappers.

macOS: native dialogs via osascript (AppKit owns the main thread).
Windows/Linux: tkinter dialogs.
"""

from __future__ import annotations

import logging
import re
import subprocess
import sys
from typing import TYPE_CHECKING

from gadgetbox import clipboard
from gadgetbox.ui.notifications import notify_copied

if TYPE_CHECKING:
    from gadgetbox.tools.base import DevTool

logger = logging.getLogger(__name__)

_IS_MACOS = sys.platform == "darwin"

# Metadata patterns to strip when copying output
_METADATA_RE = re.compile(
    r"\s*\(entropy:.*?\)"  # password entropy
    r"|\n\nOriginal bytes:.*"  # base64 byte counts
    r"|\n\nEncoded bytes:.*"
    r"|\n\n\[Auto-detected.*?\]"  # base64 auto-detect label
    r"|\n\nWarning:.*",  # JWT warning
    re.DOTALL,
)


# ---------------------------------------------------------------------------
# macOS dialogs via osascript
# ---------------------------------------------------------------------------


def _osa_input_dialog(title: str, message: str, default: str = "") -> str | None:
    """Show a native macOS input dialog. Returns text or None if cancelled."""
    # Escape double-quotes and backslashes for AppleScript
    esc_title = title.replace("\\", "\\\\").replace('"', '\\"')
    esc_msg = message.replace("\\", "\\\\").replace('"', '\\"')
    esc_default = default.replace("\\", "\\\\").replace('"', '\\"')
    script = (
        f'display dialog "{esc_msg}" '
        f'with title "{esc_title}" '
        f'default answer "{esc_default}" '
        f'buttons {{"Cancel", "OK"}} default button "OK"'
    )
    try:
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True, text=True, timeout=300,
        )
        if result.returncode != 0:
            return None  # User clicked Cancel
        # Output format: "button returned:OK, text returned:user input"
        output = result.stdout.strip()
        prefix = "text returned:"
        idx = output.find(prefix)
        if idx >= 0:
            return output[idx + len(prefix):]
        return output
    except Exception:
        logger.debug("osascript input dialog failed", exc_info=True)
        return None


def _osa_output_dialog(title: str, result: str) -> bool:
    """Show output with Copy button. Returns True if user clicked Copy."""
    esc_title = title.replace("\\", "\\\\").replace('"', '\\"')
    # Truncate very long output for the dialog
    display_text = result[:2000] + ("..." if len(result) > 2000 else "")
    esc_result = display_text.replace("\\", "\\\\").replace('"', '\\"')
    script = (
        f'display dialog "{esc_result}" '
        f'with title "{esc_title}" '
        f'buttons {{"Close", "Copy to Clipboard"}} default button "Copy to Clipboard"'
    )
    try:
        proc = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True, text=True, timeout=300,
        )
        return "Copy to Clipboard" in proc.stdout
    except Exception:
        logger.debug("osascript output dialog failed", exc_info=True)
        return False


def _osa_error_dialog(title: str, message: str) -> None:
    """Show a native macOS error alert."""
    esc_title = title.replace("\\", "\\\\").replace('"', '\\"')
    esc_msg = message.replace("\\", "\\\\").replace('"', '\\"')
    script = (
        f'display alert "{esc_title}" message "{esc_msg}" '
        f'as critical buttons {{"OK"}} default button "OK"'
    )
    try:
        subprocess.run(
            ["osascript", "-e", script],
            capture_output=True, text=True, timeout=30,
        )
    except Exception:
        logger.debug("osascript error dialog failed", exc_info=True)


def _osa_info_dialog(title: str, message: str) -> None:
    """Show a native macOS info alert."""
    esc_title = title.replace("\\", "\\\\").replace('"', '\\"')
    esc_msg = message.replace("\\", "\\\\").replace('"', '\\"')
    script = (
        f'display alert "{esc_title}" message "{esc_msg}" '
        f'buttons {{"OK"}} default button "OK"'
    )
    try:
        subprocess.run(
            ["osascript", "-e", script],
            capture_output=True, text=True, timeout=30,
        )
    except Exception:
        logger.debug("osascript info dialog failed", exc_info=True)


# ---------------------------------------------------------------------------
# tkinter dialogs (Windows / Linux)
# ---------------------------------------------------------------------------

def _ensure_root():  # type: ignore[no-untyped-def]
    """Get or create a hidden tkinter root window."""
    import tkinter as tk

    try:
        root = tk._default_root  # type: ignore[attr-defined]
        if root is not None and root.winfo_exists():
            return root
    except Exception:
        pass
    root = tk.Tk()
    root.withdraw()
    return root


def _tk_input_dialog(title: str, message: str, default: str = "") -> str | None:
    """Show a tkinter input dialog."""
    from tkinter import simpledialog

    root = _ensure_root()
    return simpledialog.askstring(title, message, initialvalue=default, parent=root)


def _tk_output_dialog(title: str, result: str) -> bool:
    """Show output in a tkinter dialog with a Copy button."""
    import tkinter as tk

    root = _ensure_root()
    copied = False

    win = tk.Toplevel(root)
    win.title(title)
    win.geometry("500x400")
    win.resizable(True, True)

    text_widget = tk.Text(win, wrap=tk.WORD, padx=10, pady=10)
    text_widget.insert("1.0", result)
    text_widget.config(state=tk.DISABLED)
    text_widget.pack(fill=tk.BOTH, expand=True)

    btn_frame = tk.Frame(win)
    btn_frame.pack(fill=tk.X, padx=10, pady=10)

    def on_copy() -> None:
        nonlocal copied
        copied = True
        win.destroy()

    tk.Button(btn_frame, text="Copy to Clipboard", command=on_copy).pack(side=tk.RIGHT, padx=5)
    tk.Button(btn_frame, text="Close", command=win.destroy).pack(side=tk.RIGHT, padx=5)

    win.transient(root)
    win.grab_set()
    win.focus_force()
    root.wait_window(win)
    return copied


def _tk_error_dialog(title: str, message: str) -> None:
    """Show a tkinter error dialog."""
    from tkinter import messagebox

    root = _ensure_root()
    messagebox.showerror(title, message, parent=root)


def _tk_info_dialog(title: str, message: str) -> None:
    """Show a tkinter info dialog."""
    from tkinter import messagebox

    root = _ensure_root()
    messagebox.showinfo(title, message, parent=root)


# ---------------------------------------------------------------------------
# Platform-dispatched public API
# ---------------------------------------------------------------------------

def _input_dialog(title: str, message: str, default: str = "") -> str | None:
    if _IS_MACOS:
        return _osa_input_dialog(title, message, default)
    return _tk_input_dialog(title, message, default)


def _output_dialog(title: str, result: str) -> bool:
    if _IS_MACOS:
        return _osa_output_dialog(title, result)
    return _tk_output_dialog(title, result)


def _error_dialog(title: str, message: str) -> None:
    if _IS_MACOS:
        _osa_error_dialog(title, message)
    else:
        _tk_error_dialog(title, message)


def info_dialog(title: str, message: str) -> None:
    """Show an informational dialog (used by app.py)."""
    if _IS_MACOS:
        _osa_info_dialog(title, message)
    else:
        _tk_info_dialog(title, message)


def _clean_for_copy(result: str) -> str:
    """Strip display-only metadata from result before copying."""
    return _METADATA_RE.sub("", result).strip()


def show_tool_dialog(tool: DevTool, input_text: str = "") -> None:
    """Show input window, process with tool, show output, offer clipboard copy."""
    text = _input_dialog(
        title=tool.name,
        message=tool.description or f"Enter input for {tool.name}",
        default=input_text,
    )
    if text is None:
        return

    error = tool.validate(text)
    if error:
        _error_dialog("GadgetBox Error", error)
        return

    try:
        result = tool.process(text)
    except Exception as e:
        _error_dialog("GadgetBox Error", str(e))
        return

    if _output_dialog(f"{tool.name} - Result", result):
        clipboard.write(_clean_for_copy(result))
        notify_copied()


def show_multi_input_dialog(
    tool: DevTool,
    fields: list[tuple[str, str]],
) -> list[str] | None:
    """Show sequential input dialogs for tools needing multiple inputs."""
    values: list[str] = []
    for label, default in fields:
        text = _input_dialog(title=tool.name, message=label, default=default)
        if text is None:
            return None
        values.append(text)
    return values
