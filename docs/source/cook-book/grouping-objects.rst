.. py:module:: rolumns
    :noindex:

Grouping by Objects
===================

The Problem
-----------

Our input data from :doc:`the Grouping by Lists example <grouping-lists>` has been extended to include the date that each employee starting holding each position:

.. code-block:: json

    [
        {
            "name": "Robert Pringles",
            "email": "bob@pringles.pop",
            "positions": [
                {
                    "year": 2008,
                    "title": "Founder"
                },
                {
                    "year": 2009,
                    "title": "CEO"
                }
            ]
        },
        {
            "name": "Daniel Sausage",
            "email": "danny@pringles.pop",
            "positions": [
                {
                    "year": 2010,
                    "title": "Head Chef"
                }
            ]
        },
        {
            "name": "Charlie Marmalade",
            "email": "charlie@pringles.pop",
            "positions": [
                {
                    "year": 2009,
                    "title": "Engineer"
                },
                {
                    "year": 2010,
                    "title": "Senior Engineer"
                },
                {
                    "year": 2011,
                    "title": "CTO"
                }
            ]
        }
    ]

We want to emit *Year* and *Title* columns to hold these values, so we'll add those to our *positions* grouping.

Code Sample
-----------

This code is identical to :doc:`the Grouping by Lists example <grouping-lists>` except for the *Year* and *Title* columns added to the *positions* column set. Note that each column's source path is relative to its column set's path.

.. testcode::

    from rolumns import Columns
    from rolumns.renderers import RowsRenderer

    data = [
        {
            "name": "Robert Pringles",
            "email": "bob@pringles.pop",
            "positions": [
                {
                    "year": 2008,
                    "title": "Founder"
                },
                {
                    "year": 2009,
                    "title": "CEO"
                }
            ]
        },
        {
            "name": "Daniel Sausage",
            "email": "danny@pringles.pop",
            "positions": [
                {
                    "year": 2010,
                    "title": "Head Chef"
                }
            ]
        },
        {
            "name": "Charlie Marmalade",
            "email": "charlie@pringles.pop",
            "positions": [
                {
                    "year": 2009,
                    "title": "Engineer"
                },
                {
                    "year": 2010,
                    "title": "Senior Engineer"
                },
                {
                    "year": 2011,
                    "title": "CTO"
                }
            ]
        }
    ]

    columns = Columns()
    columns.add("Name", "name")
    columns.add("Email", "email")

    positions = columns.group("positions")
    positions.add("Year", "year")
    positions.add("Title", "title")

    renderer = RowsRenderer(columns)
    rows = renderer.render(data)

    print(list(rows))

Result
------

.. testoutput::
   :options: +NORMALIZE_WHITESPACE

    [['Name',              'Email',              'Year', 'Title'],
     ['Robert Pringles',   'bob@pringles.pop',     2008, 'Founder'],
     ['Robert Pringles',   'bob@pringles.pop',     2009, 'CEO'],
     ['Daniel Sausage',    'danny@pringles.pop',   2010, 'Head Chef'],
     ['Charlie Marmalade', 'charlie@pringles.pop', 2009, 'Engineer'],
     ['Charlie Marmalade', 'charlie@pringles.pop', 2010, 'Senior Engineer'],
     ['Charlie Marmalade', 'charlie@pringles.pop', 2011, 'CTO']]
