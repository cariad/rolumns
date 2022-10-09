from datetime import datetime

from dateutil import parser

from rolumns.translators.translation_state import TranslationState


def to_censored_string(state: TranslationState) -> str:
    """
    Translates a value to a censored string.
    """

    value = str("" if state.value is None else state.value)

    if len(value) < 3:
        return "".join(["*" * len(value)])

    return value[0] + "".join(["*" * (len(value) - 2)]) + value[-1]


def to_datetime(state: TranslationState) -> datetime:
    """
    Translates a value to a `datetime`.
    """

    return parser.parse(state.value)
