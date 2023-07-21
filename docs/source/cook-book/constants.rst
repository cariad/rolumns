.. py:module:: rolumns
    :noindex:

Constants
=========

The Problem
-----------

Sometimes you want to bind a column to a static constant that doesn't exist within your source data.

We'll achieve this by binding the constant to the column's :class:`Source`.

Code Sample
-----------

.. testcode::

    from rolumns import Columns, Source
    from rolumns.renderers import RowsRenderer

    data = [
        {
            "name": "Robert Pringles",
            "address": {
                "planet": "Earth"
            }
        },
        {
            "name": "Daniel Sausage",
            "address": {
                "planet": "Mars"
            }
        },
        {
            "name": "Charlie Marmalade",
            "address": {
                "planet": "Pluto"
            }
        }
    ]

    columns = Columns()
    columns.add("Name", "name")
    columns.add("Address", "address.planet")
    columns.add("Lives on a Planet?", Source(constant="Yes"))

    renderer = RowsRenderer(columns)
    rows = renderer.render(data)

    print(list(rows))

Result
------

.. testoutput::
   :options: +NORMALIZE_WHITESPACE

    [['Name',              'Address', 'Lives on a Planet?'],
     ['Robert Pringles',   'Earth',   'Yes'],
     ['Daniel Sausage',    'Mars',    'Yes'],
     ['Charlie Marmalade', 'Pluto',   'Yes']]
