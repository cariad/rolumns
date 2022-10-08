from typing import Any, List, Optional, Union

from rolumns.column import Column
from rolumns.exceptions import MultipleRepeaters
from rolumns.groups import ByPath, Group
from rolumns.populated_columns import PopulatedColumns
from rolumns.source import Source


class Columns:
    """
    A set of columns.
    """

    def __init__(self, group: Optional[Group] = None) -> None:
        self._columns: List[Column] = []
        self._group = group or ByPath()
        self._grouped_set: Optional[Columns] = None

    def add(self, name: str, source: Union[Source, str]) -> None:
        """
        Adds a column.

        `source` can be either an explicit `Source` or a path to the value.
        """

        source = Source(source) if isinstance(source, str) else source
        column = Column(name, source)
        self._columns.append(column)

    def add_grouped_set(self, group: Union[Group, str]) -> "Columns":
        """
        Creates and adds a grouped column set.

        A column set cannot have multiple repeaters as direct children, thought
        it can have an unlimited number of repeaters as descendants. Will raise
        `MultipleRepeaters` if you try to add a second repeater here.
        """

        if self._grouped_set:
            raise MultipleRepeaters()

        group = group if isinstance(group, Group) else ByPath(group)
        self._grouped_set = Columns(group)
        return self._grouped_set

    def make_populated_columns(self, data: Any) -> PopulatedColumns:
        """
        Resolved `data` to populated columns.
        """

        columns = PopulatedColumns()

        for datum in self._group.resolve(data):
            inner = PopulatedColumns()

            for c in self._columns:
                inner.append(c.name, c.source.read(datum))

            if self._grouped_set:
                inner.extend(self._grouped_set.make_populated_columns(datum))

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

        if self._grouped_set:
            names.extend(self._grouped_set.names())

        return names
