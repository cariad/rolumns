from typing import Any, Dict, Iterable

from typing_extensions import TypedDict

from rolumns.groups.group import Group


class ByValue(Group):
    def name(self) -> str:
        return "__by_value__"

    def resolve(self, data: "KeyValuePair") -> Iterable[Any]:
        """
        Resolves the value of :code:`data` to an iterable list of records.
        """

        value = data["value"]

        if isinstance(value, list):
            for datum in value:
                yield datum
        else:
            yield value


class KeyValuePair(TypedDict):
    key: str
    value: Any


class ByKey(Group):
    """
    Groups rows by each key in a dictionary.

    .. testcode::

        from rolumns import Columns
        from rolumns.groups import ByKey
        from rolumns.renderers import RowsRenderer

        data = {
            "today": {
                "event": "Bought sausages",
            },
            "yesterday": {
                "event": "Bought a train set",
            },
        }

        columns = Columns(ByKey())
        columns.add("When", ByKey.key())
        columns.add("Event", ByKey.value("event"))

        print(list(RowsRenderer(columns).render(data)))

    .. testoutput::
        :options: +NORMALIZE_WHITESPACE

        [['When',      'Event'],
         ['today',     'Bought sausages'],
         ['yesterday', 'Bought a train set']]

    .. testcode::

        from rolumns import Columns
        from rolumns.groups import ByKey
        from rolumns.renderers import RowsRenderer

        data = {
            "today": [
                {"event": "Bought sausages"},
                {"event": "Bought bread"},
            ],
            "yesterday": [
                {"event": "Bought a train set"},
                {"event": "Bought a book"},
            ],
        }

        columns = Columns(ByKey())
        columns.add("When", ByKey.key())

        values = columns.group(ByKey.values())
        values.add("Event", "event")

        print(list(RowsRenderer(columns).render(data)))

    .. testoutput::
        :options: +NORMALIZE_WHITESPACE

        [['When',      'Event'],
         ['today',     'Bought sausages'],
         ['today',     'Bought bread'],
         ['yesterday', 'Bought a train set'],
         ['yesterday', 'Bought a book']]
    """

    @classmethod
    def key(cls) -> str:
        """
        Gets the path to the key name.
        """

        return "key"

    def name(self) -> str:
        return "__by_key__"

    def resolve(self, data: Dict[Any, Any]) -> Iterable[KeyValuePair]:
        """
        Resolves :code:`data` to an iterable list of :class:`KeyValuePair`.
        """

        for key, value in data.items():
            yield KeyValuePair(key=key, value=value)

    @classmethod
    def value(cls, path: str) -> str:
        """
        Gets the path to a value within each dictionary key's value.

        Use this if each key's value is a flat object. If the value is iterable
        then use :func:`ByKey.values` to get a group instead.

        .. testcode::

            from rolumns import Columns
            from rolumns.groups import ByKey
            from rolumns.renderers import RowsRenderer

            data = {
                "today": {
                    "event": "Bought sausages",
                },
                "yesterday": {
                    "event": "Bought a train set",
                },
            }

            columns = Columns(ByKey())
            columns.add("When", ByKey.key())
            columns.add("Event", ByKey.value("event"))

            print(list(RowsRenderer(columns).render(data)))

        .. testoutput::
            :options: +NORMALIZE_WHITESPACE

            [['When',      'Event'],
             ['today',     'Bought sausages'],
             ['yesterday', 'Bought a train set']]
        """

        return f"value.{path}"

    @classmethod
    def values(cls) -> ByValue:
        """
        Gets a grouper for each dictionary key's values.

        Use this if each key's value is iterable. If the value is a flat object
        then use :func:`ByKey.value` to describe a path instead.

        .. testcode::

            from rolumns import Columns
            from rolumns.groups import ByKey
            from rolumns.renderers import RowsRenderer

            data = {
                "today": [
                    {"event": "Bought sausages"},
                    {"event": "Bought bread"},
                ],
                "yesterday": [
                    {"event": "Bought a train set"},
                    {"event": "Bought a book"},
                ],
            }

            columns = Columns(ByKey())
            columns.add("When", ByKey.key())

            values = columns.group(ByKey.values())
            values.add("Event", "event")

            print(list(RowsRenderer(columns).render(data)))

        .. testoutput::
            :options: +NORMALIZE_WHITESPACE

            [['When',      'Event'],
             ['today',     'Bought sausages'],
             ['today',     'Bought bread'],
             ['yesterday', 'Bought a train set'],
             ['yesterday', 'Bought a book']]
        """

        return ByValue()
