from typing import Any, Dict, Iterable, List


class PopulatedColumns:
    """
    A collection of columns and their values.
    """

    def __init__(self) -> None:
        self._columns: Dict[str, List[Any]] = {}

    def append(self, column: str, values: Iterable[Any]) -> None:
        """
        Appends the values `values` to the column named `column`.
        """

        if column not in self._columns:
            self._columns[column] = []

        self._columns[column].extend(values)

    def extend(self, values: "PopulatedColumns") -> None:
        """
        Extends this collection from another.
        """

        for key in values._columns:
            if key not in self._columns:
                self._columns[key] = []
            self._columns[key].extend(values._columns[key])

    def fill_gaps(self) -> None:
        """
        Fills any gaps in the values caused by adding grouped data.
        """

        count = self.height()

        for c in self._columns:
            while len(self._columns[c]) < count:
                self._columns[c].append(self._columns[c][0])

    def get(self, column: str, row: int) -> Any:
        """
        Gets the value of row `row` of column `column`.
        """

        return self._columns[column][row]

    def height(self) -> int:
        """
        Gets the maximum length of all columns.
        """

        count = 1

        for c in self._columns:
            count = max(len(self._columns[c]), count)

        return count
