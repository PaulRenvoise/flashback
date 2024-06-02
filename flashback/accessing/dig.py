from __future__ import annotations

from collections.abc import Sequence, Hashable
from typing import TypeVar

T = TypeVar("T")


def dig(container: dict[Hashable, T] | Sequence[T], *keys: tuple[Hashable, ...]) -> T | None:
    """
    Retrieves the value corresponding to each `keys` repeatedly from `container`,
    supporting both dict and list indices.

    Examples:
        ```python
        from flashback.accessing import dig

        # Without dig
        dictionary.get("key1", {}).get("key2", {})[0].get("key3")

        # With dig
        dig(dictionary, "key1", "key2", 0, "key3")
        ```

    Params:
        dictionary: the dict or list to fetch the value from
        keys: the consecutive keys or indices to access

    Returns:
        the final value
    """
    for key in keys[:-1]:
        if isinstance(container, Sequence) and isinstance(key, int):
            if 0 <= key < len(container):
                container = container[key] or []
            else:
                container = [{}]
        else:
            container = container.get(key, {}) or {}

    last_key = keys[-1]
    if isinstance(container, Sequence) and isinstance(last_key, int):
        return container[last_key] if 0 <= last_key < len(container) else None

    return container.get(last_key)
