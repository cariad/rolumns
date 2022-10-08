from dateutil import parser

from rolumns.column_set import ColumnSet
from rolumns.source import Source
from rolumns.table import Table
from rolumns.translators import ToDateTime
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


def test_find() -> None:
    (inp, exp) = load_test_case(4)
    cs = ColumnSet()
    cs.add("Name", "name")
    cs.add("Current Address", "addresses.current.planet")

    assert list(Table(cs).rows(inp)) == exp


def test_find_and_group() -> None:
    (inp, exp) = load_test_case(5)
    cs = ColumnSet()
    cs.add("Name", "name")
    colours = cs.create_repeater("favourites.colours")
    colours.add("Favourite Colours", "value")
    assert list(Table(cs).rows(inp)) == exp


def test_dates() -> None:
    inp = [
        {"date_of_birth": "19920307T131415Z", "name": "alice"},
        {"date_of_birth": "19930207T161718Z", "name": "bob"},
        {"date_of_birth": "19940107T192021Z", "name": "charlie"},
    ]

    exp = [
        ["Name", "Date of Birth"],
        ["alice", parser.isoparse("1992-03-07T13:14:15Z")],
        ["bob", parser.isoparse("1993-02-07T16:17:18Z")],
        ["charlie", parser.isoparse("1994-01-07T19:20:21Z")],
    ]

    cs = ColumnSet()
    cs.add("Name", "name")
    cs.add("Date of Birth", Source("date_of_birth", trans=ToDateTime()))

    assert list(Table(cs).rows(inp)) == exp
