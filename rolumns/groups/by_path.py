from typing import Any, Iterable, Optional

from rolumns.data_resolver import DataResolver
from rolumns.groups.group import Group


class ByPath(Group):
    def __init__(self, path: Optional[str] = None) -> None:
        self._path = path

    def resolve(self, data: Any) -> Iterable[Any]:
        for datum in DataResolver(data).resolve(self._path):
            yield datum
