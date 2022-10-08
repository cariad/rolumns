from typing import Any, List


class UserDefinedFieldResolvedToMultipleValues(Exception):
    """
    Raised when a user-defined field resolves to multiple values.
    """

    def __init__(self, name: str, values: List[Any]) -> None:
        msg = (
            f'The user-defined field "{name}" resolved to multiple values '
            + f"({values}) when only one was expected"
        )

        super().__init__(msg)
