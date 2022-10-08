from pytest import raises

from rolumns.column_set import ColumnSet
from rolumns.exceptions import MultipleRepeaters


def test_create_repeater__multiple() -> None:
    cs = ColumnSet()
    cs.add_grouped_set("")

    with raises(MultipleRepeaters) as ex:
        cs.add_grouped_set("")

    expect = "A column set cannot have multiple repeaters as direct children"
    assert str(ex.value) == expect
