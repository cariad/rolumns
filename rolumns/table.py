from typing import Any, Iterable, List, Optional

from rolumns.column_set import ColumnSet


class Table:
    """
    A table of data in rows and columns.

    The `root` column set is required. Child column sets will be discovered
    automatically.

    All known columns will be rendered by default. To specify columns and their
    order, pass `ordered_columns` and/or call `append`.
    """

    def __init__(
        self,
        root: ColumnSet,
        ordered_columns: Optional[List[str]] = None,
    ) -> None:
        self._ordered_column_ids = ordered_columns or []
        self.column_set = root

    def append(self, id: str) -> None:
        """
        Appends a column to the table.
        """

        self._ordered_column_ids.append(id)

    def rows(self, data: Any) -> Iterable[List[Any]]:
        """
        Translates `data` into a series of rows.
        """

        column_ids = self._ordered_column_ids or self.column_set.names()
        yield column_ids

        columns = self.column_set.make_populated_columns(data)

        for row_index in range(columns.height()):
            row: List[Any] = []

            for column_id in column_ids:
                row.append(columns.get(column_id, row_index))

            yield row
