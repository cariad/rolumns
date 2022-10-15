.. py:module:: rolumns
    :noindex:

User-Defined Fields
===================

The Problem
-----------

User-defined fields allow you to pivot a table. For example, given this data:

.. code-block:: json

    [
        {
            "name": "Robert Pringles",
            "address": "Earth",
            "email": "bob@pringles.pop",
            "title": "CEO"
        },
        {
            "name": "Daniel Sausage",
            "address": "Mars",
            "email": "danny@pringles.pop",
            "title": "Head Chef"
        },
        {
            "name": "Charlie Marmalade",
            "address": "Pluto",
            "email": "charlie@pringles.pop",
            "title": "CTO"
        }
    ]

--we already know how to create table like this:

.. list-table:: No User-Defined Fields
   :widths: 30 20 30 20
   :header-rows: 1

   * - Name
     - Address
     - Email
     - Title
   * - Robert Pringles
     - Earth
     - bob@pringles.pop
     - CEO
   * - Daniel Sausage
     - Mars
     - danny@pringles.pop
     - Head Chef
   * - Charlie Marmalade
     - Pluto
     - charlie@pringles.pop
     - CTO

--but we might prefer to pivot that same data like this:

.. list-table:: User-Defined Fields
   :widths: 40 20 40
   :header-rows: 1

   * - Name
     - Property
     - Value
   * - Robert Pringles
     - Address
     - Earth
   * - Robert Pringles
     - Email
     - bob@pringles.pop
   * - Robert Pringles
     - Title
     - CEO
   * - Daniel Sausage
     - Address
     - Mars
   * - Daniel Sausage
     - Email
     - danny@pringles.pop
   * - Daniel Sausage
     - Title
     - Head Chef
   * - Charlie Marmalade
     - Address
     - Pluto
   * - Charlie Marmalade
     - Email
     - charlie@pringles.pop
   * - Charlie Marmalade
     - Title
     - CTO

We'll achieve this by using a :class:`groups.ByUserDefinedFields` group type.

Code Sample
-----------

This code is similar to :doc:`the Flat Table example <flat>`, but note:

1. An :class:`groups.ByUserDefinedFields` instance is created and the user-defined fields are appended. Just like with columns, the first argument is the name and the second is the path to the data.
2. The :class:`groups.ByUserDefinedFields` instance is set as the root column set's group.
3. Two *Property* and *Value* columns are added to include the field names and values in the render. The names can be anything you want, but the paths must be the :py:attr:`groups.ByUserDefinedFields.NAME` and :py:attr:`groups.ByUserDefinedFields.VALUE` tokens.

.. testcode::

    from rolumns import Columns, Source
    from rolumns.groups import ByUserDefinedFields
    from rolumns.renderers import RowsRenderer

    data = [
        {
            "name": "Robert Pringles",
            "address": "Earth",
            "email": "bob@pringles.pop",
            "title": "CEO"
        },
        {
            "name": "Daniel Sausage",
            "address": "Mars",
            "email": "danny@pringles.pop",
            "title": "Head Chef"
        },
        {
            "name": "Charlie Marmalade",
            "address": "Pluto",
            "email": "charlie@pringles.pop",
            "title": "CTO"
        }
    ]

    columns = Columns()
    columns.add("Name", "name")

    group = ByUserDefinedFields()
    group.append("Address", "address")
    group.append("Email", "email")
    group.append("Title", "title")

    udfs = columns.group(group)
    udfs.add("Property", ByUserDefinedFields.NAME)
    udfs.add("Value", ByUserDefinedFields.VALUE)

    renderer = RowsRenderer(columns)
    rows = renderer.render(data)

    print(list(rows))

Result
------

.. testoutput::
   :options: +NORMALIZE_WHITESPACE

    [['Name',              'Property', 'Value'],
     ['Robert Pringles',   'Address',  'Earth'],
     ['Robert Pringles',   'Email',    'bob@pringles.pop'],
     ['Robert Pringles',   'Title',    'CEO'],
     ['Daniel Sausage',    'Address',  'Mars'],
     ['Daniel Sausage',    'Email',    'danny@pringles.pop'],
     ['Daniel Sausage',    'Title',    'Head Chef'],
     ['Charlie Marmalade', 'Address',  'Pluto'],
     ['Charlie Marmalade', 'Email',    'charlie@pringles.pop'],
     ['Charlie Marmalade', 'Title',    'CTO']]
