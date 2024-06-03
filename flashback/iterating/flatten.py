from __future__ import annotations

from typing import TypeVar

T = TypeVar("T")


def flatten(iterable: list[T] | tuple[T, ...] | set[T] | frozenset[T] | range) -> tuple[T, ...]:
    """
    Unpacks nested iterables into the root `iterable`.

    Examples:
        ```python
        from flashback.iterating import flatten

        for item in flatten(["a", ["b", ["c", "d"]], "e"]):
            print(item)
        #=> "a"
        #=> "b"
        #=> "c"
        #=> "d"
        #=> "e"

        assert flatten([1, {2, 3}, (4,), range(5, 6)]) == (1, 2, 3, 4, 5)
        ```

    Params:
        iterable: the iterable to flatten

    Returns:
        the flattened iterable
    """
    items = []
    for item in iterable:
        if isinstance(item, (list, tuple, set, frozenset, range)):  # noqa: UP038
            for nested_item in flatten(item):
                items.append(nested_item)  # noqa: PERF402
        else:
            items.append(item)

    return tuple(items)
