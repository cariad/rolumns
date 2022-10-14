from typing import Any, Iterable, Optional

from rolumns.data_resolver import DataResolver
from rolumns.exceptions import TranslationFailed
from rolumns.translators import TranslationState, Translator


class Source:
    """
    Describes how to read a value from an object.

    ## Example

    Given this object:

    ```json
    {
        "address": {
            "planet": "Pluto"
        },
        "favourite_colour": "orange",
        "name": "charlie"
    }
    ```

    - The path `name` describes "orange".
    - The path `address.planet` describes "Pluto".
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
        Gets the prescribed value of `record`.
        """

        for datum in DataResolver(record).resolve(self._path):
            if self._translator:
                state = TranslationState(value=datum)

                try:
                    datum = self._translator(state)
                except Exception as ex:
                    raise TranslationFailed(datum, str(ex))

            yield datum
