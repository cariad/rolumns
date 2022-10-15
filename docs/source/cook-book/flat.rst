.. py:module:: rolumns
    :noindex:

A Flat Table
============

The Problem
-----------

Say we want to transform this list of records into a table with *Name* and *Email* columns:

.. code-block:: json

    [
        {
            "name": "Robert Pringles",
            "email": "bob@pringles.pop"
        },
        {
            "name": "Daniel Sausage",
            "email": "danny@pringles.pop"
        },
        {
            "name": "Charlie Marmalade",
            "email": "charlie@pringles.pop"
        }
    ]


We'll achieve this by creating a **column set** then passing it -- and the input data -- into a **renderer**.

Code Sample
-----------

In the code below, we:

1. Create a :class:`Columns` column set.
2. Add *Name* and *Email* columns to the set. The first argument of :func:`Columns.add` is the column's name and the second is the source key in our input data.
3. Create a :class:`renderers.RowsRenderer` renderer for our column set.
4. Render the input data.

.. testcode::

    from rolumns import Columns
    from rolumns.renderers import RowsRenderer

    data = [
        {
            "name": "Robert Pringles",
            "email": "bob@pringles.pop",
        },
        {
            "name": "Daniel Sausage",
            "email": "danny@pringles.pop",
        },
        {
            "name": "Charlie Marmalade",
            "email": "charlie@pringles.pop",
        },
    ]

    columns = Columns()
    columns.add("Name", "name")
    columns.add("Email", "email")

    renderer = RowsRenderer(columns)
    rows = renderer.render(data)

    print(list(rows))

Result
------

Each object yielded by the :code:`rows` iterator represents a row in a table, and each row is a list of its cells:

.. testoutput::
   :options: +NORMALIZE_WHITESPACE

    [['Name',              'Email'],
     ['Robert Pringles',   'bob@pringles.pop'],
     ['Daniel Sausage',    'danny@pringles.pop'],
     ['Charlie Marmalade', 'charlie@pringles.pop']]
