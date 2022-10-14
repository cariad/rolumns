A Flat Table with Child Records
===============================

The Problem
-----------

Our input data from :doc:`the Flat Table example <flat>` has been extended to add an *address* object per employee:

.. code-block:: json

    [
        {
            "name": "Robert Pringles",
            "email": "bob@pringles.pop",
            "address": {
                "planet": "Earth"
            }
        },
        {
            "name": "Daniel Sausage",
            "email": "danny@pringles.pop",
            "address": {
                "planet": "Mars"
            }
        },
        {
            "name": "Charlie Marmalade",
            "email": "charlie@pringles.pop",
            "address": {
                "planet": "Pluto"
            }
        }
    ]

To add a *Planet* column to our table, we'll describe a path that drills into this new child object.

Code Sample
-----------

This code is identical to :doc:`the Flat Table example <flat>` except for a new *Planet* column, which uses dots to describe a path into the *address* child object:

.. testcode::

    from rolumns import Columns
    from rolumns.renderers import RowsRenderer

    data = [
        {
            "name": "Robert Pringles",
            "email": "bob@pringles.pop",
            "address": {
                "planet": "Earth"
            }
        },
        {
            "name": "Daniel Sausage",
            "email": "danny@pringles.pop",
            "address": {
                "planet": "Mars"
            }
        },
        {
            "name": "Charlie Marmalade",
            "email": "charlie@pringles.pop",
            "address": {
                "planet": "Pluto"
            }
        },
    ]

    columns = Columns()
    columns.add("Name", "name")
    columns.add("Email", "email")
    columns.add("Planet", "address.planet")

    renderer = RowsRenderer(columns)
    rows = renderer.render(data)

    print(list(rows))

Result
------

.. testoutput::
   :options: +NORMALIZE_WHITESPACE

    [['Name',              'Email',                'Planet'],
     ['Robert Pringles',   'bob@pringles.pop',     'Earth'],
     ['Daniel Sausage',    'danny@pringles.pop',   'Mars'],
     ['Charlie Marmalade', 'charlie@pringles.pop', 'Pluto']]
