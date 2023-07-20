from __future__ import annotations

from logging import DEBUG
from typing import Any, Iterator, Optional, Union

from rolumns.by_path import ByPath
from rolumns.group import Group
from rolumns.logging import dump, is_debug, logger


class DataNavigator:
    def __init__(
        self,
        group: Optional[Group] = None,
        parent: Optional[DataNavigator] = None,
    ) -> None:
        self._data: Optional[Any] = None
        self._group = group or ByPath()
        self._parent = parent
        self._resolved: Optional[Iterator[Any]] = None
        self._current: Optional[Any] = None

    def __iter__(self) -> Any:
        return self

    def __str__(self) -> str:
        return "%s(%s)" % (
            self.__class__.__name__,
            self._group,
        )

    def __next__(self) -> Any:
        logger.debug("%s moving to next record", self)
        self._make_resolved()

        if self._resolved is None:
            raise ValueError()

        try:
            self._current = next(self._resolved)
            logger.debug(
                "%s current is %s (%s)", self, self._current, type(self._current)
            )
            assert isinstance(self._current, dict)
        except StopIteration:
            logger.debug("%s exhausted", self)
            raise

        return self.current

    @property
    def group(self) -> Group:
        return self._group

    def subgroup(
        self,
        group: Union[Group, str],
    ) -> DataNavigator:
        if isinstance(group, str):
            group = ByPath(group)

        return DataNavigator(
            group,
            parent=self,
        )

    def _make_resolved(self) -> None:
        force_update = False

        if self._parent is None and self._data is None:
            raise ValueError("no parent and no data")

        if self._parent and self._data is not self._parent.current:
            logger.debug(
                "%s parent record changed: %s",
                self,
                dump(self._parent.current),
            )

            self._data = self._parent.current
            self._index = -1
            force_update = True

        if self._resolved is None or force_update:
            self._resolved = iter(self._group.resolve(self._data))
            # if logger.getEffectiveLevel() == DEBUG:
            #     logger.debug(
            #         "%s resolved to: %s",
            #         self,
            #         dump(self._resolved),
            #     )

    @property
    def current(self) -> Any:
        # self._make_resolved()
        # if self._resolved is None:
        #     raise ValueError()

        if is_debug():
            logger.debug(
                "%s yielding current: %s",
                self,
                dump(self._current),
            )

        return self._current

    def one(self) -> Any:
        self._make_resolved()
        if self._resolved is None:
            raise ValueError()

        result: Optional[Any] = None

        for index, value in enumerate(self._resolved):
            if index == 0:
                result = value
            else:
                raise ValueError("%s expected %s to be one", self, dump(self._resolved))

        if logger.getEffectiveLevel() == DEBUG:
            logger.debug(
                "%s yielding one: %s",
                self,
                dump(result),
            )

        return result

    def load(self, data: Any) -> None:
        self._data = data
