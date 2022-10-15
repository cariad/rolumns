.. py:module:: rolumns
    :noindex:

Translating Values
==================

The Problem
-----------

Sometimes, you need to translate a value before it's rendered; perhaps to convert a string to a Python `datetime` instance, or to format a number a particular way.

In this case, let's say we want to write a table with the following data but the email addresses must be censored:

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


We'll achieve this by passing a translator into the *Email* column.

Code Sample
-----------

This code is identical to :doc:`the Flat Table example <flat>` except for the :class:`Source` being passed into the *Email* column. In the previous example, we passed in only the path; this is shorthand for a :class:`Source` with only a path. Now, we pass in both the path and translator as a :class:`Source` instance.

.. testcode::

    from rolumns import Columns, Source, TranslationState
    from rolumns.renderers import RowsRenderer

    def censor(state: TranslationState) -> str:
        return (
            state.value[0]
            + "".join(["*" * (len(state.value) - 2)])
            + state.value[-1]
        )

    data = [
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

    columns = Columns()
    columns.add("Name", "name")
    columns.add("Email", Source("email", translator=censor))

    renderer = RowsRenderer(columns)
    rows = renderer.render(data)

    print(list(rows))

Result
------

.. testoutput::
   :options: +NORMALIZE_WHITESPACE

    [['Name',              'Email'],
     ['Robert Pringles',   'b**************p'],
     ['Daniel Sausage',    'd****************p'],
     ['Charlie Marmalade', 'c******************p']]
