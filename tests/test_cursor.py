from typing import Union

from pytest import mark

from rolumns import ByPath, Cursor, Group


@mark.parametrize(
    "group",
    [
        "value",
        ByPath("value"),
    ],
)
def test_by_path(group: Union[Group, str]) -> None:
    cursor = Cursor(group)

    cursor.load(
        [
            {"value": "one"},
            {"value": "two"},
            {"value": "three"},
        ]
    )

    assert list(cursor) == [
        "one",
        "two",
        "three",
    ]


def test_group() -> None:
    parent = Cursor("group")
    child = parent.group("value")

    assert child.cursor_group == ByPath("value")


def test_list() -> None:
    cursor = Cursor("value")

    cursor.load(
        {
            "value": [
                "one",
                "two",
                "three",
            ],
        },
    )

    assert list(cursor) == [
        "one",
        "two",
        "three",
    ]


def test_str() -> None:
    assert str(Cursor("value")) == 'Cursor(ByPath("value"))'
