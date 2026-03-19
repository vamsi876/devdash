"""Cross-platform desktop notifications."""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


def notify(title: str, message: str, subtitle: str = "") -> None:
    """Show a desktop notification with consistent GadgetBox styling."""
    try:
        from plyer import notification

        full_message = f"{subtitle}\n{message}" if subtitle else message
        notification.notify(
            title=title,
            message=full_message,
            app_name="GadgetBox",
            timeout=5,
        )
    except Exception:
        logger.debug("Desktop notification failed", exc_info=True)


def notify_copied() -> None:
    """Show 'Copied to clipboard' notification."""
    notify("GadgetBox", "Copied to clipboard!")


def notify_error(message: str) -> None:
    """Show an error notification."""
    notify("GadgetBox - Error", message)
