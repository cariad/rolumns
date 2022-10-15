from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class TranslationState:
    path: Optional[str]
    """
    The original value's data source path.
    """

    record: Any
    """
    The original value's source record.
    """

    value: Any
    """
    The original value.
    """
