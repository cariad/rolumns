# Rolumns

**Rolumns** is a Python package for squishing data into rows and columns.

## Installation

Rolumns requires Python 3.7 or later.

```console
pip install rolumns
```

## Usage

### A simple dataset

Say we have this data that we want to transform into a table with "Name" and "Email" columns:

```json
{
    "name": "Robert Pringles",
    "email": "bob@pringles.pop"
}
```

We'll start by creating and adding our columns to a `rolumns.Columns` instance.

The first argument of `add` is the name and the second is the value key:

```python
import rolumns

data = {
    "name": "Robert Pringles",
    "email": "bob@pringles.pop",
}

columns = rolumns.Columns()
columns.add("Name", "name")
columns.add("Email", "email")
```

To create a list of rows that make up a table, we pass those columns into a `rolumns.renderers.RowsRenderer` instance then call `render`:

```python
renderer = rolumns.renderers.RowsRenderer(columns)
rows = renderer.render(data)
```

This creates an iterable list of lists that can be passed into something like [openpyxl](https://openpyxl.readthedocs.io) to emit an Excel spreadsheet:

```json
[
    ["Name",            "Email"],
    ["Robert Pringles", "bob@pringles.pop"],
]
```

You can also render to Markdown via the `rolumns.renderers.MarkdownRenderer`:

```python
renderer = rolumns.renderers.MarkdownRenderer(columns)
markdown = renderer.render(data)
```

| Name | Email |
| - | - |
| Robert Pringles | bob@pringles.pop |

### Multiple rows

Since single-row tables are boring, you can pass an iterable list into the renderers to get multiple rows:

```python
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
```

| Name | Email |
| - | - |
| Robert Pringles | bob@pringles.pop |
| Daniel Sausage | dan@pringles.pop |
| Charlie Marmalade | charlie@pringles.pop |

### Reading child objects

Say our data has been extended with an "address" key. To include a "Planet" column in our output, set its path to `address.planet` to drill into the `address` object:

```python
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
```

| Name | Email | Planet |
| - | - | - |
| Robert Pringles | bob@pringles.pop | Earth |
| Charlie Marmalade | charlie@pringles.pop | Mars |

### Column sets and repeating data

You can add as many columns to an `rolumns.Columns` instance as you like, and you can add at most one repeating group too.

For example, let's say our data has been extended to include employment history:

```json
[
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
```

If we want to keep "Name" and "Email" in our table, but repeat those rows for each employment position, we start by adding the first two columns exactly as before:

```python
columns = rolumns.Columns()
columns.add("Name", "name")
columns.add("Email", "email")
```

To add the repeating group, we append a new `rolumns.Columns` instance to our root set by calling `add_group`. The parameter describes where to find the repeating data, and the columns we add to that new set describe where to find their values within that group:

```python
positions = columns.add_group("positions")
positions.add("Year", "year")
positions.add("Title", "title")
```

The full code sample looks like this:

```python
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
```

| Name | Email | Year | Title |
| - | - | - | - |
| Robert Pringles | bob@pringles.pop | 2008 | Founder |
| Robert Pringles | bob@pringles.pop | 2009 | CEO |
| Charlie Marmalade | charlie@pringles.pop | 2009 | Engineer |
| Charlie Marmalade | charlie@pringles.pop | 2010 | Senior Engineer |
| Charlie Marmalade | charlie@pringles.pop | 2011 | CTO |

Naturally, groups can also be grouped:

```python
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
```

| Name | Email | Year | Title | Award |
| - | - | - | - | - |
| Robert Pringles | bob@pringles.pop | 2008 | Founder | Best Coffee |
| Robert Pringles | bob@pringles.pop | 2009 | CEO | Fastest Doughnut Run |
| Robert Pringles | bob@pringles.pop | 2009 | CEO | Tie of the Year |
| Charlie Marmalade | charlie@pringles.pop | 2009 | Engineer | Engineer of the Decade |
| Charlie Marmalade | charlie@pringles.pop | 2009 | Engineer | Least Security Vulnerabilities |
| Charlie Marmalade | charlie@pringles.pop | 2010 | Senior Engineer | Best Code Reviews |
| Charlie Marmalade | charlie@pringles.pop | 2011 | CTO | Cloud Uplift of the Century |
