from typing import Any


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

    def read(self, record: Any) -> Any:
        """
        Gets the prescribed value of `record`.
        """

        parts = self.path.split(".")
        value = record
        for part in parts:
            value = value[part]
        return value
