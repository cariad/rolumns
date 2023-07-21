from pytest import raises

from rolumns.exceptions import TranslationFailed
from rolumns.source import Source
from rolumns.translation_state import TranslationState


def test_fail() -> None:
    def fail(state: TranslationState) -> str:
        raise Exception("failed")

    source = Source(path="date", translator=fail)

    with raises(TranslationFailed) as ex:
        list(source.read({"date": "pringles"}))

    expect = "Failed to translate 'pringles' (failed)"
    assert str(ex.value) == expect
