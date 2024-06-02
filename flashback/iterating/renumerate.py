from __future__ import annotations

from collections.abc import Sized, Reversible
from typing import Protocol, TypeVar

T_co = TypeVar("T_co", covariant=True)


class SizedReversible(Protocol[T_co], Sized, Reversible):
    pass


def renumerate(iterable: SizedReversible) -> zip:
    """
    Enumerates an `iterable` starting from the end.

    Examples:
        ```python
        from flashback.iterating import renumerate

        # Drop-in replacement for enumerate()
        lst = ["a", "b", "c"]
        for index, item in renumerate(lst):
            print(index, item)
        #=> 2 "c"
        #=> 1 "b"
        #=> 0 "a"

        # Still returns an iterator
        iter = renumerate(lst)
        assert next(iter) == (2, "c")
        ```

    Params:
        iterable: the list to reverse and enumerate

    Returns:
        the iterator containing the reversed enumeration
    """
    return zip(range(len(iterable) - 1, -1, -1), reversed(iterable))
