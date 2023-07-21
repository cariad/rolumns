from typing import Any, Iterable, Optional

from rolumns.cursor import Cursor
from rolumns.data_resolver import DataResolver
from rolumns.exceptions import TranslationFailed
from rolumns.translation_state import TranslationState
from rolumns.types import Translator


class Source:
    """
    Describes how to read a value from an object.

    :code:`path` describes the path to the value. For example, given this object:

    .. code:: json

        {
            "name": "Robert Pringles",
            "address": {
                "planet": "Pluto"
            }
        }

    - The path :code:`"name"` returns `Robert Pringles`
    - The path :code:`"address.planet"` returns `Pluto`

    And given this list of primitives:

    .. code:: json

        [
            2022,
            2023,
            2024
        ]

    - The path :code:`None` iterates over the values

    :code:`constant` describes any static constant to bind to.

    :code:`cursor` describes any cursor to bind to.
    """

    def __init__(
        self,
        constant: Optional[Any] = None,
        cursor: Optional[Cursor] = None,
        path: Optional[str] = None,
        translator: Optional[Translator] = None,
    ) -> None:
        self._constant = constant
        self._cursor = cursor
        self._path = path
        self._translator = translator

    def read(self, record: Any) -> Iterable[Any]:
        """
        Yields each prescribed value of :code:`record`.
        """

        if self._constant is not None:
            yield self._constant
            return

        if self._cursor is not None:
            record = self._cursor.current

        for datum in DataResolver(record).resolve(self._path):
            if self._translator:
                state = TranslationState(
                    path=self._path,
                    record=record,
                    value=datum,
                )

                try:
                    datum = self._translator(state)
                except Exception as ex:
                    raise TranslationFailed(datum, str(ex))

            yield datum
