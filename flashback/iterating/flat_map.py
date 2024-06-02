from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import TypeVar

from .flatten import flatten

T = TypeVar("T")
U = TypeVar("U")


def flat_map(func: Callable[[T], U], iterable: Iterable[T]) -> map[U]:
    """
    Applies the function `func` to each item and nested item of `iterable`.

    Examples:
        ```python
        from flashback.iterating import flat_map

        for item in flat_map(lambda x: x * 2, [1, [2, [3, 4]], 5]):
            print(item)
        #=> 2
        #=> 4
        #=> 6
        #=> 8
        #=> 10

        assert list(flat_map(lambda x: x / 2, [1, {2, 3}, (4,), range(5, 6)]) == [0.5, 1, 1.5, 2, 2.5, 3]
        ```

    Params:
        func: the callable to apply on each item of the iterable
        iterable: the iterable to flatten and map

    Returns:
        the flattened and mapped iterable
    """
    flattened_iterable = flatten(iterable)

    return map(func, flattened_iterable)
