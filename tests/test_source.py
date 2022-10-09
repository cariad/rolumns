from pytest import raises

from rolumns.exceptions import TranslationFailed
from rolumns.source import Source
from rolumns.translators import to_datetime


def test_fail() -> None:
    source = Source("date", translator=to_datetime)

    with raises(TranslationFailed) as ex:
        list(source.read({"date": "pringles"}))

    expect = "Failed to translate 'pringles' (Unknown string format: pringles)"
    assert str(ex.value) == expect
