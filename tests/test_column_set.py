from rolumns.column import Column
from rolumns.column_set import ColumnSet
from rolumns.column_source import ColumnSource
from tests.data import load_test_case


def test_array() -> None:
    (inp, exp) = load_test_case(1)
    cs = ColumnSet()
    cs.append(Column("Name", ColumnSource("name")))
    cs.append(Column("Favourite Colour", ColumnSource("favourite_colour")))
    actual = cs.rows(inp)
    assert actual == exp


def test_single() -> None:
    (inp, exp) = load_test_case(0)
    cs = ColumnSet()
    cs.append(Column("Name", ColumnSource("name")))
    cs.append(Column("Favourite Colour", ColumnSource("favourite_colour")))
    actual = cs.rows(inp)
    assert actual == exp


def test_sub() -> None:
    (inp, exp) = load_test_case(2)
    cs = ColumnSet()
    cs.append(Column("Name", ColumnSource("name")))
    cs.append(Column("Favourite Colour", ColumnSource("favourite_colour")))
    cs.append(Column("Address", ColumnSource("address.planet")))
    actual = cs.rows(inp)
    assert actual == exp


def test_repeating_sub() -> None:
    (inp, exp) = load_test_case(3)
    cs = ColumnSet()
    cs.append(Column("Name", ColumnSource("name")))
    cs.append(Column("Favourite Colour", ColumnSource("favourite_colour")))
    addresses = ColumnSet("addresses")
    addresses.append(Column("Address", ColumnSource("planet")))
    cs.append(addresses)
    assert cs.rows(inp) == exp
