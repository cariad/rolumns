from typing import Any


class TranslationFailed(Exception):
    """
    Raised when a value translation fails.
    """

    def __init__(self, value: Any, reason: str) -> None:
        msg = f"Failed to translate {repr(value)} ({reason})"
        super().__init__(msg)
