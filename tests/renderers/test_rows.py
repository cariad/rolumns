from rolumns import ByKey, Columns
from rolumns.groups import ByUserDefinedFields, UserDefinedField
from rolumns.renderers.rows import RowsRenderer
from tests.data import load_test_case

# Fiddly cases:


def test_empty() -> None:
    (inp, exp) = load_test_case(0)
    cs = Columns()
    cs.add("Name", "name")
    cs.add("Favourite Colour", "favourite_colour")
    cs.data.load(inp)
    assert list(RowsRenderer(cs).render()) == exp


# def test_append() -> None:
#     (inp, exp) = load_test_case(0)
#     cs = Columns()
#     cs.add("Name", "name")
#     cs.add("Favourite Colour", "favourite_colour")
#     t = RowsRenderer(cs)
#     t.append("Name")
#     t.append("Favourite Colour")
#     assert list(t.render(inp)) == exp


# def test_only_one() -> None:
#     (inp, exp) = load_test_case(0, expect_variant="only-name")
#     cs = Columns()
#     cs.add("Name", "name")
#     cs.add("Favourite Colour", "favourite_colour")
#     assert list(RowsRenderer(cs, ["Name"]).render(inp)) == exp


# def test_reversed() -> None:
#     (inp, exp) = load_test_case(0, expect_variant="reversed")
#     cs = Columns()
#     cs.add("Name", "name")
#     cs.add("Favourite Colour", "favourite_colour")
#     assert list(RowsRenderer(cs, ["Favourite Colour", "Name"]).render(inp)) == exp


# # Test suites:


def test_array() -> None:
    (inp, exp) = load_test_case(1)

    cs = Columns()
    cs.add("Name", "name")
    cs.add("Favourite Colour", "favourite_colour")

    cs.data.load(inp)

    assert list(RowsRenderer(cs).render()) == exp


# def test_sub() -> None:
#     (inp, exp) = load_test_case(2)
#     cs = Columns()
#     cs.add("Name", "name")
#     cs.add("Favourite Colour", "favourite_colour")
#     cs.add("Address", "address.planet")
#     assert list(RowsRenderer(cs).render(inp)) == exp


def test_sub__child_does_not_exist() -> None:
    (inp, exp) = load_test_case(2, expect_variant="missing")

    cs = Columns()
    cs.add("Name", "name")
    cs.add("Favourite Colour", "favourite_colour")

    # address.solar_system doesn't exist in the source data.
    cs.add("Address", "address.solar_system")

    cs.data.load(inp)

    assert list(RowsRenderer(cs).render()) == exp


# def test_repeating_sub() -> None:
#     (inp, exp) = load_test_case(3)
#     cs = Columns()
#     cs.add("Name", "name")
#     cs.add("Favourite Colour", "favourite_colour")
#     addresses = cs.group("addresses")
#     addresses.add("Address", "planet")

#     assert list(RowsRenderer(cs).render(inp)) == exp


# def test_find() -> None:
#     (inp, exp) = load_test_case(4)
#     cs = Columns()
#     cs.add("Name", "name")
#     cs.add("Current Address", "addresses.current.planet")

#     assert list(RowsRenderer(cs).render(inp)) == exp


# def test_find_and_group() -> None:
#     (inp, exp) = load_test_case(5)
#     cs = Columns()
#     cs.add("Name", "name")
#     colours = cs.group("favourites.colours")
#     colours.add("Favourite Colours", "value")

#     cs.data.load(inp)

#     assert list(RowsRenderer(cs).render()) == exp


# def test_translation() -> None:
#     inp = [
#         {"name": "alice"},
#         {"name": "bob"},
#         {"name": "charlie"},
#     ]

#     def to_upper(state: TranslationState) -> str:
#         return str(state.value).upper()

#     exp = [
#         ["Name"],
#         ["ALICE"],
#         ["BOB"],
#         ["CHARLIE"],
#     ]

#     cs = Columns()
#     cs.add("Name", Source("name", translator=to_upper))

#     assert list(RowsRenderer(cs).render(inp)) == exp


def test_udf_lookup() -> None:
    (inp, exp) = load_test_case(6)
    cs = Columns()
    cs.add("Name", "name")

    udfs = cs.group(
        ByUserDefinedFields(
            UserDefinedField("Favourite colour", "favourite_colour"),
            UserDefinedField("Planet", "planet"),
            UserDefinedField("Smell", "smell"),
        )
    )

    udfs.add("UDF Name", "name")
    udfs.add("UDF Value", "value")

    cs.data.load(inp)

    assert list(RowsRenderer(cs).render()) == exp


# def test_primitive_list() -> None:
#     (inp, exp) = load_test_case(7)
#     cs = Columns()
#     cs.add("Name", "name")

#     things = cs.group("favourite_things")
#     things.add("Favourite Things")

#     cs.data.load(inp)

#     assert list(RowsRenderer(cs).render()) == exp


# def test_dictionary() -> None:
#     (inp, exp) = load_test_case(8)
#     cs = Columns(ByKey())
#     cs.add("When", ByKey.key())
#     cs.add("Event", ByKey.value("event"))
#     assert list(RowsRenderer(cs).render(inp)) == exp


# def test_dictionary_object_list() -> None:
#     (inp, exp) = load_test_case(9)
#     cs = Columns(ByKey())
#     cs.add("When", ByKey.key())
#     events = cs.group(ByKey.values())
#     events.add("Event", "event")
#     assert list(RowsRenderer(cs).render(inp)) == exp


