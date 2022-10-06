from rolumns.column import Column
from rolumns.column_set import ColumnSet
from rolumns.column_source import ColumnSource
from tests.data import load_test_case


def test_array() -> None:
    (inp, exp) = load_test_case(1)
    cs = ColumnSet()
    cs.append(Column[str]("Name", ColumnSource[str]("name")))
    cs.append(Column[str]("Favourite Colour", ColumnSource[str]("favourite_colour")))
    actual = cs.rows(inp)
    assert actual == exp


def test_single() -> None:
    (inp, exp) = load_test_case(0)
    cs = ColumnSet()
    cs.append(Column[str]("Name", ColumnSource[str]("name")))
    cs.append(Column[str]("Favourite Colour", ColumnSource[str]("favourite_colour")))
    actual = cs.rows(inp)
    assert actual == exp
