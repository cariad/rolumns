from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from rolumns.exceptions import TranslationFailed

TValue = TypeVar("TValue")


class Translator(ABC, Generic[TValue]):
    def translate(self, value: Any) -> TValue:
        try:
            return self.try_translate(value)
        except Exception as ex:
            raise TranslationFailed(value, str(ex))

    @abstractmethod
    def try_translate(self, value: Any) -> TValue:
        """
        Attempts to translate `value` to `TValue`.

        Raises any exception to indicate failure.
        """
