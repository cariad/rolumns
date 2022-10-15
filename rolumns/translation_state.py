from dataclasses import dataclass
from typing import Any


@dataclass
class TranslationState:
    value: Any
    """
    The original value.
    """
