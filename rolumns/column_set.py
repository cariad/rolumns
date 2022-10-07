from typing import Any, Iterable, List, Optional, Union

from rolumns.column import Column
from rolumns.populated_columns import PopulatedColumns


class ColumnSet:
    """
    A set of columns.

    `path` describes the root record path for the set's columns to read data
    from. This is likely to be empty for the root column set and set only to
    describe iteration in child sets.
    """

    def __init__(self, path: Optional[str] = None) -> None:
        self._columns: List[Union[Column, "ColumnSet"]] = []
        self._path = path

    def append(self, column: Union[Column, "ColumnSet"]) -> None:
        """
        Appends one or more columns.
        """

        self._columns.append(column)

    def make_populated_columns(self, data: Any) -> PopulatedColumns:
        """
        Resolved `data` to populated columns.
        """

        columns = PopulatedColumns()

        if isinstance(data, list):
            data_list: Iterable[Any] = data
        else:
            data_list = [data]

        for datum in data_list:
            datum = datum[self._path] if self._path else datum
            inner_columns = PopulatedColumns()

            for c in self._columns:
                if isinstance(c, Column):
                    inner_columns.append(c.name, c.source.read(datum))
                else:
                    inner_columns.extend(c.make_populated_columns(datum))

            inner_columns.fill_gaps()
            columns.extend(inner_columns)

        return columns

    def names(self) -> List[str]:
        """
        Gets the names of the columns within this set and its children.
        """

        names: List[str] = []

        for c in self._columns:
            if isinstance(c, Column):
                names.append(c.name)
            else:
                names.extend(c.names())

        return names

    def rows(self, data: Any) -> List[List[Any]]:
        """
        Translates `data` into a series of rows.
        """

        columns = self.make_populated_columns(data)
        names = self.names()
        rows: List[List[Any]] = [names]

        for row_index in range(columns.height()):
            row: List[Any] = []

            for name in names:
                row.append(columns.get(name, row_index))

            rows.append(row)

        return rows
