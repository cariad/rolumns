from typing import Any, Iterable, Optional

from rolumns.data_resolver import DataResolver
from rolumns.groups.group import Group


class ByPath(Group):
    def __init__(self, path: Optional[str] = None) -> None:
        self._path = path

    def __str__(self) -> str:
        return f'ByPath("{self._path or ""}")'

    def name(self) -> str:
        return self._path or ""

    def resolve(self, data: Any) -> Iterable[Any]:
        for datum in DataResolver(data).resolve(self._path):
            yield datum
