from pytest import raises

from rolumns.column_set import ColumnSet
from rolumns.exceptions import MultipleRepeaters


def test_create_repeater__multiple() -> None:
    cs = ColumnSet()
    cs.create_repeater("")

    with raises(MultipleRepeaters) as ex:
        cs.create_repeater("")

    expect = "A column set cannot have multiple repeaters as direct children"
    assert str(ex.value) == expect
