from io import StringIO
from typing import Any, Dict, Iterable, List, Optional

from rolumns.columns import Columns
from rolumns.enums import ColumnAlignment
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
        self._alignments: Dict[str, ColumnAlignment] = {}

    def _make_header_separator(
        self,
        column_count: int,
        alignments: Optional[Dict[int, ColumnAlignment]] = None,
        widths: Optional[Dict[int, int]] = None,
    ) -> str:
        """
        Makes the row that separates column headers from values.
        """

        alignments = alignments or {}
        widths = widths or {}

        wip = "| "

        for i in range(column_count):
            if i > 0:
                wip += " | "

            dash_count = widths.get(i, 1)
            if i in alignments:
                dash_count -= 1

            column_alignment = alignments.get(i, None)

            prefix = ":" if column_alignment == ColumnAlignment.LEFT else ""
            suffix = ":" if column_alignment == ColumnAlignment.RIGHT else ""

            wip += prefix
            wip += "-" * dash_count
            wip += suffix

        wip += " |"
        return wip

    def append(
        self,
        column: str,
        alignment: Optional[ColumnAlignment] = None,
    ) -> None:
        """
        Appends a column to the table.
        """

        self._rows.append(column)

        if alignment:
            self._alignments[column] = alignment

    @staticmethod
    def length(value: str) -> int:
        """
        Calculates the displayable width of a string.
        """

        return int(len(value.encode(encoding="utf_16_le")) / 2)

    @staticmethod
    def pad(
        value: str,
        length: int,
        align: Optional[ColumnAlignment] = None,
    ) -> str:
        """
        Pads a string to a displayable width.
        """

        if align == ColumnAlignment.RIGHT:
            length -= 1

        p = length - MarkdownRenderer.length(value)

        padding = "" if p <= 0 else (" " * p)

        if align in (None, ColumnAlignment.LEFT):
            return value + padding

        return padding + value + " "

    def render(
        self,
        data: Optional[Any] = None,
    ) -> Iterable[str]:
        """
        Translates :code:`data` into an iterable list of strings that make up a
        Markdown table row-by-row.
        """

        rows = self._rows.render(data)

        for index, row in enumerate(rows):
            yield "| " + " | ".join([str(c) for c in row]) + " |"
            if index == 0:
                yield self._make_header_separator(len(row))

    def render_string(
        self,
        data: Optional[Any] = None,
    ) -> str:
        """
        Translates :code:`data` into a Markdown table.
        """

        rows = self._rows.render(data)

        aligns: Dict[int, ColumnAlignment] = {}
        raw: List[List[str]] = []
        widths: Dict[int, int] = {}

        for row_index, row in enumerate(rows):
            if row_index == 0 and self._alignments:
                for column_index, column_name in enumerate(row):
                    if column_name in self._alignments:
                        aligns[column_index] = self._alignments[column_name]

            raw_row: List[str] = []
            for index, cell in enumerate(row):
                value = "" if cell is None else str(cell)
                widths[index] = max(widths.get(index, 0), self.length(value))
                raw_row.append(value)
            raw.append(raw_row)

        result = StringIO()

        for index, raw_row in enumerate(raw):
            for column_index, cell in enumerate(raw_row):
                result.write("| ")
                cell = MarkdownRenderer.pad(
                    cell,
                    widths[column_index] + 1,
                    align=aligns.get(column_index, None),
                )
                result.write(cell)
            result.write("|\n")
            if index == 0:
                result.write(
                    self._make_header_separator(
                        len(raw_row),
                        alignments=aligns,
                        widths=widths,
                    )
                )
                result.write("\n")

        return result.getvalue()
