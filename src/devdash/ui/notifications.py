"""macOS native notifications helper."""

import rumps


def notify(title: str, message: str, subtitle: str = "") -> None:
    """Show a macOS notification with consistent DevDash styling."""
    rumps.notification(
        title=title,
        subtitle=subtitle,
        message=message,
    )


def notify_copied() -> None:
    """Show 'Copied to clipboard' notification."""
    notify("DevDash", "Copied to clipboard!")


def notify_error(message: str) -> None:
    """Show an error notification."""
    notify("DevDash - Error", message)
