from dateutil import parser

from rolumns.columns import Columns
from rolumns.groups import ByUserDefinedFields, UserDefinedField
from rolumns.renderers.rows import RowsRenderer
from rolumns.source import Source
from rolumns.translators import to_datetime
from tests.data import load_test_case

# Fiddly cases:


def test_empty() -> None:
    (inp, exp) = load_test_case(0)
    cs = Columns()
    cs.add("Name", "name")
    cs.add("Favourite Colour", "favourite_colour")
    assert list(RowsRenderer(cs).render(inp)) == exp


def test_append() -> None:
    (inp, exp) = load_test_case(0)
    cs = Columns()
    cs.add("Name", "name")
    cs.add("Favourite Colour", "favourite_colour")
    t = RowsRenderer(cs)
    t.append("Name")
    t.append("Favourite Colour")
    assert list(t.render(inp)) == exp


def test_only_one() -> None:
    (inp, exp) = load_test_case(0, expect_variant="only-name")
    cs = Columns()
    cs.add("Name", "name")
    cs.add("Favourite Colour", "favourite_colour")
    assert list(RowsRenderer(cs, ["Name"]).render(inp)) == exp


def test_reversed() -> None:
    (inp, exp) = load_test_case(0, expect_variant="reversed")
    cs = Columns()
    cs.add("Name", "name")
    cs.add("Favourite Colour", "favourite_colour")
    assert list(RowsRenderer(cs, ["Favourite Colour", "Name"]).render(inp)) == exp


# Test suites:


def test_array() -> None:
    (inp, exp) = load_test_case(1)

    cs = Columns()
    cs.add("Name", "name")
    cs.add("Favourite Colour", "favourite_colour")
    assert list(RowsRenderer(cs).render(inp)) == exp


def test_sub() -> None:
    (inp, exp) = load_test_case(2)
    cs = Columns()
    cs.add("Name", "name")
    cs.add("Favourite Colour", "favourite_colour")
    cs.add("Address", "address.planet")
    assert list(RowsRenderer(cs).render(inp)) == exp


def test_repeating_sub() -> None:
    (inp, exp) = load_test_case(3)
    cs = Columns()
    cs.add("Name", "name")
    cs.add("Favourite Colour", "favourite_colour")
    addresses = cs.add_group("addresses")
    addresses.add("Address", "planet")

    assert list(RowsRenderer(cs).render(inp)) == exp


def test_find() -> None:
    (inp, exp) = load_test_case(4)
    cs = Columns()
    cs.add("Name", "name")
    cs.add("Current Address", "addresses.current.planet")

    assert list(RowsRenderer(cs).render(inp)) == exp


def test_find_and_group() -> None:
    (inp, exp) = load_test_case(5)
    cs = Columns()
    cs.add("Name", "name")
    colours = cs.add_group("favourites.colours")
    colours.add("Favourite Colours", "value")
    assert list(RowsRenderer(cs).render(inp)) == exp


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

    cs = Columns()
    cs.add("Name", "name")
    cs.add("Date of Birth", Source("date_of_birth", translator=to_datetime))

    assert list(RowsRenderer(cs).render(inp)) == exp


def test_udf_lookup() -> None:
    (inp, exp) = load_test_case(6)
    cs = Columns()
    cs.add("Name", "name")

    udfs = cs.add_group(
        ByUserDefinedFields(
            UserDefinedField("Favourite colour", "favourite_colour"),
            UserDefinedField("Planet", "planet"),
            UserDefinedField("Smell", "smell"),
        )
    )

    udfs.add("UDF Name", "name")
    udfs.add("UDF Value", "value")
    assert list(RowsRenderer(cs).render(inp)) == exp


def test_primitive_list() -> None:
    (inp, exp) = load_test_case(7)
    cs = Columns()
    cs.add("Name", "name")

    things = cs.add_group("favourite_things")
    things.add("Favourite Things")
    assert list(RowsRenderer(cs).render(inp)) == exp
