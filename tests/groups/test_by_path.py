from typing import Optional

from pytest import mark

from rolumns.groups import ByPath


@mark.parametrize(
    "path, expect",
    [
        (None, 'ByPath("")'),
        ("foo", 'ByPath("foo")'),
    ],
)
def test_str(path: Optional[str], expect: str) -> None:
    assert str(ByPath(path)) == expect
