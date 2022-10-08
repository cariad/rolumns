from datetime import datetime
from typing import Any

from dateutil import parser

from rolumns.translators.translator import Translator


class ToDateTime(Translator[datetime]):
    def try_translate(self, value: Any) -> datetime:
        return parser.parse(value)
