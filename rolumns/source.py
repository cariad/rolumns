from typing import Any, Iterable, Optional

from rolumns.data_resolver import DataResolver
from rolumns.exceptions import TranslationFailed
from rolumns.translators import TranslationState, Translator


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
    """

    def __init__(
        self,
        path: Optional[str],
        translator: Optional[Translator] = None,
    ) -> None:
        self._path = path
        self._translator = translator

    def read(self, record: Any) -> Iterable[Any]:
        """
        Yields each prescribed value of :code:`record`.
        """

        for datum in DataResolver(record).resolve(self._path):
            if self._translator:
                state = TranslationState(value=datum)

                try:
                    datum = self._translator(state)
                except Exception as ex:
                    raise TranslationFailed(datum, str(ex))

            yield datum
