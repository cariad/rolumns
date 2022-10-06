from json import load
from pathlib import Path
from typing import Any, Literal, Tuple, Union

Raison = Union[Literal["expect"], Literal["input"]]


def load_data(test_case: int, raison: Raison) -> Any:
    data = Path("tests") / "data"
    with open(data / f"{test_case:04}-{raison}.json") as f:
        return load(f)


def load_test_case(id: int) -> Tuple[Any, Any]:
    return (load_data(id, "input"), load_data(id, "expect"))


__all__ = [
    "load_test_case",
]
