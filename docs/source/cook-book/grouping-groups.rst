.. py:module:: rolumns
    :noindex:

Grouping Groups
===============

The Problem
-----------

Our input data from :doc:`the Grouping by Objects example <grouping-objects>` has been extended to include a list of awards that each employee achieved during their time in each position:

.. code-block:: json

    [
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

We'll add an *Awards* column by adding a new grouping to the *positions* column set.

Code Sample
-----------

This code is similar to :doc:`the Grouping by Objects example <grouping-objects>` except for the *awards* column set added to the *positions* column set.

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
    rows = renderer.render(data)

    print(list(rows))

Result
------

.. testoutput::
   :options: +NORMALIZE_WHITESPACE

    [['Name',              'Email',              'Year', 'Title',           'Award'],
     ['Robert Pringles',   'bob@pringles.pop',     2008, 'Founder',         'Best Product 2008'],
     ['Robert Pringles',   'bob@pringles.pop',     2008, 'Founder',         'Founder of the Year'],
     ['Robert Pringles',   'bob@pringles.pop',     2009, 'CEO',             'Fastest Doughnut Run'],
     ['Robert Pringles',   'bob@pringles.pop',     2009, 'CEO',             'Tie of the Year'],
     ['Daniel Sausage',    'danny@pringles.pop',   2010, 'Head Chef',       'Salad of the Century'],
     ['Daniel Sausage',    'danny@pringles.pop',   2010, 'Head Chef',       'Soup of the Week'],
     ['Daniel Sausage',    'danny@pringles.pop',   2010, 'Head Chef',       'Sandwich of the Decade'],
     ['Charlie Marmalade', 'charlie@pringles.pop', 2009, 'Engineer',        'Engineer of the Month'],
     ['Charlie Marmalade', 'charlie@pringles.pop', 2009, 'Engineer',        'Least Security Vulnerabilities 2009'],
     ['Charlie Marmalade', 'charlie@pringles.pop', 2010, 'Senior Engineer', 'Best Code Reviews'],
     ['Charlie Marmalade', 'charlie@pringles.pop', 2010, 'Senior Engineer', 'Support Champion 2010'],
     ['Charlie Marmalade', 'charlie@pringles.pop', 2011, 'CTO',             'Cloud Uplift of the Century'],
     ['Charlie Marmalade', 'charlie@pringles.pop', 2011, 'CTO',             'Worst Tie 2011']]
