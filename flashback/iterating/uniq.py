from __future__ import annotations

from collections.abc import Iterable

from typing import TypeVar

T = TypeVar("T")


def uniq(iterable: Iterable[T]) -> tuple[T, ...]:
    """
    Removes duplicates items from `iterable` while keeping their order.

    Examples:
        ```python
        from flashback.iterating import uniq

        for user_id in uniq([1058, 1058, 85, 9264, 19475, 85]):
            print(user_id)
        #=> 1058
        #=> 85
        #=> 9264
        #=> 19475

        # Keeps order
        assert set([1, 1, 3, 4, 5, 5]) != uniq([1, 1, 3, 4, 5, 5])
        ```

    Params:
        iterable: the iterable to remove duplicates from

    Returns:
        the iterable without duplicates
    """
    unique = []
    seen = set()

    for item in iterable:
        repr_item = repr(item)
        if repr_item in seen:
            continue

        unique.append(item)
        seen.add(repr_item)

    return tuple(unique)
