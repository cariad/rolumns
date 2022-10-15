.. py:module:: rolumns
    :noindex:

Grouping by Lists
=================

The Problem
-----------

Our input data from :doc:`the Flat Table example <flat>` has been extended to include a list of positions that each employee has held:

.. code-block:: json

    [
        {
            "name": "Robert Pringles",
            "email": "bob@pringles.pop",
            "positions": [
              "Founder",
              "CEO"
            ]
        },
        {
            "name": "Daniel Sausage",
            "email": "danny@pringles.pop",
            "positions": [
              "Head Chef"
            ]
        },
        {
            "name": "Charlie Marmalade",
            "email": "charlie@pringles.pop",
            "positions": [
              "Engineer",
              "Senior Engineer",
              "CTO"
            ]
        }
    ]

We want to emit a row for each position and repeat the name and email address as-needed -- or, we want to *group* the positions by employee.

Each :class:`Columns` column set can reference multiple columns from a single flat record and at most one grouping set. So, to achieve this, we'll add a grouping set for the positions.

Code Sample
-----------

This code is identical to :doc:`the Flat Table example <flat>` except for the *positions* column set created by calling :func:`Columns.group`. The path passed in describes the path to the iterable collection.

Since the grouping set is just a :class:`Columns` column set, we can add columns to it exactly as before. Note, though, that the column doesn't have a source path because its column set iterates over primitive values rather than dictionaries.

.. testcode::

    from rolumns import Columns
    from rolumns.renderers import RowsRenderer

    data = [
        {
            "name": "Robert Pringles",
            "email": "bob@pringles.pop",
            "positions": [
              "Founder",
              "CEO"
            ]
        },
        {
            "name": "Daniel Sausage",
            "email": "danny@pringles.pop",
            "positions": [
              "Head Chef"
            ]
        },
        {
            "name": "Charlie Marmalade",
            "email": "charlie@pringles.pop",
            "positions": [
              "Engineer",
              "Senior Engineer",
              "CTO"
            ]
        }
    ]

    columns = Columns()
    columns.add("Name", "name")
    columns.add("Email", "email")

    positions = columns.group("positions")
    positions.add("Position")

    renderer = RowsRenderer(columns)
    rows = renderer.render(data)

    print(list(rows))

Result
------

.. testoutput::
   :options: +NORMALIZE_WHITESPACE

    [['Name',              'Email',                'Position'],
     ['Robert Pringles',   'bob@pringles.pop',     'Founder'],
     ['Robert Pringles',   'bob@pringles.pop',     'CEO'],
     ['Daniel Sausage',    'danny@pringles.pop',   'Head Chef'],
     ['Charlie Marmalade', 'charlie@pringles.pop', 'Engineer'],
     ['Charlie Marmalade', 'charlie@pringles.pop', 'Senior Engineer'],
     ['Charlie Marmalade', 'charlie@pringles.pop', 'CTO']]
