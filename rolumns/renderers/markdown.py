from io import StringIO
from typing import Any, Dict, Iterable, List, Optional

from rolumns.columns import Columns
from rolumns.renderers.rows import RowsRenderer


class MarkdownRenderer:
    """
    Renders the set of columns :code:`columns` to an iterable list of strings
    that make up a Markdown table row-by-row.

    All columns will be rendered by default. To specify columns and their order,
    pass :code:`mask` and/or call :func:`MarkdownRenderer.append`.

    .. testcode::

        from rolumns import Columns
        from rolumns.renderers import MarkdownRenderer

        data = [
            {
                "name": "Robert Pringles",
                "email": "bob@pringles.pop",
            },
            {
                "name": "Daniel Sausage",
                "email": "danny@pringles.pop",
            },
            {
                "name": "Charlie Marmalade",
                "email": "charlie@pringles.pop",
            },
        ]

        columns = Columns()
        columns.add("Name", "name")
        columns.add("Email", "email")

        renderer = MarkdownRenderer(columns)
        rows = renderer.render(data)

        print(list(rows))

    .. testoutput::
       :options: +NORMALIZE_WHITESPACE

        ['| Name | Email |',
         '| - | - |',
         '| Robert Pringles | bob@pringles.pop |',
         '| Daniel Sausage | danny@pringles.pop |',
         '| Charlie Marmalade | charlie@pringles.pop |']
    """

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
        Translates :code:`data` into an iterable list of strings that make up a
        Markdown table row-by-row.
        """

        rows = self._rows.render(data)

        for index, row in enumerate(rows):
            yield "| " + " | ".join([str(c) for c in row]) + " |"
            if index == 0:
                yield "| " + " | ".join("-" * len(row)) + " |"

    def render_string(self, data: Any) -> str:
        """
        Translates :code:`data` into a Markdown table.
        """

        rows = self._rows.render(data)
        raw: List[List[str]] = []
        maxes: Dict[int, int] = {}

        for row in rows:
            raw_row: List[str] = []
            for index, cell in enumerate(row):
                value = str(cell)
                maxes[index] = max(maxes.get(index, 0), len(value))
                raw_row.append(value)
            raw.append(raw_row)

        result = StringIO()

        for index, raw_row in enumerate(raw):
            for column_index, column_value in enumerate(raw_row):
                result.write("| ")
                result.write(column_value.ljust(maxes[column_index] + 1))
            result.write("|\n")
            if index == 0:
                for column_index, column_value in enumerate(raw_row):
                    result.write("| ")
                    result.write("-" * maxes[column_index])
                    result.write(" ")
                result.write("|\n")

        return result.getvalue()
