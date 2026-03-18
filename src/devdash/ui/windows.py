"""Custom dialog wrappers using osascript for reliable macOS dialogs."""

from __future__ import annotations

import logging
import re
import subprocess
from typing import TYPE_CHECKING

from devdash import clipboard
from devdash.ui.notifications import notify_copied

if TYPE_CHECKING:
    from devdash.tools.base import DevTool

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


def _escape(text: str) -> str:
    """Escape text for use inside AppleScript strings."""
    return (
        text.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", "\\n")
        .replace("\r", "")
        .replace("\t", "\\t")
    )


def _input_dialog(title: str, message: str, default: str = "") -> str | None:
    """Show a native macOS input dialog via osascript.

    Returns the entered text, or None if cancelled.
    """
    script = (
        f'display dialog "{_escape(message)}" '
        f'default answer "{_escape(default)}" '
        f'with title "{_escape(title)}" '
        f'buttons {{"Cancel", "Process"}} default button "Process"'
        "\n"
        "return text returned of result"
    )
    try:
        r = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True,
            text=True,
            timeout=300,
        )
        if r.returncode == 0:
            return r.stdout.strip()
    except subprocess.TimeoutExpired:
        logger.warning("Input dialog timed out for %s", title)
    except Exception:
        logger.exception("Failed to show input dialog")
    return None


def _output_dialog(title: str, result: str) -> bool:
    """Show a native macOS output dialog via osascript.

    Returns True if the user clicked 'Copy to Clipboard'.
    """
    # Truncate very long results for the dialog display
    display = result if len(result) <= 1000 else result[:997] + "..."
    script = (
        f'display dialog "{_escape(display)}" '
        f'with title "{_escape(title)}" '
        f'buttons {{"Close", "Copy to Clipboard"}} '
        f'default button "Copy to Clipboard"'
    )
    try:
        r = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True,
            text=True,
            timeout=300,
        )
        if r.returncode == 0:
            return "Copy to Clipboard" in r.stdout
    except Exception:
        logger.exception("Failed to show output dialog")
    return False


def _error_dialog(title: str, message: str) -> None:
    """Show a native macOS error alert via osascript."""
    script = (
        f'display alert "{_escape(title)}" '
        f'message "{_escape(message)}" as critical'
    )
    try:
        subprocess.run(
            ["osascript", "-e", script],
            capture_output=True,
            timeout=10,
        )
    except Exception:
        logger.exception("Failed to show error dialog")


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
        _error_dialog("DevDash Error", error)
        return

    try:
        result = tool.process(text)
    except Exception as e:
        _error_dialog("DevDash Error", str(e))
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
