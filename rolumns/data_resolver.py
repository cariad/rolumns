from typing import Any, Iterable, List, Optional

from rolumns.logging import logger, missing_value_logger


class DataResolver:
    """
    Data resolver.

    `root` is the root data object to resolve into. It can represent a single
    record or be iterable.
    """

    def __init__(self, root: Any) -> None:
        if isinstance(root, list):
            self._root: List[Any] = root
        else:
            self._root = [root]

    @staticmethod
    def _resolve(parts: List[str], data: Any) -> Iterable[Optional[Any]]:
        if data is None:
            logger.warning(
                "Cannot use %s as indices of None, so yielding None",
                parts,
            )

            yield None
            return

        if isinstance(data, list):
            for d in data:
                for r in DataResolver._resolve(parts.copy(), d):
                    yield r

        else:
            part = parts.pop()

            try:
                data = data[part]

            except KeyError:
                missing_value_logger.warning(
                    'No "%s" in %s',
                    part,
                    data,
                )

                yield None
                return

            except TypeError as ex:
                missing_value_logger.warning(
                    'Cannot use "%s" as index of %s (%s)',
                    part,
                    data,
                    ex,
                )

                raise

            if not parts:
                # This is the leaf, so there better be something to read!
                yield data
            else:
                for r in DataResolver._resolve(parts.copy(), data):
                    yield r

    def resolve(self, path: Optional[str]) -> Iterable[Any]:
        if path:
            parts = path.split(".")
            parts.reverse()

            for r in self._resolve(parts.copy(), self._root):
                yield r
        else:
            for datum in self._root:
                yield datum
