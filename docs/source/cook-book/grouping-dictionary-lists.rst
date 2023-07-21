.. py:module:: rolumns
    :noindex:

Grouping Dictionary Lists
=========================

The Problem
-----------

In :doc:`the Grouping Dictionaries example <grouping-dictionaries>` the dictionary's values were flat objects. But what if the values are iterable?

.. code-block:: json

    {
        "today": [
            {
                "event": "Bought sausages"
            },
            {
                "event": "Bought bread"
            }
        ],
        "yesterday": [
            {
                "event": "Bought a train set"
            },
            {
                "event": "Bought a book"
            }
        ]
    }

To create another table with *When* and *Event* columns, we'll use the same :class:`ByKey` as before but we'll also extend the column set with an additional group for values.

Code Sample
-----------

Note that the column set is grouped via :class:`ByKey` and the path to the key name is read from :func:`ByKey.key()` as before, but now a child grouping is added via the :func:`ByKey.values()` function.

.. testcode::

    from rolumns import ByKey, Columns
    from rolumns.renderers import RowsRenderer

    data = {
        "today": [
            {
               "event": "Bought sausages",
            },
            {
                "event": "Bought bread",
            },
        ],
        "yesterday": [
            {
                "event": "Bought a train set",
            },
            {
                "event": "Bought a book",
            },
        ],
    }

    columns = Columns(ByKey())
    columns.add("When", ByKey.key())

    events = columns.group(ByKey.values())
    events.add("Event", "event")

    renderer = RowsRenderer(columns)
    rows = renderer.render(data)

    print(list(rows))

Result
------

.. testoutput::
   :options: +NORMALIZE_WHITESPACE

    [['When',      'Event'],
     ['today',     'Bought sausages'],
     ['today',     'Bought bread'],
     ['yesterday', 'Bought a train set'],
     ['yesterday', 'Bought a book']]
