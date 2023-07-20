# from pytest import raises

# from rolumns.columns import Columns
# from rolumns.exceptions import MultipleGroups
# from rolumns.groups import ByKey


# def test_create_repeater__multiple() -> None:
#     cs = Columns()
#     cs.group("")

#     with raises(MultipleGroups) as ex:
#         cs.group("")

#     assert str(ex.value) == "A column set cannot have multiple groups"


# def test_normalize() -> None:
#     data = [
#         {
#             "name": "Robert Pringles",
#             "email": "bob@pringles.pop",
#             "sandwich_order": "vegan cheese & pickle",
#             "positions": [
#                 {
#                     # This "start" property is to ensure that the input schema
#                     # is different than the output schema.
#                     "start": {
#                         "year": 2008,
#                     },
#                     "title": "Founder",
#                 },
#                 {
#                     "start": {"year": 2009},
#                     "title": "CEO",
#                 },
#             ],
#         },
#         {
#             "name": "Charlie Marmalade",
#             "email": "charlie@pringles.pop",
#             "sandwich_order": "marmalade bagel",
#             "positions": [
#                 {
#                     "start": {
#                         "year": 2009,
#                     },
#                     "title": "Engineer",
#                 },
#                 {
#                     "start": {
#                         "year": 2010,
#                     },
#                     "title": "Senior Engineer",
#                 },
#                 {
#                     "start": {
#                         "year": 2011,
#                     },
#                     "title": "CTO",
#                 },
#             ],
#         },
#     ]

#     cs = Columns()
#     cs.add("Name", "name")
#     cs.add("Email", "email")
#     positions = cs.group("positions")
#     positions.add("Year", "start.year")
#     positions.add("Title", "title")

#     expect = [
#         {
#             "Name": "Robert Pringles",
#             "Email": "bob@pringles.pop",
#             "positions": [
#                 {
#                     "Year": 2008,
#                     "Title": "Founder",
#                 },
#                 {
#                     "Year": 2009,
#                     "Title": "CEO",
#                 },
#             ],
#         },
#         {
#             "Name": "Charlie Marmalade",
#             "Email": "charlie@pringles.pop",
#             "positions": [
#                 {
#                     "Year": 2009,
#                     "Title": "Engineer",
#                 },
#                 {
#                     "Year": 2010,
#                     "Title": "Senior Engineer",
#                 },
#                 {
#                     "Year": 2011,
#                     "Title": "CTO",
#                 },
#             ],
#         },
#     ]

#     cs.data.load(data)

#     assert cs.normalize() == expect


# def test_normalize_dict_flat() -> None:
#     data = {
#         "today": {
#             "event": "Bought sausages",
#         },
#         "yesterday": {
#             "event": "Bought a train set",
#         },
#     }

#     cs = Columns(ByKey())
#     cs.add("When", ByKey.key())
#     cs.add("Event", ByKey.value("event"))

#     expect = [
#         {
#             "When": "today",
#             "Event": "Bought sausages",
#         },
#         {
#             "When": "yesterday",
#             "Event": "Bought a train set",
#         },
#     ]

#     cs.data.load(data)

#     assert cs.normalize() == expect


# def test_normalize_dict_flat_as_group() -> None:
#     data = {
#         "today": {
#             "event": "Bought sausages",
#         },
#         "yesterday": {
#             "event": "Bought a train set",
#         },
#     }

#     cs = Columns(ByKey())
#     cs.add("When", ByKey.key())
#     values = cs.group(ByKey.values())
#     values.add("Event", "event")

#     expect = [
#         {
#             "When": "today",
#             "__by_value__": [
#                 {
#                     "Event": "Bought sausages",
#                 },
#             ],
#         },
#         {
#             "When": "yesterday",
#             "__by_value__": [
#                 {
#                     "Event": "Bought a train set",
#                 },
#             ],
#         },
#     ]

#     cs.data.load(data)

#     assert cs.normalize() == expect


# # def test_normalize_dict_list() -> None:
# #     data = {
# #         "today": [
# #             {
# #                 "event": "Bought sausages",
# #             },
# #             {
# #                 "event": "Bought bread",
# #             },
# #         ],
# #         "yesterday": [
# #             {
# #                 "event": "Bought a train set",
# #             },
# #             {
# #                 "event": "Bought a book",
# #             },
# #         ],
# #     }

# #     cs = Columns(ByKey())
# #     cs.add("When", ByKey.key())
# #     values = cs.group(ByKey.values())
# #     values.add("Event", "event")

# #     expect = [
# #         {
# #             "When": "today",
# #             "__by_value__": [
# #                 {
# #                     "Event": "Bought sausages",
# #                 },
# #                 {
# #                     "Event": "Bought bread",
# #                 },
# #             ],
# #         },
# #         {
# #             "When": "yesterday",
# #             "__by_value__": [
# #                 {
# #                     "Event": "Bought a train set",
# #                 },
# #                 {
# #                     "Event": "Bought a book",
# #                 },
# #             ],
# #         },
# #     ]

# #     cs.data.load(data)

# #     assert cs.normalize() == expect


