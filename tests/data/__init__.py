from json import load
from pathlib import Path
from typing import Any, Literal, Optional, Tuple, Union

Raison = Union[Literal["expect"], Literal["input"]]


def load_data(test_case: int, raison: Raison, variant: Optional[str] = None) -> Any:
    data = Path("tests") / "data"
    variant = f"-{variant}" if variant else ""
    with open(data / f"{test_case:04}-{raison}{variant}.json") as f:
        return load(f)


def load_test_case(id: int, expect_variant: Optional[str] = None) -> Tuple[Any, Any]:
    return (
        load_data(id, "input"),
        load_data(id, "expect", variant=expect_variant),
    )


__all__ = [
    "load_test_case",
]
