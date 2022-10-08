"""
**Rolumns** is a Python package for squishing data into rows and columns.
"""

from importlib.resources import open_text

from rolumns.columns import Columns

with open_text(__package__, "VERSION") as t:
    __version__ = t.readline().strip()

__all__ = [
    "Columns",
]
