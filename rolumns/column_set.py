from typing import Any, List, Optional, Union

from rolumns.column import Column
from rolumns.data_resolver import DataResolver
from rolumns.exceptions import MultipleRepeaters
from rolumns.populated_columns import PopulatedColumns
from rolumns.source import Source


class ColumnSet:
    """
    A set of columns.

    `path` describes the root record path for the set's columns to read data
    from. This is likely to be empty for the root column set and set only to
    describe iteration in child sets.
    """

    def __init__(self, path: Optional[str] = None) -> None:
        self._columns: List[Column] = []
        self._path = path
        self._repeater: Optional[ColumnSet] = None

    def add(self, name: str, source: Union[Source, str]) -> None:
        """
        Adds a column.

        `source` can be either an explicit `Source` or a path to the value.
        """

        source = Source(source) if isinstance(source, str) else source
        column = Column(name, source)
        self._columns.append(column)

    def create_repeater(self, path: str) -> "ColumnSet":
        """
        Creates and attaches a repeating column set.

        `path` is the relative path to the repeating data source.

        A column set cannot have multiple repeaters as direct children, thought
        it can have an unlimited number of repeaters as descendants. Will raise
        `MultipleRepeaters` if you try to add a second repeater here.
        """

        if self._repeater:
            raise MultipleRepeaters()

        self._repeater = ColumnSet(path)
        return self._repeater

    def make_populated_columns(self, data: Any) -> PopulatedColumns:
        """
        Resolved `data` to populated columns.
        """

        columns = PopulatedColumns()

        for datum in DataResolver(data).resolve(self._path):
            inner = PopulatedColumns()

            for c in self._columns:
                inner.append(c.name, c.source.read(datum))

            if self._repeater:
                inner.extend(self._repeater.make_populated_columns(datum))

            inner.fill_gaps()
            columns.extend(inner)

        return columns

    def names(self) -> List[str]:
        """
        Gets the names of the columns within this set and its children.
        """

        names: List[str] = []

        for c in self._columns:
            names.append(c.name)

        if self._repeater:
            names.extend(self._repeater.names())

        return names
