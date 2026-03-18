"""Abstract base class for all DevDash tools."""

from abc import ABC, abstractmethod


class DevTool(ABC):
    """Base class for all DevDash tools."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Display name in the menu."""
        ...

    @property
    @abstractmethod
    def keyword(self) -> str:
        """Short identifier for CLI and auto-detection."""
        ...

    @property
    def category(self) -> str:
        """Menu category grouping."""
        return "General"

    @property
    def description(self) -> str:
        """One-line description shown in tooltip."""
        return ""

    @abstractmethod
    def process(self, input_text: str, **kwargs: object) -> str:
        """Process input and return output string."""
        ...

    def validate(self, input_text: str) -> str | None:
        """Validate input. Return error message or None if valid."""
        return None