# def test_dictionary_string_list() -> None:
#     (inp, exp) = load_test_case(10)
#     cs = Columns(ByKey())
#     cs.add("When", ByKey.key())
#     events = cs.group(ByKey.values())
#     events.add("Event")
#     assert list(RowsRenderer(cs).render(inp)) == exp


# def test_dictionary_object_list_via_child() -> None:
#     (inp, exp) = load_test_case(11)
#     cs = Columns(ByKey("diary"))
#     cs.add("When", ByKey.key())
#     events = cs.group(ByKey.values())
#     events.add("Event", "event")
#     assert list(RowsRenderer(cs).render(inp)) == exp


# def test_dictionary_object_list_with_child_group() -> None:
#     (inp, exp) = load_test_case(12)

#     cs = Columns(ByKey())
#     cs.add("When", ByKey.key())

#     events = cs.group(ByKey.values())
#     events.add("Event", "event")

#     types = events.group(ByPath("types"))
#     types.add("Types", "name")

#     cs.data.load(inp)

#     assert list(RowsRenderer(cs).render()) == exp


def test_udf_from_repeating_group() -> None:
    (inp, exp) = load_test_case(13)

    cs = Columns(ByKey())
    cs.add("Boss", ByKey.value("static.boss_name.value"))

    fund_group = cs.group(ByKey.value("repeating.contact_details"))

    udfs = fund_group.group(
        ByUserDefinedFields(
            UserDefinedField("Fax", "fax.value"),
            UserDefinedField("VOIP", "voip.value"),
        )
    )

    udfs.add("Device", "name")
    udfs.add("Number", "value")

    cs.data.load(inp)

    assert list(RowsRenderer(cs).render()) == exp


# def test_foo() -> None:
#     (inp, exp) = load_test_case(13)

#     root_data = DataNavigator(ByKey())

#     cs = Columns(root_data)

#     group_data = root_data.subgroup(ByKey.value("groups.am:performance:fund"))

#     group_columns = cs.group(group_data)

#     group_columns.add("Portfolio Deal ID", "iqeq:portfolio_id.value")
#     group_columns.add("Deal Name", "am:fund:general:fund_name.value")

#     udfs = group_columns.group(
#         ByUserDefinedFields(
#             UserDefinedField(
#                 "Fund Manager",
#                 root_data.subgroup(
#                     ByKey.value("metrics.am:fund_manager:general:name.value"),
#                 ),
#             ),
#             UserDefinedField(
#                 "GP Name",
#                 root_data.subgroup(
#                     ByKey.value("metrics.am:gp:general:gp_name.value"),
#                 ),
#             ),
#             UserDefinedField(
#                 "Sector",
#                 Source("am:fund:general:sector.value"),
#                 # group_data.subgroup(ByKey.value("am:fund:general:sector.value")),
#             ),
#         ),
#     )

#     udfs.add("UDF Name", "name")
#     udfs.add("UDF Value", "value")

#     root_data.load(inp)

#     assert list(RowsRenderer(cs).render()) == exp


# def test_foo_group_udfs_only() -> None:
#     (inp, exp) = load_test_case(13)

#     root_data = DataNavigator(ByKey())

#     cs = Columns(root_data)

#     group_data = root_data.subgroup(ByKey.value("groups.am:performance:fund"))

#     group_columns = cs.group(group_data)

#     udfs = group_columns.group(
#         ByUserDefinedFields(
#             UserDefinedField("Sector", "am:fund:general:sector.value"),
#         ),
#     )

#     udfs.add("UDF Name", "name")
#     udfs.add("UDF Value", "value")

#     root_data.load(inp)

#     assert list(RowsRenderer(cs).render()) == exp


# def test_simple_udfs() -> None:
#     inp = {
#         "groups": [
#             {
#                 "favourite_colour": "green",
#                 "name": "alice",
#                 "planet": "Earth",
#                 "smell": "lavender",
#             },
#             {
#                 "favourite_colour": "magenta",
#                 "name": "bob",
#                 "planet": "Mars",
#                 "smell": "rose",
#             },
#             {
#                 "favourite_colour": "orange",
#                 "name": "charlie",
#                 "planet": "Pluto",
#                 "smell": "lynx",
#             },
#         ]
#     }

#     exp = [
#         ["Name", "UDF Name", "UDF Value"],
#         ["alice", "Favourite colour", "green"],
#         ["alice", "Planet", "Earth"],
#         ["alice", "Smell", "lavender"],
#         ["bob", "Favourite colour", "magenta"],
#         ["bob", "Planet", "Mars"],
#         ["bob", "Smell", "rose"],
#         ["charlie", "Favourite colour", "orange"],
#         ["charlie", "Planet", "Pluto"],
#         ["charlie", "Smell", "lynx"],
#     ]

#     cs = Columns(ByPath("groups"))
#     cs.add("Name", "name")

#     udfs = cs.group(
#         ByUserDefinedFields(
#             UserDefinedField("Favourite colour", "favourite_colour"),
#             UserDefinedField("Planet", "planet"),
#             UserDefinedField("Smell", "smell"),
#         )
#     )

#     udfs.add("UDF Name", "name")
#     udfs.add("UDF Value", "value")

#     cs.data.load(inp)

#     assert list(RowsRenderer(cs).render()) == exp
