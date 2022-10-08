from abc import ABC, abstractmethod
from typing import Any, Iterable


class Group(ABC):
    @abstractmethod
    def resolve(self, data: Any) -> Iterable[Any]:
        """ """
