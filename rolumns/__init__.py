"""
Rolumns is a Python package for squishing data into rows and columns.

Full documentation is online at https://rolumns.dev.
"""

from importlib.resources import open_text

from rolumns.by_key import ByKey
from rolumns.by_path import ByPath
from rolumns.by_user_defined_fields import ByUserDefinedFields, UserDefinedField
from rolumns.columns import Columns
from rolumns.cursor import Cursor
from rolumns.group import Group
from rolumns.source import Source
from rolumns.translation_state import TranslationState

with open_text(__package__, "VERSION") as t:
    __version__ = t.readline().strip()

__all__ = [
    "ByKey",
    "ByPath",
    "ByUserDefinedFields",
    "Columns",
    "Cursor",
    "Group",
    "Source",
    "TranslationState",
    "UserDefinedField",
]
