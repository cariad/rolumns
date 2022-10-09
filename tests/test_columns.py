from pytest import raises

from rolumns.columns import Columns
from rolumns.exceptions import MultipleRepeaters


def test_create_repeater__multiple() -> None:
    cs = Columns()
    cs.add_group("")

    with raises(MultipleRepeaters) as ex:
        cs.add_group("")

    expect = "A column set cannot have multiple repeaters as direct children"
    assert str(ex.value) == expect


def test_normalize() -> None:
    data = [
        {
            "name": "Robert Pringles",
            "email": "bob@pringles.pop",
            "sandwich_order": "vegan cheese & pickle",
            "positions": [
                {
                    # This "start" property is to ensure that the input schema
                    # is different than the output schema.
                    "start": {
                        "year": 2008,
                    },
                    "title": "Founder",
                },
                {
                    "start": {"year": 2009},
                    "title": "CEO",
                },
            ],
        },
        {
            "name": "Charlie Marmalade",
            "email": "charlie@pringles.pop",
            "sandwich_order": "marmalade bagel",
            "positions": [
                {
                    "start": {
                        "year": 2009,
                    },
                    "title": "Engineer",
                },
                {
                    "start": {
                        "year": 2010,
                    },
                    "title": "Senior Engineer",
                },
                {
                    "start": {
                        "year": 2011,
                    },
                    "title": "CTO",
                },
            ],
        },
    ]

    cs = Columns()
    cs.add("Name", "name")
    cs.add("Email", "email")
    positions = cs.add_group("positions")
    positions.add("Year", "start.year")
    positions.add("Title", "title")

    expect = [
        {
            "Name": "Robert Pringles",
            "Email": "bob@pringles.pop",
            "positions": [
                {
                    "Year": 2008,
                    "Title": "Founder",
                },
                {
                    "Year": 2009,
                    "Title": "CEO",
                },
            ],
        },
        {
            "Name": "Charlie Marmalade",
            "Email": "charlie@pringles.pop",
            "positions": [
                {
                    "Year": 2009,
                    "Title": "Engineer",
                },
                {
                    "Year": 2010,
                    "Title": "Senior Engineer",
                },
                {
                    "Year": 2011,
                    "Title": "CTO",
                },
            ],
        },
    ]

    assert cs.normalize(data) == expect


def test_normalized_to_column_values() -> None:
    resolved = [
        {
            "name": "Robert Pringles",
            "email": "bob@pringles.pop",
            "positions": [
                {
                    "year": 2008,
                    "title": "Founder",
                },
                {
                    "year": 2009,
                    "title": "CEO",
                },
            ],
        },
        {
            "name": "Charlie Marmalade",
            "email": "charlie@pringles.pop",
            "positions": [
                {
                    "year": 2009,
                    "title": "Engineer",
                },
                {
                    "year": 2010,
                    "title": "Senior Engineer",
                },
                {
                    "year": 2011,
                    "title": "CTO",
                },
            ],
        },
    ]

    expect = {
        "email": [
            "bob@pringles.pop",
            "bob@pringles.pop",
            "charlie@pringles.pop",
            "charlie@pringles.pop",
            "charlie@pringles.pop",
        ],
        "name": [
            "Robert Pringles",
            "Robert Pringles",
            "Charlie Marmalade",
            "Charlie Marmalade",
            "Charlie Marmalade",
        ],
        "title": [
            "Founder",
            "CEO",
            "Engineer",
            "Senior Engineer",
            "CTO",
        ],
        "year": [
            2008,
            2009,
            2009,
            2010,
            2011,
        ],
    }
    assert Columns.normalized_to_column_values(resolved) == expect


def test_normalized_to_column_values__chained() -> None:
    resolved = [
        {
            "name": "Robert Pringles",
            "email": "bob@pringles.pop",
            "positions": [
                {
                    "year": 2008,
                    "title": "Founder",
                    "awards": [
                        {"award": "Best Coffee"},
                    ],
                },
                {
                    "year": 2009,
                    "title": "CEO",
                    "awards": [
                        {"award": "Fastest Doughnut Run"},
                        {"award": "Tie of the Year"},
                    ],
                },
            ],
        },
        {
            "name": "Charlie Marmalade",
            "email": "charlie@pringles.pop",
            "positions": [
                {
                    "year": 2009,
                    "title": "Engineer",
                    "awards": [
                        {"award": "Engineer of the Decade"},
                        {"award": "Least Security Vulnerabilities"},
                    ],
                },
                {
                    "year": 2010,
                    "title": "Senior Engineer",
                    "awards": [
                        {"award": "Best Code Reviews"},
                    ],
                },
                {
                    "year": 2011,
                    "title": "CTO",
                    "awards": [
                        {"award": "Cloud Uplift of the Century"},
                    ],
                },
            ],
        },
    ]

    expect = {
        "award": [
            "Best Coffee",
            "Fastest Doughnut Run",
            "Tie of the Year",
            "Engineer of the Decade",
            "Least Security Vulnerabilities",
            "Best Code Reviews",
            "Cloud Uplift of the Century",
        ],
        "email": [
            "bob@pringles.pop",
            "bob@pringles.pop",
            "bob@pringles.pop",
            "charlie@pringles.pop",
            "charlie@pringles.pop",
            "charlie@pringles.pop",
            "charlie@pringles.pop",
        ],
        "name": [
            "Robert Pringles",
            "Robert Pringles",
            "Robert Pringles",
            "Charlie Marmalade",
            "Charlie Marmalade",
            "Charlie Marmalade",
            "Charlie Marmalade",
        ],
        "title": [
            "Founder",
            "CEO",
            "CEO",
            "Engineer",
            "Engineer",
            "Senior Engineer",
            "CTO",
        ],
        "year": [
            2008,
            2009,
            2009,
            2009,
            2009,
            2010,
            2011,
        ],
    }
    assert Columns.normalized_to_column_values(resolved) == expect
