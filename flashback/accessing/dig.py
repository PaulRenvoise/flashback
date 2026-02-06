from collections.abc import Hashable
import typing as t


class SupportsGetItem(t.Protocol):
    def __getitem__(self: "SupportsGetItem", key: t.Any, /) -> t.Any:
        pass


def dig(container: SupportsGetItem, /, *keys: Hashable) -> t.Any | None:
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

    current = container

    for key in keys[:-1]:
        try:
            current = current[key] or {}
        except (KeyError, IndexError):
            current = {}

    last_key = keys[-1]
    try:
        return current[last_key]
    except (KeyError, IndexError):
        return None
