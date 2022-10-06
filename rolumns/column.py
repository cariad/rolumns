from typing import Generic

from rolumns.column_source import ColumnSource
from rolumns.types import TColumnData


class Column(Generic[TColumnData]):
    """
    A column to render.
    """

    def __init__(self, name: str, source: ColumnSource[TColumnData]) -> None:
        self.name = name
        self.source = source
