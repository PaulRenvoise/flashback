from __future__ import annotations

from typing import Any


def pick(dictionary: dict[Any, Any], *keys: tuple[Any]) -> dict[Any, Any]:
    """
    Fetches key/value pairs from `dictionary` corresponding to `keys`.

    Examples:
        ```python
        from flashback.accessing import pick

        # Without pick
        dictionary_2 = {k: dictionary[k] for k in ["key1", "key2"] if k in dictionary}

        # With pick
        dictionary_2 = pick(dictionary, "key1", "key2")
        ```

    Params:
        dictionary: the dict to fetch the key/value pairs from
        keys: the keys to get the key/value pairs with

    Returns:
        the dict built from fetched key/value pairs
    """
    return {k: dictionary[k] for k in keys if k in dictionary}
