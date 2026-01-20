from collections.abc import Sequence, Hashable, Mapping
import typing as t


def dig(container: Mapping[t.Any, t.Any] | Sequence[t.Any], *keys: Hashable) -> t.Any | None:
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
    if not keys:
        return None

    current: t.Any = container

    for key in keys[:-1]:
        if isinstance(current, Sequence) and isinstance(key, int):
            if 0 <= key < len(current):
                current = current[key] or {}
            else:
                current = {}
        else:
            current = current.get(key, {}) or {}

    last_key = keys[-1]
    if isinstance(current, Sequence) and isinstance(last_key, int):
        return current[last_key] if 0 <= last_key < len(current) else None

    return current.get(last_key)
