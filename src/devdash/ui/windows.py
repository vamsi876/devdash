"""Custom rumps.Window wrappers for consistent tool UI."""

from __future__ import annotations

from typing import TYPE_CHECKING

import rumps

from devdash import clipboard
from devdash.ui.notifications import notify_copied, notify_error

if TYPE_CHECKING:
    from devdash.tools.base import DevTool


def show_tool_dialog(tool: DevTool, input_text: str = "") -> None:
    """Show input window, process with tool, show output, offer clipboard copy."""
    window = rumps.Window(
        message=tool.description or f"Enter input for {tool.name}",
        title=tool.name,
        default_text=input_text,
        ok="Process",
        cancel="Cancel",
        dimensions=(320, 200),
    )
    response = window.run()
    if not response.clicked:
        return

    text = response.text
    error = tool.validate(text)
    if error:
        notify_error(error)
        return

    try:
        result = tool.process(text)
    except Exception as e:
        notify_error(f"Error: {e}")
        return

    # Show output window
    output_window = rumps.Window(
        message="Result (click OK to copy to clipboard):",
        title=f"{tool.name} - Output",
        default_text=result,
        ok="Copy to Clipboard",
        cancel="Close",
        dimensions=(320, 200),
    )
    out_response = output_window.run()
    if out_response.clicked:
        clipboard.write(result)
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
        window = rumps.Window(
            message=label,
            title=tool.name,
            default_text=default,
            ok="Next" if len(values) < len(fields) - 1 else "Process",
            cancel="Cancel",
            dimensions=(320, 150),
        )
        response = window.run()
        if not response.clicked:
            return None
        values.append(response.text)
    return values
