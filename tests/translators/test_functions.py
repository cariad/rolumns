from datetime import datetime, timezone
from typing import Optional

from pytest import mark, raises

from rolumns.translators import TranslationState, to_censored_string, to_datetime


@mark.parametrize(
    "value, expect",
    [
        (None, ""),
        ("", ""),
        ("a", "*"),
        ("ab", "**"),
        ("abc", "a*c"),
        ("abcd", "a**d"),
    ],
)
def test_to_censored_string(value: Optional[str], expect: str) -> None:
    assert to_censored_string(TranslationState(value=value)) == expect


def test_to_datetime() -> None:
    expect = datetime(1992, 3, 7, 13, 14, 15, tzinfo=timezone.utc)
    assert to_datetime(TranslationState(value="19920307T131415Z")) == expect


def test_to_datetime__fail() -> None:
    with raises(Exception):
        assert to_datetime(TranslationState(value="pringles"))

    # We truly don't care which exception was raised or what its message is.
