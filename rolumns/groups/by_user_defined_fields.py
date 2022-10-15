from typing import Any, Iterable, List, Union

from rolumns.exceptions import UserDefinedFieldResolvedToMultipleValues
from rolumns.groups.group import Group
from rolumns.source import Source


class UserDefinedField:
    """
    A user-defined field.
    """

    def __init__(self, name: str, source: Union[Source, str]) -> None:
        self.name = name
        self.source = source if isinstance(source, Source) else Source(source)


class ByUserDefinedFields(Group):
    """
    Groups rows by a list of user-defined fields. :code:`fields` describes the
    fields to resolve.
    """

    NAME = "name"
    """
    Path to the field name.
    """

    VALUE = "value"
    """
    Path to the field value.
    """

    def __init__(self, *fields: UserDefinedField) -> None:
        self._fields: List[UserDefinedField] = [u for u in fields]

    def append(self, name: str, source: Union[Source, str]) -> None:
        self._fields.append(UserDefinedField(name, source))

    def name(self) -> str:
        return "__user_defined_fields__"

    def resolve(self, data: Any) -> Iterable[Any]:
        """
        Resolves :code:`data` to an iterable list of records.

        The field name will be recorded at the
        :py:attr:`ByUserDefinedFields.NAME` path and the value at
        :py:attr:`ByUserDefinedFields.VALUE`.
        """

        for field in self._fields:
            first_value = None

            for index, value in enumerate(field.source.read(data)):
                if index > 0:
                    raise UserDefinedFieldResolvedToMultipleValues(
                        field.name,
                        [first_value, value],
                    )
                first_value = value

            yield {
                self.NAME: field.name,
                self.VALUE: first_value,
            }
