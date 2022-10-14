# Rolumns

**Rolumns** is a Python package for squishing data into rows and columns.

Full documentation is online at **[rolumns.dev](https://rolumns.dev)**.

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

### Translating values

Sometimes, you need to translate a value before it's rendered; perhaps to convert a string to a Python `datetime` instance, or to format a number as currency.

So, for example, let's say we want to censor the email addresses we're writing out to the table.

First, we write a function that takes a `rolumns.translators.TranslationState` state and returns the translated value:

```python
def censor(state: rolumns.translators.TranslationState) -> str:
    value = str("" if state.value is None else state.value)

    if len(value) < 3:
        return "".join(["*" * len(value)])

    return value[0] + "".join(["*" * (len(value) - 2)]) + value[-1]
```

Then, when we add the "Email" column to the column set, we pass an explicit `rolumns.Source` instance rather than just the string path:

```python
# columns.add("Email", "email")
columns.add("Email", Source("email", translator=censor))
```

Here's the full code sample:

```python
import rolumns
import rolumns.renderers
import rolumns.translators

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
columns.add("Email", rolumns.Source("email", translator=censor))

renderer = rolumns.renderers.MarkdownRenderer(columns)
rows = renderer.render(data)
```

| Name | Email |
| - | - |
| Robert Pringles | b**************p |
| Daniel Sausage | d****************p |
| Charlie Marmalade | c******************p |

A collection of translators are provided within `rolumns.translators`.

### User-defined fields

User-defined fields allow you to pivot a table.

For example, given this date:

```json
[
    {
        "name": "Robert Pringles",
        "address": "Earth",
        "email": "bob@pringles.pop",
        "title": "CEO"
    },
    {
        "name": "Daniel Sausage",
        "address": "Mars",
        "email": "dan@pringles.pop",
        "title": "Head Chef"
    },
    {
        "name": "Charlie Marmalade",
        "address": "Pluto",
        "email": "charlie@pringles.pop",
        "title": "CTO"
    }
]
```

...we already know how to create table like this:

| Name              | Address | Email                | Title     |
| -                 | -       | -                    | -         |
| Robert Pringles   | Earth   | bob@pringles.pop     | CEO       |
| Daniel Sausage    | Mars    | dan@pringles.pop     | Head Chef |
| Charlie Marmalade | Pluto   | charlie@pringles.pop | CTO       |

...but we might prefer to pivot the same data like this:

| Name | Property | Value |
| - | - | - |
| Robert Pringles | Address | Earth |
| Robert Pringles | Email | bob@pringles.pop |
| Robert Pringles | Title | CEO |
| Daniel Sausage | Address | Mars |
| Daniel Sausage | Email | dan@pringles.pop |
| Daniel Sausage | Title | Head Chef |
| Charlie Marmalade | Address | Pluto |
| Charlie Marmalade | Email | charlie@pringles.pop |
| Charlie Marmalade | Title | CTO |

To achieve this, we start by creating a typical column set and adding the "Name" column:

```python
columns = rolumns.Columns()
columns.add("Name", "name")
```

Now we'll create a `rolumns.groups.ByUserDefinedFields` instance and add our user-defined fields. The first argument describes the field name and the second argument describes the path to the value:

```python
group = rolumns.groups.ByUserDefinedFields()
group.append("Address", "address")
group.append("Email", "email")
group.append("Title", "title")
```

Now we'll pass this grouping to the root column set, where in previous examples we've passed the path to the collection to iterate:

```python
udfs = columns.add_group(group)
```

To add the field names and values to the column set, we call the same `add` function as before. The paths are specified by the `ByUserDefinedFields.NAME` and `ByUserDefinedFields.VALUE` constants:

```python
udfs.add("Property", rolumns.groups.ByUserDefinedFields.NAME)
udfs.add("Value", rolumns.groups.ByUserDefinedFields.VALUE)
```

The full code sample looks like this:

```python
data = [
    {
        "name": "Robert Pringles",
        "address": "Earth",
        "email": "bob@pringles.pop",
        "title": "CEO",
    },
    {
        "name": "Daniel Sausage",
        "address": "Mars",
        "email": "dan@pringles.pop",
        "title": "Head Chef",
    },
    {
        "name": "Charlie Marmalade",
        "address": "Pluto",
        "email": "charlie@pringles.pop",
        "title": "CTO",
    },
]

columns = rolumns.Columns()
columns.add("Name", "name")

group = rolumns.groups.ByUserDefinedFields()
group.append("Address", "address")
group.append("Email", "email")
group.append("Title", "title")

udfs = columns.add_group(group)
udfs.add("Property", rolumns.groups.ByUserDefinedFields.NAME)
udfs.add("Value", rolumns.groups.ByUserDefinedFields.VALUE)

renderer = rolumns.renderers.MarkdownRenderer(columns)
rows = renderer.render(data)
```

| Name | Property | Value |
| - | - | - |
| Robert Pringles | Address | Earth |
| Robert Pringles | Email | bob@pringles.pop |
| Robert Pringles | Title | CEO |
| Daniel Sausage | Address | Mars |
| Daniel Sausage | Email | dan@pringles.pop |
| Daniel Sausage | Title | Head Chef |
| Charlie Marmalade | Address | Pluto |
| Charlie Marmalade | Email | charlie@pringles.pop |
| Charlie Marmalade | Title | CTO |
