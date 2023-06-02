from typing import Any, List

from pytest import mark, raises

from rolumns.data_resolver import DataResolver


@mark.parametrize(
    "data, path, expect",
    [
        (
            {},
            "name",
            [
                None,
            ],  # There is no "name" in {}.
        ),
        (
            [
                {},
                {},
            ],
            "name",
            [
                None,
                None,
            ],  # There is no "name" in {}.
        ),
        (
            {
                "name": "alice",
            },
            "name",
            [
                "alice",
            ],
        ),
        (
            [
                {
                    "name": "alice",
                },
                {
                    "name": "bob",
                },
            ],
            "name",
            [
                "alice",
                "bob",
            ],
        ),
        (
            {
                "address": {
                    "planet": "Earth",
                },
            },
            "address.planet",
            [
                "Earth",
            ],
        ),
        (
            {
                "addresses": {
                    "current": {
                        "planet": "Earth",
                    },
                },
            },
            "addresses.current.planet",
            [
                "Earth",
            ],
        ),
    ],
)
def test(data: Any, path: str, expect: List[Any]) -> None:
    assert list(DataResolver(data).resolve(path)) == expect


def test_resolve__type_error() -> None:
    with raises(TypeError) as ex:
        list(DataResolver("pringles").resolve("bob"))

    assert str(ex.value) == "string indices must be integers"
