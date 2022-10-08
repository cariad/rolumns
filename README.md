# Rolumns

**Rolumns** is a Python package for squishing data into rows and columns.

## Installation

Rolumns requires Python 3.7 or later.

```console
pip install rolumns
```

## Examples

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
