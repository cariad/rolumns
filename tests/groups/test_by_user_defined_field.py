from pytest import raises

from rolumns.exceptions import UserDefinedFieldResolvedToMultipleValues
from rolumns.groups import ByUserDefinedFields, UserDefinedField


def test() -> None:
    group = ByUserDefinedFields(UserDefinedField("Colour", "colour"))

    expect = [
        {
            "name": "Colour",
            "value": "neon",
        }
    ]

    assert list(group.resolve({"colour": "neon"})) == expect


def test_no_value() -> None:
    group = ByUserDefinedFields(UserDefinedField("Colour", "colour"))

    expect = [
        {
            "name": "Colour",
            "value": None,
        },
    ]

    assert list(group.resolve({})) == expect


def test_multiple() -> None:
    group = ByUserDefinedFields(UserDefinedField("Colour", "colour"))

    with raises(UserDefinedFieldResolvedToMultipleValues) as ex:
        list(group.resolve([{"colour": "magenta"}, {"colour": "neon"}]))

    expect = (
        'The user-defined field "Colour" resolved to multiple values '
        + "(['magenta', 'neon']) when only one was expected"
    )
    assert str(ex.value) == expect
