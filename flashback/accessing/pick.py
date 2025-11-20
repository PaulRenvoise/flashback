from collections.abc import Hashable, Mapping
import typing as t


def pick[T](mapping: Mapping[t.Any, T], *keys: Hashable) -> dict[Hashable, T]:
    """
    Fetches key/value pairs from `mapping` corresponding to `keys`.

    Examples:
        ```python
        from flashback.accessing import pick

        # Without pick
        mapping_2 = {k: mapping[k] for k in ["key1", "key2"] if k in mapping}

        # With pick
        mapping_2 = pick(mapping, "key1", "key2")
        ```

    Params:
        mapping: the dict to fetch the key/value pairs from
        keys: the keys to get the key/value pairs with

    Returns:
        the dict built from fetched key/value pairs
    """
    return {k: mapping[k] for k in keys if k in mapping}
