.. py:module:: rolumns
    :noindex:

Grouping Dictionaries
=====================

The Problem
-----------

Sometimes, rather being a list of records, the data you'd like to iterate is a dictionary:

.. code-block:: json

    {
        "today": {
            "event": "Bought sausages"
        },
        "yesterday": {
            "event": "Bought a train set"
        }
    }

To create a table with *When* and *Event* columns, we'll use a specific dictionary grouper.

Code Sample
-----------

Note that the column set is grouped via :class:`groups.ByKey`. The path to the key name is read from :func:`groups.ByKey.key()` and a path that drills into the key's value is built with the :func:`groups.ByKey.value()` function.

.. testcode::

    from rolumns import Columns
    from rolumns.groups import ByKey
    from rolumns.renderers import RowsRenderer

    data = {
        "today": {
            "event": "Bought sausages",
        },
        "yesterday": {
            "event": "Bought a train set",
        },
    }

    columns = Columns(ByKey())
    columns.add("When", ByKey.key())
    columns.add("Event", ByKey.value("event"))

    renderer = RowsRenderer(columns)
    rows = renderer.render(data)

    print(list(rows))

Result
------

.. testoutput::
   :options: +NORMALIZE_WHITESPACE

    [['When',      'Event'],
     ['today',     'Bought sausages'],
     ['yesterday', 'Bought a train set']]
