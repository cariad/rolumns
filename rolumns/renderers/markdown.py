from typing import Any, Iterable, List, Optional

from rolumns.columns import Columns
from rolumns.renderers.rows import RowsRenderer


class MarkdownRenderer:
    def __init__(
        self,
        columns: Columns,
        mask: Optional[List[str]] = None,
    ) -> None:
        self._rows = RowsRenderer(columns, mask=mask)

    def append(self, column: str) -> None:
        """
        Appends a column to the table.
        """

        self._rows.append(column)

    def render(self, data: Any) -> Iterable[str]:
        """
        Translates `data` into an iterable list of strings which make up a
        Markdown table row-by-row.
        """

        rows = self._rows.render(data)

        for index, row in enumerate(rows):
            yield "| " + " | ".join(row) + " |"
            if index == 0:
                yield "| " + " | ".join("-" * len(row)) + " |"
