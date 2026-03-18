"""Dynamic tool discovery and registration."""

import importlib
import logging
import pkgutil
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from devdash.tools.base import DevTool

logger = logging.getLogger(__name__)


def discover_tools() -> list["DevTool"]:
    """Scan the tools/ directory and return registered tool instances."""
    tools: list[DevTool] = []
    package_name = "devdash.tools"

    try:
        package = importlib.import_module(package_name)
    except ImportError:
        logger.error("Could not import tools package")
        return tools

    package_path = getattr(package, "__path__", None)
    if package_path is None:
        return tools

    for _importer, module_name, _ispkg in pkgutil.iter_modules(package_path):
        if module_name.startswith("_") or module_name == "base":
            continue
        try:
            module = importlib.import_module(f"{package_name}.{module_name}")
            register_fn = getattr(module, "register", None)
            if register_fn and callable(register_fn):
                tool = register_fn()
                tools.append(tool)
        except Exception:
            logger.exception("Failed to load tool module: %s", module_name)

    # Sort by category then name
    tools.sort(key=lambda t: (t.category, t.name))
    return tools
