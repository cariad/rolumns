.. py:module:: rolumns
    :noindex:

User-Defined Fields with Repeating Values
=========================================

The Problem
-----------

Sometimes you want to include repeating static values inside a group of user-defined fields.

For example, let's say we want to extend the example in :doc:`User-Defined Fields <udfs>` to repeat the same company information with every row of staff details:

.. code-block:: json

    {
        "company": {
            "name": "Pringles IT Services"
        },
        "staff": [
            {
                "name": "Robert Pringles",
                "email": "bob@pringles.pop",
                "title": "CEO"
            },
            {
                "name": "Daniel Sausage",
                "email": "danny@pringles.pop",
                "title": "Head Chef"
            },
            {
                "name": "Charlie Marmalade",
                "email": "charlie@pringles.pop",
                "title": "CTO"
            }
        ]
    }


We'll achieve this by passing the root column set's cursor to the new user-defined field.

Code Sample
-----------

This code is similar to :doc:`User-Defined Fields <udfs>`, but note that the new "Company" column attaches itself to the root column set's cursor. This override allows the "company.name" path to resolve to the "company" object in the root of the input data rather than a non-existant "company" object inside each staff member's record.

.. testcode::

    from rolumns import ByUserDefinedFields, Columns, Source
    from rolumns.renderers import RowsRenderer

    data = {
        "company": {
            "name": "Pringles IT Services"
        },
        "staff": [
            {
                "name": "Robert Pringles",
                "email": "bob@pringles.pop",
                "title": "CEO"
            },
            {
                "name": "Daniel Sausage",
                "email": "danny@pringles.pop",
                "title": "Head Chef"
            },
            {
                "name": "Charlie Marmalade",
                "email": "charlie@pringles.pop",
                "title": "CTO"
            }
        ]
    }

    columns = Columns()

    staff = columns.group("staff")
    staff.add("Name", "name")

    by_udf = ByUserDefinedFields()
    by_udf.append("Email", "email")
    by_udf.append("Title", "title")
    by_udf.append("Company", Source(path="company.name", cursor=columns.cursor))

    udfs = staff.group(by_udf)
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
     ['Robert Pringles',   'Email',    'bob@pringles.pop'],
     ['Robert Pringles',   'Title',    'CEO'],
     ['Robert Pringles',   'Company',  'Pringles IT Services'],
     ['Daniel Sausage',    'Email',    'danny@pringles.pop'],
     ['Daniel Sausage',    'Title',    'Head Chef'],
     ['Daniel Sausage',    'Company',  'Pringles IT Services'],
     ['Charlie Marmalade', 'Email',    'charlie@pringles.pop'],
     ['Charlie Marmalade', 'Title',    'CTO'],
     ['Charlie Marmalade', 'Company',  'Pringles IT Services']]
