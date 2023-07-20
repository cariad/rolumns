from typing import Any, Iterable, List, Optional

from rolumns.columns import Columns
from rolumns.logging import logger


class RowsRenderer:
    """
    Renders the set of columns :code:`columns` to an iterable list of rows.

    All columns will be rendered by default. To specify columns and their order,
    pass :code:`mask` and/or call :func:`RowsRenderer.append`.
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

    def render(self) -> Iterable[List[Any]]:
        """
        Translates :code:`data` into an iterable list of rows.
        """

        logger.debug("Started rendering rows")

        column_ids = self._mask or self._columns.names()

        logger.debug("Yielding column IDs: %s", column_ids)
        yield column_ids

        columns = self._columns.to_column_values()
        height = 0

        for _, value in columns.items():
            if height > 0 and height != len(value):
                raise Exception
            height = max(height, len(value))

            logger.debug(
                "Max height after checking %s (%i) is %i",
                value,
                len(value),
                height,
            )

        for row_index in range(height):
            row: List[Any] = []

            for column_id in column_ids:
                row.append(columns[column_id][row_index])

            yield row
