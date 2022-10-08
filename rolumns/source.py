from typing import Any, Iterable, Optional

from rolumns.data_resolver import DataResolver
from rolumns.translators import Translator


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
        path: str,
        trans: Optional[Translator[Any]] = None,
    ) -> None:
        self._path = path
        self._translator = trans

    def read(self, record: Any) -> Iterable[Any]:
        """
        Gets the prescribed value of `record`.
        """

        for datum in DataResolver(record).resolve(self._path):
            if self._translator:
                datum = self._translator.translate(datum)
            yield datum
