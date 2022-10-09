import rolumns
import rolumns.renderers
import rolumns.translators


def test_simple() -> None:
    data = {
        "name": "Robert Pringles",
        "email": "bob@pringles.pop",
    }

    columns = rolumns.Columns()
    columns.add("Name", "name")
    columns.add("Email", "email")

    rows_renderer = rolumns.renderers.RowsRenderer(columns)

    expect_rows = [
        ["Name", "Email"],
        ["Robert Pringles", "bob@pringles.pop"],
    ]

    assert list(rows_renderer.render(data)) == expect_rows

    md_renderer = rolumns.renderers.MarkdownRenderer(columns)

    expect_md = [
        "| Name | Email |",
        "| - | - |",
        "| Robert Pringles | bob@pringles.pop |",
    ]

    assert list(md_renderer.render(data)) == expect_md


def test_multiple() -> None:
    data = [
        {
            "name": "Robert Pringles",
            "email": "bob@pringles.pop",
        },
        {
            "name": "Daniel Sausage",
            "email": "dan@pringles.pop",
        },
        {
            "name": "Charlie Marmalade",
            "email": "charlie@pringles.pop",
        },
    ]

    columns = rolumns.Columns()
    columns.add("Name", "name")
    columns.add("Email", "email")

    renderer = rolumns.renderers.MarkdownRenderer(columns)
    rows = renderer.render(data)

    expect = [
        "| Name | Email |",
        "| - | - |",
        "| Robert Pringles | bob@pringles.pop |",
        "| Daniel Sausage | dan@pringles.pop |",
        "| Charlie Marmalade | charlie@pringles.pop |",
    ]

    assert list(rows) == expect


def test_child() -> None:
    data = [
        {
            "name": "Robert Pringles",
            "email": "bob@pringles.pop",
            "address": {
                "planet": "Earth",
            },
        },
        {
            "name": "Charlie Marmalade",
            "email": "charlie@pringles.pop",
            "address": {
                "planet": "Mars",
            },
        },
    ]

    columns = rolumns.Columns()
    columns.add("Name", "name")
    columns.add("Email", "email")
    columns.add("Planet", "address.planet")

    renderer = rolumns.renderers.MarkdownRenderer(columns)
    rows = renderer.render(data)

    expect = [
        "| Name | Email | Planet |",
        "| - | - | - |",
        "| Robert Pringles | bob@pringles.pop | Earth |",
        "| Charlie Marmalade | charlie@pringles.pop | Mars |",
    ]

    assert list(rows) == expect


def test_repeating() -> None:
    data = [
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

    columns = rolumns.Columns()
    columns.add("Name", "name")
    columns.add("Email", "email")

    positions = columns.add_group("positions")
    positions.add("Year", "year")
    positions.add("Title", "title")

    renderer = rolumns.renderers.MarkdownRenderer(columns)
    rows = renderer.render(data)

    expect = [
        "| Name | Email | Year | Title |",
        "| - | - | - | - |",
        "| Robert Pringles | bob@pringles.pop | 2008 | Founder |",
        "| Robert Pringles | bob@pringles.pop | 2009 | CEO |",
        "| Charlie Marmalade | charlie@pringles.pop | 2009 | Engineer |",
        "| Charlie Marmalade | charlie@pringles.pop | 2010 | Senior Engineer |",
        "| Charlie Marmalade | charlie@pringles.pop | 2011 | CTO |",
    ]

    assert list(rows) == expect


def test_repeating_chained() -> None:
    data = [
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

    columns = rolumns.Columns()
    columns.add("Name", "name")
    columns.add("Email", "email")

    positions = columns.add_group("positions")
    positions.add("Year", "year")
    positions.add("Title", "title")

    awards = positions.add_group("awards")
    awards.add("Award", "award")

    renderer = rolumns.renderers.MarkdownRenderer(columns)
    rows = renderer.render(data)

    expect = [
        "| Name | Email | Year | Title | Award |",
        "| - | - | - | - | - |",
        "| Robert Pringles | bob@pringles.pop | 2008 | Founder | Best Coffee |",
        "| Robert Pringles | bob@pringles.pop | 2009 | CEO | Fastest Doughnut Run |",
        "| Robert Pringles | bob@pringles.pop | 2009 | CEO | Tie of the Year |",
        "| Charlie Marmalade | charlie@pringles.pop | 2009 | Engineer | Engineer of the Decade |",  # noqa: E501
        "| Charlie Marmalade | charlie@pringles.pop | 2009 | Engineer | Least Security Vulnerabilities |",  # noqa: E501
        "| Charlie Marmalade | charlie@pringles.pop | 2010 | Senior Engineer | Best Code Reviews |",  # noqa: E501
        "| Charlie Marmalade | charlie@pringles.pop | 2011 | CTO | Cloud Uplift of the Century |",  # noqa: E501
    ]

    assert list(rows) == expect


def test_translate() -> None:
    data = [
        {
            "name": "Robert Pringles",
            "email": "bob@pringles.pop",
        },
        {
            "name": "Daniel Sausage",
            "email": "dan@pringles.pop",
        },
        {
            "name": "Charlie Marmalade",
            "email": "charlie@pringles.pop",
        },
    ]

    def censor(state: rolumns.translators.TranslationState) -> str:
        value = str("" if state.value is None else state.value)

        if len(value) < 3:
            return "".join(["*" * len(value)])

        return value[0] + "".join(["*" * (len(value) - 2)]) + value[-1]

    columns = rolumns.Columns()
    columns.add("Name", "name")
    columns.add("Email", rolumns.Source("email", translator=censor))

    renderer = rolumns.renderers.MarkdownRenderer(columns)

    expect = [
        "| Name | Email |",
        "| - | - |",
        "| Robert Pringles | b**************p |",
        "| Daniel Sausage | d**************p |",
        "| Charlie Marmalade | c******************p |",
    ]

    assert list(renderer.render(data)) == expect
