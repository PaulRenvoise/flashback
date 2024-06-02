from __future__ import annotations

from collections.abc import Hashable
from typing import TypeVar

T = TypeVar("T")


def values_at(dictionary: dict[Hashable, T], *keys: tuple[Hashable, ...]) -> list[T]:
    """
    Retrieves the values corresponding to each `keys` in `dictionary`.

    Examples:
        ```python
        from flashback.accessing import values_at

        # Without values_at
        values = [dictionary[k] for k in ["key1", "key2"] if k in dictionary]

        # With values_at
        values = values_at(dictionary, "key1", "key2")
        ```

    Params:
        dictionary: the dict to fetch the values from
        keys: the keys to get the data with

    Returns:
        the fetched values
    """
    return [dictionary[k] for k in keys if k in dictionary]
