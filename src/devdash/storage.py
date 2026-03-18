"""Optional SQLite storage for tool history and favorites.

The database is created lazily on first access and stored at
~/.config/devdash/history.db with restricted (0o600) permissions.
All public methods are thread-safe — each call opens its own
connection so there is no shared state between threads.
"""

import os
import sqlite3
import threading
from pathlib import Path

from devdash.config import CONFIG_DIR

DB_PATH: Path = CONFIG_DIR / "history.db"
_PREVIEW_MAX = 200
_HISTORY_KEEP = 100

_init_lock = threading.Lock()
_initialized = False


def _truncate(text: str | None, limit: int = _PREVIEW_MAX) -> str | None:
    """Truncate *text* to *limit* characters, appending an ellipsis if cut."""
    if text is None:
        return None
    if len(text) <= limit:
        return text
    return text[: limit - 1] + "\u2026"


def _ensure_db() -> None:
    """Create the database file and tables if they do not yet exist.

    Uses a module-level lock so the schema is applied at most once per
    process, regardless of how many threads call in concurrently.
    """
    global _initialized
    if _initialized:
        return

    with _init_lock:
        # Double-check after acquiring the lock.
        if _initialized:
            return

        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        con = sqlite3.connect(str(DB_PATH))
        try:
            con.executescript(
                """\
                CREATE TABLE IF NOT EXISTS tool_history (
                    id              INTEGER PRIMARY KEY AUTOINCREMENT,
                    tool_name       TEXT    NOT NULL,
                    input_preview   TEXT,
                    output_preview  TEXT,
                    timestamp       TEXT    DEFAULT CURRENT_TIMESTAMP
                );

                CREATE INDEX IF NOT EXISTS idx_tool_history_tool
                    ON tool_history (tool_name, timestamp DESC);

                CREATE TABLE IF NOT EXISTS favorites (
                    id        INTEGER PRIMARY KEY AUTOINCREMENT,
                    tool_name TEXT NOT NULL,
                    label     TEXT NOT NULL,
                    content   TEXT NOT NULL
                );

                CREATE INDEX IF NOT EXISTS idx_favorites_tool
                    ON favorites (tool_name);
                """
            )
        finally:
            con.close()

        os.chmod(DB_PATH, 0o600)
        _initialized = True


def _connect() -> sqlite3.Connection:
    """Return a new connection to the history database.

    Ensures the schema exists before handing back the connection.
    """
    _ensure_db()
    con = sqlite3.connect(str(DB_PATH))
    con.row_factory = sqlite3.Row
    return con


class HistoryStore:
    """High-level interface to the DevDash history / favorites database.

    Supports use as a context manager::

        with HistoryStore() as store:
            store.add_history("base64", "hello", "aGVsbG8=")

    When used without a context manager, call :meth:`close` explicitly
    or simply let the garbage collector handle it — each public method
    opens (and closes) its own connection, so the instance itself holds
    no long-lived resources.
    """

    def __init__(self) -> None:
        self._closed = False

    # -- context manager ----------------------------------------------------

    def __enter__(self) -> "HistoryStore":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:  # noqa: ANN001
        self.close()
        return None

    def close(self) -> None:
        """Mark the store as closed.  Subsequent calls will raise."""
        self._closed = True

    def _check_open(self) -> None:
        if self._closed:
            raise RuntimeError("HistoryStore is closed")

    # -- tool_history -------------------------------------------------------

    def add_history(
        self,
        tool_name: str,
        input_text: str | None = None,
        output_text: str | None = None,
    ) -> None:
        """Record a tool invocation, then auto-cleanup old rows."""
        self._check_open()
        in_prev = _truncate(input_text)
        out_prev = _truncate(output_text)
        con = _connect()
        try:
            con.execute(
                "INSERT INTO tool_history (tool_name, input_preview, output_preview) "
                "VALUES (?, ?, ?)",
                (tool_name, in_prev, out_prev),
            )
            con.commit()
        finally:
            con.close()
        self.cleanup(tool_name)

    def get_history(self, tool_name: str, limit: int = 20) -> list[dict]:
        """Return the most recent *limit* history rows for *tool_name*."""
        self._check_open()
        con = _connect()
        try:
            rows = con.execute(
                "SELECT id, tool_name, input_preview, output_preview, timestamp "
                "FROM tool_history "
                "WHERE tool_name = ? "
                "ORDER BY timestamp DESC "
                "LIMIT ?",
                (tool_name, limit),
            ).fetchall()
            return [dict(r) for r in rows]
        finally:
            con.close()

    # -- favorites ----------------------------------------------------------

    def add_favorite(self, tool_name: str, label: str, content: str) -> int:
        """Save a favorite and return its row id."""
        self._check_open()
        con = _connect()
        try:
            cur = con.execute(
                "INSERT INTO favorites (tool_name, label, content) VALUES (?, ?, ?)",
                (tool_name, label, content),
            )
            con.commit()
            return cur.lastrowid  # type: ignore[return-value]
        finally:
            con.close()

    def get_favorites(self, tool_name: str) -> list[dict]:
        """Return all favorites for *tool_name*, ordered by id."""
        self._check_open()
        con = _connect()
        try:
            rows = con.execute(
                "SELECT id, tool_name, label, content "
                "FROM favorites "
                "WHERE tool_name = ? "
                "ORDER BY id",
                (tool_name,),
            ).fetchall()
            return [dict(r) for r in rows]
        finally:
            con.close()

    def remove_favorite(self, favorite_id: int) -> bool:
        """Delete a favorite by id.  Returns True if a row was deleted."""
        self._check_open()
        con = _connect()
        try:
            cur = con.execute("DELETE FROM favorites WHERE id = ?", (favorite_id,))
            con.commit()
            return cur.rowcount > 0
        finally:
            con.close()

    # -- maintenance --------------------------------------------------------

    def cleanup(self, tool_name: str | None = None) -> None:
        """Trim tool_history to the newest *_HISTORY_KEEP* rows per tool.

        If *tool_name* is given, only that tool is cleaned.  Otherwise
        every tool present in the table is processed.
        """
        self._check_open()
        con = _connect()
        try:
            if tool_name is not None:
                tools = [tool_name]
            else:
                tools = [
                    row["tool_name"]
                    for row in con.execute("SELECT DISTINCT tool_name FROM tool_history").fetchall()
                ]

            for name in tools:
                con.execute(
                    "DELETE FROM tool_history "
                    "WHERE tool_name = ? "
                    "AND id NOT IN ("
                    "  SELECT id FROM tool_history "
                    "  WHERE tool_name = ? "
                    "  ORDER BY timestamp DESC "
                    "  LIMIT ?"
                    ")",
                    (name, name, _HISTORY_KEEP),
                )
            con.commit()
        finally:
            con.close()
