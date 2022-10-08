from typing import Any, Iterable

from rolumns.data_resolver import DataResolver


class ColumnSource:
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

    def __init__(self, path: str) -> None:
        self.path = path

    def read(self, record: Any) -> Iterable[Any]:
        """
        Gets the prescribed value of `record`.
        """

        for datum in DataResolver(record).resolve(self.path):
            yield datum
