from datetime import datetime, timezone

from pytest import raises

from rolumns.exceptions import TranslationFailed
from rolumns.translators import ToDateTime


def test() -> None:
    expect = datetime(1992, 3, 7, 13, 14, 15, tzinfo=timezone.utc)
    assert ToDateTime().translate("19920307T131415Z") == expect


def test_fail() -> None:
    with raises(TranslationFailed) as ex:
        assert ToDateTime().translate("pringles")

    expect = "Failed to translate 'pringles' (Unknown string format: pringles)"
    assert str(ex.value) == expect
