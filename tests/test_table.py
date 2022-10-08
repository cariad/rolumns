from rolumns.column_set import ColumnSet
from rolumns.table import Table
from tests.data import load_test_case

# Fiddly cases:


def test_empty() -> None:
    (inp, exp) = load_test_case(0)
    cs = ColumnSet()
    cs.add("Name", "name")
    cs.add("Favourite Colour", "favourite_colour")
    assert list(Table(cs).rows(inp)) == exp


def test_append() -> None:
    (inp, exp) = load_test_case(0)
    cs = ColumnSet()
    cs.add("Name", "name")
    cs.add("Favourite Colour", "favourite_colour")
    t = Table(cs)
    t.append("Name")
    t.append("Favourite Colour")
    assert list(t.rows(inp)) == exp


def test_only_one() -> None:
    (inp, exp) = load_test_case(0, expect_variant="only-name")
    cs = ColumnSet()
    cs.add("Name", "name")
    cs.add("Favourite Colour", "favourite_colour")
    assert list(Table(cs, ["Name"]).rows(inp)) == exp


def test_reversed() -> None:
    (inp, exp) = load_test_case(0, expect_variant="reversed")
    cs = ColumnSet()
    cs.add("Name", "name")
    cs.add("Favourite Colour", "favourite_colour")
    assert list(Table(cs, ["Favourite Colour", "Name"]).rows(inp)) == exp


# Test suites:


def test_array() -> None:
    (inp, exp) = load_test_case(1)

    cs = ColumnSet()
    cs.add("Name", "name")
    cs.add("Favourite Colour", "favourite_colour")
    assert list(Table(cs).rows(inp)) == exp


def test_sub() -> None:
    (inp, exp) = load_test_case(2)
    cs = ColumnSet()
    cs.add("Name", "name")
    cs.add("Favourite Colour", "favourite_colour")
    cs.add("Address", "address.planet")
    assert list(Table(cs).rows(inp)) == exp


def test_repeating_sub() -> None:
    (inp, exp) = load_test_case(3)
    cs = ColumnSet()
    cs.add("Name", "name")
    cs.add("Favourite Colour", "favourite_colour")
    addresses = cs.create_repeater("addresses")
    addresses.add("Address", "planet")

    assert list(Table(cs).rows(inp)) == exp
