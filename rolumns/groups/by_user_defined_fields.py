from typing import Any, Iterable, List, Union

from rolumns.data_navigator import DataNavigator
from rolumns.exceptions import UserDefinedFieldResolvedToMultipleValues
from rolumns.group import Group

# from rolumns.logging import logger
from rolumns.source import Source


class UserDefinedField:
    """
    A user-defined field.
    """

    def __init__(
        self,
        name: str,
        source: Union[DataNavigator, Source, str],
    ) -> None:
        self.name = name

        if isinstance(source, str):
            self.source: Union[DataNavigator, Source] = Source(source)
        else:
            self.source = source

    def __str__(self) -> str:
        return self.name


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

    def __str__(self) -> str:
        return "%s(%i fields)" % (self.__class__.__name__, len(self._fields))

    def __init__(self, *fields: UserDefinedField) -> None:
        self._fields: List[UserDefinedField] = [u for u in fields]

    def append(self, name: str, source: DataNavigator) -> None:
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
            # logger.info('Resolving UDF "%s"', field)

            first_value = None

            source = field.source

            e = source.read(data) if isinstance(source, Source) else source.one()

            for index, value in enumerate(e):
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
