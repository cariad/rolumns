from abc import ABC, abstractmethod
from typing import Any, Iterable


class Group(ABC):
    @abstractmethod
    def name(self) -> str:
        """
        Gets the name of this group unique to its parent column set.
        """

    @abstractmethod
    def resolve(self, data: Any) -> Iterable[Any]:
        """ """
