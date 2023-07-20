"""
Rolumns is a Python package for squishing data into rows and columns.

Full documentation is online at https://rolumns.dev.
"""

from importlib.resources import open_text

from rolumns.by_path import ByPath
from rolumns.columns import Columns
from rolumns.data_navigator import DataNavigator
from rolumns.groups import ByKey
from rolumns.source import Source
from rolumns.translation_state import TranslationState

with open_text(__package__, "VERSION") as t:
    __version__ = t.readline().strip()

__all__ = [
    "ByKey",
    "ByPath",
    "Columns",
    "DataNavigator",
    "Source",
    "TranslationState",
]
