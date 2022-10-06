from typing import Dict, Generic

from rolumns.types import TColumnData


class ColumnSource(Generic[TColumnData]):
    def __init__(self, path: str) -> None:
        self.path = path

    def resolve_from(self, data: Dict[str, TColumnData]) -> TColumnData:
        return data[self.path]