# def test_normalized_to_column_values() -> None:
#     resolved = [
#         {
#             "name": "Robert Pringles",
#             "email": "bob@pringles.pop",
#             "positions": [
#                 {
#                     "year": 2008,
#                     "title": "Founder",
#                 },
#                 {
#                     "year": 2009,
#                     "title": "CEO",
#                 },
#             ],
#         },
#         {
#             "name": "Charlie Marmalade",
#             "email": "charlie@pringles.pop",
#             "positions": [
#                 {
#                     "year": 2009,
#                     "title": "Engineer",
#                 },
#                 {
#                     "year": 2010,
#                     "title": "Senior Engineer",
#                 },
#                 {
#                     "year": 2011,
#                     "title": "CTO",
#                 },
#             ],
#         },
#     ]

#     expect = {
#         "email": [
#             "bob@pringles.pop",
#             "bob@pringles.pop",
#             "charlie@pringles.pop",
#             "charlie@pringles.pop",
#             "charlie@pringles.pop",
#         ],
#         "name": [
#             "Robert Pringles",
#             "Robert Pringles",
#             "Charlie Marmalade",
#             "Charlie Marmalade",
#             "Charlie Marmalade",
#         ],
#         "title": [
#             "Founder",
#             "CEO",
#             "Engineer",
#             "Senior Engineer",
#             "CTO",
#         ],
#         "year": [
#             2008,
#             2009,
#             2009,
#             2010,
#             2011,
#         ],
#     }
#     assert Columns.normalized_to_column_values(resolved) == expect


# def test_normalized_to_column_values__chained() -> None:
#     resolved = [
#         {
#             "name": "Robert Pringles",
#             "email": "bob@pringles.pop",
#             "positions": [
#                 {
#                     "year": 2008,
#                     "title": "Founder",
#                     "awards": [
#                         {"award": "Best Coffee"},
#                     ],
#                 },
#                 {
#                     "year": 2009,
#                     "title": "CEO",
#                     "awards": [
#                         {"award": "Fastest Doughnut Run"},
#                         {"award": "Tie of the Year"},
#                     ],
#                 },
#             ],
#         },
#         {
#             "name": "Charlie Marmalade",
#             "email": "charlie@pringles.pop",
#             "positions": [
#                 {
#                     "year": 2009,
#                     "title": "Engineer",
#                     "awards": [
#                         {"award": "Engineer of the Decade"},
#                         {"award": "Least Security Vulnerabilities"},
#                     ],
#                 },
#                 {
#                     "year": 2010,
#                     "title": "Senior Engineer",
#                     "awards": [
#                         {"award": "Best Code Reviews"},
#                     ],
#                 },
#                 {
#                     "year": 2011,
#                     "title": "CTO",
#                     "awards": [
#                         {"award": "Cloud Uplift of the Century"},
#                     ],
#                 },
#             ],
#         },
#     ]

#     expect = {
#         "award": [
#             "Best Coffee",
#             "Fastest Doughnut Run",
#             "Tie of the Year",
#             "Engineer of the Decade",
#             "Least Security Vulnerabilities",
#             "Best Code Reviews",
#             "Cloud Uplift of the Century",
#         ],
#         "email": [
#             "bob@pringles.pop",
#             "bob@pringles.pop",
#             "bob@pringles.pop",
#             "charlie@pringles.pop",
#             "charlie@pringles.pop",
#             "charlie@pringles.pop",
#             "charlie@pringles.pop",
#         ],
#         "name": [
#             "Robert Pringles",
#             "Robert Pringles",
#             "Robert Pringles",
#             "Charlie Marmalade",
#             "Charlie Marmalade",
#             "Charlie Marmalade",
#             "Charlie Marmalade",
#         ],
#         "title": [
#             "Founder",
#             "CEO",
#             "CEO",
#             "Engineer",
#             "Engineer",
#             "Senior Engineer",
#             "CTO",
#         ],
#         "year": [
#             2008,
#             2009,
#             2009,
#             2009,
#             2009,
#             2010,
#             2011,
#         ],
#     }
#     assert Columns.normalized_to_column_values(resolved) == expect


# def test_records__dict_flat() -> None:
#     data = {
#         "today": {
#             "event": "Bought sausages",
#         },
#         "yesterday": {
#             "event": "Bought a train set",
#         },
#     }

#     cs = Columns(ByKey())

#     expect = [
#         {
#             "key": "today",
#             "value": {"event": "Bought sausages"},
#         },
#         {
#             "key": "yesterday",
#             "value": {"event": "Bought a train set"},
#         },
#     ]

#     cs.data.load(data)

#     assert list(cs.records()) == expect


# def test_records__dict_list() -> None:
#     data = {
#         "today": [
#             {"event": "Bought sausages"},
#             {"event": "Bought bread"},
#         ],
#         "yesterday": [
#             {"event": "Bought a train set"},
#             {"event": "Bought a book"},
#         ],
#     }

#     cs = Columns(ByKey())

#     expect = [
#         {
#             "key": "today",
#             "value": [
#                 {"event": "Bought sausages"},
#                 {"event": "Bought bread"},
#             ],
#         },
#         {
#             "key": "yesterday",
#             "value": [
#                 {"event": "Bought a train set"},
#                 {"event": "Bought a book"},
#             ],
#         },
#     ]

#     cs.data.load(data)

#     assert list(cs.records()) == expect
