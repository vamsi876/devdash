"""Cross-platform dialog wrappers using tkinter."""

from __future__ import annotations

import logging
import re
import tkinter as tk
from tkinter import messagebox, simpledialog
from typing import TYPE_CHECKING

from gadgetbox import clipboard
from gadgetbox.ui.notifications import notify_copied

if TYPE_CHECKING:
    from gadgetbox.tools.base import DevTool

logger = logging.getLogger(__name__)

# Metadata patterns to strip when copying output
_METADATA_RE = re.compile(
    r"\s*\(entropy:.*?\)"  # password entropy
    r"|\n\nOriginal bytes:.*"  # base64 byte counts
    r"|\n\nEncoded bytes:.*"
    r"|\n\n\[Auto-detected.*?\]"  # base64 auto-detect label
    r"|\n\nWarning:.*",  # JWT warning
    re.DOTALL,
)


def _ensure_root() -> tk.Tk:
    """Get or create a hidden tkinter root window."""
    try:
        root = tk._default_root  # type: ignore[attr-defined]
        if root is not None and root.winfo_exists():
            return root
    except Exception:
        pass
    root = tk.Tk()
    root.withdraw()
    return root


def _input_dialog(title: str, message: str, default: str = "") -> str | None:
    """Show an input dialog. Returns entered text, or None if cancelled."""
    root = _ensure_root()
    result = simpledialog.askstring(
        title,
        message,
        initialvalue=default,
        parent=root,
    )
    return result


def _output_dialog(title: str, result: str) -> bool:
    """Show output in a dialog with a Copy button.

    Returns True if the user clicked 'Copy to Clipboard'.
    """
    root = _ensure_root()
    copied = False

    win = tk.Toplevel(root)
    win.title(title)
    win.geometry("500x400")
    win.resizable(True, True)

    # Text display
    text_widget = tk.Text(win, wrap=tk.WORD, padx=10, pady=10)
    text_widget.insert("1.0", result)
    text_widget.config(state=tk.DISABLED)
    text_widget.pack(fill=tk.BOTH, expand=True)

    # Button frame
    btn_frame = tk.Frame(win)
    btn_frame.pack(fill=tk.X, padx=10, pady=10)

    def on_copy() -> None:
        nonlocal copied
        copied = True
        win.destroy()

    def on_close() -> None:
        win.destroy()

    tk.Button(btn_frame, text="Copy to Clipboard", command=on_copy).pack(side=tk.RIGHT, padx=5)
    tk.Button(btn_frame, text="Close", command=on_close).pack(side=tk.RIGHT, padx=5)

    # Make modal
    win.transient(root)
    win.grab_set()
    win.focus_force()
    root.wait_window(win)

    return copied


def _error_dialog(title: str, message: str) -> None:
    """Show an error alert dialog."""
    root = _ensure_root()
    messagebox.showerror(title, message, parent=root)


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
    """Show sequential input dialogs for tools needing multiple inputs.

    Args:
        tool: The tool instance.
        fields: List of (label, default_value) tuples.

    Returns:
        List of input values, or None if cancelled.
    """
    values: list[str] = []
    for label, default in fields:
        text = _input_dialog(
            title=tool.name,
            message=label,
            default=default,
        )
        if text is None:
            return None
        values.append(text)
    return values
