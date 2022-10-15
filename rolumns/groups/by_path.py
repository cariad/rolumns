from typing import Any, Iterable, Optional

from rolumns.data_resolver import DataResolver
from rolumns.groups.group import Group


class ByPath(Group):
    """
    Groups rows by a list of records. :code:`path` describes the path to the
    list in the input record.
    """

    def __init__(self, path: Optional[str] = None) -> None:
        self._path = path

    def __str__(self) -> str:
        return f'ByPath("{self._path or ""}")'

    def name(self) -> str:
        """
        Gets the name of this group unique to its parent column set.
        """

        return self._path or ""

    def resolve(self, data: Any) -> Iterable[Any]:
        """
        Resolves :code:`data` to an iterable list of records.
        """

        for datum in DataResolver(data).resolve(self._path):
            yield datum
