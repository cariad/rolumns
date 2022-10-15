.. py:module:: rolumns
    :noindex:

Conditional Translating
=======================

The Problem
-----------

Sometimes your data will include hints for conditionally translating values. For example, this employee data indicates whether or not a person's address must be censored in reports:

.. code-block:: json

    [
        {
            "name": "Robert Pringles",
            "address": {
                "planet": "Earth",
                "secret": true
            }
        },
        {
            "name": "Daniel Sausage",
            "address": {
                "planet": "Mars",
                "secret": false
            }
        },
        {
            "name": "Charlie Marmalade",
            "address": {
                "planet": "Pluto",
                "secret": true
            }
        }
    ]

We'll achieve this by passing a translator into the *Address* column and interrogating the record's values to decide whether or not to censor the address.

Code Sample
-----------

This code is similar to :doc:`the Translating example <translating>` but note that the translator function now interrogates the :code:`state.record` to check if the address should be censored before deciding which value to return.

.. testcode::

    from rolumns import Columns, Source, TranslationState
    from rolumns.renderers import RowsRenderer

    def censor(state: TranslationState) -> str:
        if not state.record["address"]["secret"]:
           return state.value

        return (
            state.value[0]
            + "".join(["*" * (len(state.value) - 2)])
            + state.value[-1]
        )

    data = [
        {
            "name": "Robert Pringles",
            "address": {
                "planet": "Earth",
                "secret": True
            }
        },
        {
            "name": "Daniel Sausage",
            "address": {
                "planet": "Mars",
                "secret": False
            }
        },
        {
            "name": "Charlie Marmalade",
            "address": {
                "planet": "Pluto",
                "secret": True
            }
        }
    ]

    columns = Columns()
    columns.add("Name", "name")
    columns.add("Address", Source("address.planet", translator=censor))

    renderer = RowsRenderer(columns)
    rows = renderer.render(data)

    print(list(rows))

Result
------

.. testoutput::
   :options: +NORMALIZE_WHITESPACE

    [['Name',              'Address'],
     ['Robert Pringles',   'E***h'],
     ['Daniel Sausage',    'Mars'],
     ['Charlie Marmalade', 'P***o']]
