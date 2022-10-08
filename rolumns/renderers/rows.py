from typing import Any, Iterable, List, Optional

from rolumns.columns import Columns


class RowsRenderer:
    """
    Renders the set of columns `columns` to an iterable list of rows.

    All known columns will be rendered by default. To specify columns and their
    order, pass `mask` and/or call `append`.
    """

    def __init__(
        self,
        columns: Columns,
        mask: Optional[List[str]] = None,
    ) -> None:
        self._columns = columns
        self._mask = mask or []

    def append(self, column: str) -> None:
        """
        Appends a column to the table.
        """

        self._mask.append(column)

    def render(self, data: Any) -> Iterable[List[Any]]:
        """
        Translates `data` into an iterable list of rows.
        """

        column_ids = self._mask or self._columns.names()
        yield column_ids

        columns = self._columns.make_populated_columns(data)

        for row_index in range(columns.height()):
            row: List[Any] = []

            for column_id in column_ids:
                row.append(columns.get(column_id, row_index))

            yield row
