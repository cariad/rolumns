from inspect import isgenerator
from json import dumps
from logging import DEBUG, getLogger
from typing import Any

logger = getLogger("rolumns")


def dump(obj: Any) -> str:
    if isgenerator(obj):
        result = "["
        for index, value in enumerate(obj):
            result += f"\n {index}. {dump(value)}"
        return result + "\n]"

    return dumps(obj, indent=2, sort_keys=True)


def is_debug() -> bool:
    return logger.getEffectiveLevel() == DEBUG
