from typing import Any, Iterable, Union

from rolumns.exceptions import UserDefinedFieldResolvedToMultipleValues
from rolumns.groups.group import Group
from rolumns.source import Source


class UserDefinedField:
    def __init__(self, name: str, source: Union[Source, str]) -> None:
        self.name = name
        self.source = source if isinstance(source, Source) else Source(source)


class ByUserDefinedFields(Group):
    def __init__(self, *fields: UserDefinedField) -> None:
        self._fields = fields

    def resolve(self, data: Any) -> Iterable[Any]:
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
                "name": field.name,
                "value": first_value,
            }
