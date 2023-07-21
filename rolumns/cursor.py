from __future__ import annotations

from typing import Any, Iterator, Optional, Union, cast

from rolumns.by_path import ByPath
from rolumns.group import Group


class Cursor:
    """
    A read-only cursor over iterable records.

    :code:`group` describes how records should be resolved. Pass a string to
    imply a :class:`ByPath` grouping.

    :code:`parent` describes this cursor's parent, if any.
    """

    def __init__(
        self,
        group: Optional[Union[Group, str]] = None,
        parent: Optional[Cursor] = None,
    ) -> None:
        if isinstance(group, str) or group is None:
            group = ByPath(group)

        self._data: Optional[Any] = None
        self._group = group or ByPath()
        self._parent = parent
        self._resolved: Optional[Iterator[Any]] = None
        self._current: Optional[Any] = None

    def __iter__(self) -> Any:
        return self

    def __next__(self) -> Any:
        resolved = self._make_resolved()
        self._current = next(resolved)

        if isinstance(self._current, list):
            current_list = cast(Iterator[Any], self._current)
            self._resolved = iter(current_list)
            self._current = next(self._resolved)

        return self.current

    def __str__(self) -> str:
        return "%s(%s)" % (
            self.__class__.__name__,
            self._group,
        )

    def _make_resolved(self) -> Iterator[Any]:
        force_update = False

        if self._parent is None and self._data is None:
            raise ValueError("%s has no parent and no data" % self)

        if self._parent and self._data is not self._parent.current:
            self._data = self._parent.current
            self._index = -1
            force_update = True

        if self._resolved is None or force_update:
            self._resolved = iter(self._group.resolve(self._data))

        return self._resolved

    @property
    def current(self) -> Any:
        """
        Current record.
        """

        return self._current

    @property
    def cursor_group(self) -> Group:
        return self._group

    def group(
        self,
        group: Union[Group, str],
    ) -> Cursor:
        """
        Creates and returns a child cursor.

        :code:`group` describes how records should be resolved. Pass a string to
        imply a :class:`ByPath` grouping.
        """

        if isinstance(group, str):
            group = ByPath(group)

        return Cursor(
            group,
            parent=self,
        )

    def load(
        self,
        data: Any,
    ) -> None:
        """
        Loads :code:`data` into the cursor.
        """

        self._data = data
