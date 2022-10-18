.. py:module:: rolumns
    :noindex:

Aligning Markdown Columns
=========================

The Problem
-----------

The :class:`renderers.MarkdownRenderer` aligns columns to the left by default, but what if you prefer to align some columns to the right instead -- like numbers?

.. code-block:: json

    [
        {
            "favourite_number": "10",
            "name": "alice"
        },
        {
            "favourite_number": "100",
            "name": "bob"
        },
        {
            "favourite_number": "1000",
            "name": "charlie"
        }
    ]

We'll achieve this by explicitly adding the columns to :class:`renderers.MarkdownRenderer` with alignments.

Code Sample
-----------

.. testcode::

    from rolumns import Columns
    from rolumns.enums import ColumnAlignment
    from rolumns.renderers import MarkdownRenderer

    data = [
        {
            "favourite_number": "10",
            "name": "alice"
        },
        {
            "favourite_number": "100",
            "name": "bob"
        },
        {
            "favourite_number": "1000",
            "name": "charlie"
        }
    ]

    columns = Columns()
    columns.add("Name", "name")
    columns.add("Favourite Number", "favourite_number")

    renderer = MarkdownRenderer(columns)
    renderer.append("Name")
    renderer.append("Favourite Number", ColumnAlignment.RIGHT)

    print(renderer.render_string(data))

Result
------

.. testoutput::
   :options: +NORMALIZE_WHITESPACE

    | Name    | Favourite Number |
    | ------- | ---------------: |
    | alice   |               10 |
    | bob     |              100 |
    | charlie |             1000 |
