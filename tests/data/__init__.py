from json import load
from pathlib import Path
from typing import Any, Literal, Optional, Tuple, Union

Raison = Union[Literal["expect"], Literal["input"]]
Format = Union[Literal["json"], Literal["md"]]


def load_data(
    test_case: int,
    raison: Raison,
    format: Optional[Format] = None,
    variant: Optional[str] = None,
) -> Any:
    data = Path("tests") / "data"
    format = format or "json"
    variant = f"-{variant}" if variant else ""
    with open(data / f"{test_case:04}-{raison}{variant}.{format}") as f:
        if format == "json":
            return load(f)
        return [r.rstrip() for r in f.readlines()]


def load_test_case(
    id: int,
    expect_format: Optional[Format] = None,
    expect_variant: Optional[str] = None,
) -> Tuple[Any, Any]:
    return (
        load_data(id, "input"),
        load_data(id, "expect", format=expect_format, variant=expect_variant),
    )


__all__ = [
    "load_test_case",
]
