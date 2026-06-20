"""Shared utilities for PharmaBridge backend."""

from datetime import datetime, timezone


def utcnow_iso() -> str:
    """Returns the current UTC time as an ISO 8601 string."""
    return datetime.now(timezone.utc).isoformat()


def safe_truncate(text: str, max_length: int = 200) -> str:
    """Truncates text to the given length, adding an ellipsis if it was truncated."""
    if not text:
        return ""
    text = text.strip()
    if len(text) <= max_length:
        return text
    return text[: max_length - 1].rstrip() + "…"
