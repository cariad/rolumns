from typing import Any, Iterable, List


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

        parts = self.path.split(".")
        parts.reverse()

        for r in self._read(parts.copy(), record):
            yield r

    def _read(self, parts: List[str], data: Any) -> Iterable[Any]:
        if isinstance(data, list):
            for d in data:
                for r in self._read(parts.copy(), d):
                    yield r
            return

        part = parts.pop()
        data = data[part]

        if not parts:
            # This is the leaf, so there better be something to read!
            yield data
            return

        for r in self._read(parts.copy(), data):
            yield r
