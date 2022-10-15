.. py:module:: rolumns
    :noindex:

Choosing Columns to Render
==========================

The Problem
-----------

In previous examples, we've always rendered columns in the order that we added them to their column sets. For example, in :doc:`the Grouping Groups example <grouping-groups>`, the root column set is rendered on the left, followed by the first grouping in the middle, then the final grouping on the right.

We can adjust the order of the columns during rendering by appending them directly to the renderer.

Code Sample
-----------

This code is similar to :doc:`the Grouping by Objects example <grouping-objects>` except for the three calls to :func:`renderers.RowsRenderer.append` which explicitly describe which columns to render and in what order:

.. testcode::

    from rolumns import Columns
    from rolumns.renderers import RowsRenderer

    data = [
        {
            "name": "Robert Pringles",
            "email": "bob@pringles.pop",
            "positions": [
                {
                    "year": 2008,
                    "title": "Founder",
                    "awards": [
                      "Best Product 2008",
                      "Founder of the Year",
                    ]
                },
                {
                    "year": 2009,
                    "title": "CEO",
                    "awards": [
                      "Fastest Doughnut Run",
                      "Tie of the Year"
                    ]
                }
            ]
        },
        {
            "name": "Daniel Sausage",
            "email": "danny@pringles.pop",
            "positions": [
                {
                    "year": 2010,
                    "title": "Head Chef",
                    "awards": [
                      "Salad of the Century",
                      "Soup of the Week",
                      "Sandwich of the Decade"
                    ]
                }
            ]
        },
        {
            "name": "Charlie Marmalade",
            "email": "charlie@pringles.pop",
            "positions": [
                {
                    "year": 2009,
                    "title": "Engineer",
                    "awards": [
                      "Engineer of the Month",
                      "Least Security Vulnerabilities 2009"
                    ]
                },
                {
                    "year": 2010,
                    "title": "Senior Engineer",
                    "awards": [
                      "Best Code Reviews",
                      "Support Champion 2010",
                    ]
                },
                {
                    "year": 2011,
                    "title": "CTO",
                    "awards": [
                      "Cloud Uplift of the Century",
                      "Worst Tie 2011",
                    ]
                }
            ]
        }
    ]

    columns = Columns()
    columns.add("Name", "name")
    columns.add("Email", "email")

    positions = columns.group("positions")
    positions.add("Year", "year")
    positions.add("Title", "title")

    awards = positions.group("awards")
    awards.add("Award")

    renderer = RowsRenderer(columns)
    renderer.append("Award")
    renderer.append("Name")
    renderer.append("Year")
    rows = renderer.render(data)

    print(list(rows))

Result
------

.. testoutput::
   :options: +NORMALIZE_WHITESPACE

    [['Award',                               'Name',            'Year'],
     ['Best Product 2008',                   'Robert Pringles',   2008],
     ['Founder of the Year',                 'Robert Pringles',   2008],
     ['Fastest Doughnut Run',                'Robert Pringles',   2009],
     ['Tie of the Year',                     'Robert Pringles',   2009],
     ['Salad of the Century',                'Daniel Sausage',    2010],
     ['Soup of the Week',                    'Daniel Sausage',    2010],
     ['Sandwich of the Decade',              'Daniel Sausage',    2010],
     ['Engineer of the Month',               'Charlie Marmalade', 2009],
     ['Least Security Vulnerabilities 2009', 'Charlie Marmalade', 2009],
     ['Best Code Reviews',                   'Charlie Marmalade', 2010],
     ['Support Champion 2010',               'Charlie Marmalade', 2010],
     ['Cloud Uplift of the Century',         'Charlie Marmalade', 2011],
     ['Worst Tie 2011',                      'Charlie Marmalade', 2011]]
