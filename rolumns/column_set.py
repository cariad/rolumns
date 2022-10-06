from typing import Any, List

from rolumns.column import Column


class ColumnSet:
    """
    A set of columns.
    """

    def __init__(self) -> None:
        self._columns: List[Column[Any]] = []

    def append(self, column: Column[Any]) -> None:
        """
        Appends a column to the set.
        """

        self._columns.append(column)

    def rows(self, data: Any) -> List[List[Any]]:
        """
        Translates `data` into a series of rows.
        """

        rows: List[List[Any]] = [
            [c.name for c in self._columns],
        ]

        row: List[Any] = []

        for c in self._columns:
            row.append(c.source.resolve_from(data))

        rows.append(row)
        return rows
