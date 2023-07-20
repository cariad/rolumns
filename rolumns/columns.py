from typing import Any, Dict, Iterable, List, Optional, Tuple, Union

from rolumns.by_path import ByPath
from rolumns.column import Column
from rolumns.data_navigator import DataNavigator
from rolumns.exceptions import MultipleGroups
from rolumns.group import Group
from rolumns.logging import dump, is_debug, logger
from rolumns.source import Source


class Columns:
    """
    A set of columns.

    .. testcode::

        from rolumns import Columns

        data = [
            {
                "name": "Robert Pringles",
                "email": "bob@pringles.pop",
            },
        ]

        columns = Columns()
        columns.add("Name", "name")
        columns.add("Email", "email")
    """

    def __init__(
        self,
        group: Optional[Union[DataNavigator, Group]] = None,
    ) -> None:
        self._columns: List[Column] = []

        if isinstance(group, Group):
            self._data = DataNavigator(group)
        else:
            self._data = group or DataNavigator()

        self._grouped_set: Optional[Columns] = None

    def __str__(self) -> str:
        return "%s(%s)" % (self.__class__.__name__, self._data)

    @property
    def data(self) -> DataNavigator:
        return self._data

    def add(
        self,
        name: str,
        source: Optional[Union[Source, str]] = None,
    ) -> None:
        """
        Adds a column.

        `source` describes the data source for the column, which can be:

        - an explicit :class:`Source`
        - a string that describes the :code:`.`-separated path to the value
        - `None` if this set's record is an iterable list of primitives

        .. testcode::

            from rolumns import Columns, Source

            data = [
                {
                    "name": "Robert Pringles",
                    "email": "bob@pringles.pop",
                    "awards": [
                        "Fastest Doughnut Run",
                        "Tie of the Year",
                    ],
                },
            ]

            columns = Columns()
            columns.add("Name", "name")
            columns.add("Email", Source("email"))

            awards = columns.group("awards")
            # "awards" is also a column set
            awards.add("Awards")
        """

        source = source if isinstance(source, Source) else Source(source)
        column = Column(name, source)
        self._columns.append(column)

    def group(
        self,
        group: Union[DataNavigator, Group, str],
    ) -> "Columns":
        """
        Creates and adds a grouped column set.

        A column set cannot have multiple groups (though each group can have its
        own group). Will raise :class:`exceptions.MultipleGroups` if you try to
        add a second group.

        .. testcode::

            from rolumns import Columns, Source

            data = [
                {
                    "name": "Robert Pringles",
                    "awards": [
                        "Fastest Doughnut Run",
                        "Tie of the Year",
                    ],
                },
            ]

            columns = Columns()
            columns.add("Name", "name")

            awards = columns.group("awards")
            awards.add("Awards")
        """

        if self._grouped_set:
            raise MultipleGroups()

        if isinstance(group, str):
            group = ByPath(group)

        if isinstance(group, Group):
            group = self._data.subgroup(group)

        self._grouped_set = Columns(group)
        return self._grouped_set

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

    def normalize(self) -> List[Dict[str, Any]]:
        """
        Normalises `data` into a list of dictionaries describing column names
        and values.
        """

        logger.debug("%s normalising", self)

        result: List[Dict[str, Any]] = []

        for record in self.records():
            if is_debug():
                logger.debug("%s normalising record %s", self, dump(record))

            resolved: Dict[str, Any] = {}

            for column in self._columns:
                for index, value in enumerate(column.source.read(record)):
                    if index == 0:
                        resolved[column.name] = value
                    else:
                        raise Exception("Encountered multiple values")

            if self._grouped_set:
                key = self._grouped_set._data.group.name()
                resolved[key] = self._grouped_set.normalize()

            result.append(resolved)

        if is_debug():
            logger.debug("%s normalised columns to %s", self, dump(result))

        return result

    @staticmethod
    def normalized_to_column_values(
        normalized: List[Dict[str, Any]],
    ) -> Dict[str, List[Any]]:
        """
        Translates the normalised list of values `normalized` to a dictionary of
        column names and values.
        """

        filled_columns: Dict[str, List[Any]] = {}
        filled_columns_height = 0

        for record in normalized:
            # logger.info("record = %s", record)
            inner_columns: Dict[str, List[Any]] = {}
            inner_height = 1

            group: Optional[Tuple[str, List[Any]]] = None

            for key, value in record.items():
                if isinstance(value, list):
                    if group:
                        raise Exception("Encountered multiple groups")
                    group = (key, value)
                else:
                    inner_columns[key] = [value]

            if group:
                group_values = Columns.normalized_to_column_values(group[1])

                for key, value in group_values.items():
                    if inner_height > 1 and inner_height != len(value):
                        # logger.warning("inner_height = %i, value = %s (%i)"
                        # , inner_height, value, len(value),)
                        raise Exception
                    inner_height = max(inner_height, len(value))
                    inner_columns[key] = value

                for key, value in inner_columns.items():
                    while len(value) < inner_height:
                        value.append(value[0])

            for key, value in inner_columns.items():
                if key not in filled_columns:
                    filled_columns[key] = [None] * filled_columns_height
                filled_columns[key].extend(value)

            filled_columns_height += inner_height
            # logger.info("inner_height = %i, filled_columns_height = %i", inner
            # _height, filled_columns_height)

        return filled_columns

    def records(self) -> Iterable[Any]:
        """
        Gets an iterable list of the records of `data` described by this column
        set's grouping.
        """

        for record in self._data:
            if is_debug():
                logger.debug("%s discovered child record %s", self, dump(record))

            if isinstance(record, list):
                for d in record:
                    yield d
            else:
                yield record

    def to_column_values(self) -> Dict[str, List[Any]]:
        """
        Translates `data` to a dictionary of column names and values.
        """

        normalized = self.normalize()
        return Columns.normalized_to_column_values(normalized)
