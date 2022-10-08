from typing import Any, List

from pytest import mark

from rolumns.data_resolver import DataResolver


@mark.parametrize(
    "data, path, expect",
    [
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
