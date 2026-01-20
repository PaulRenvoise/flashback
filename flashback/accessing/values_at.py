from collections.abc import Hashable, Mapping
import typing as t


def values_at[T](mapping: Mapping[t.Any, T], *keys: Hashable) -> list[T]:
    """
    Retrieves the values corresponding to each `keys` in `mapping`.

    Examples:
        ```python
        from flashback.accessing import values_at

        # Without values_at
        values = [mapping[k] for k in ["key1", "key2"] if k in mapping]

        # With values_at
        values = values_at(mapping, "key1", "key2")
        ```

    Params:
        mapping: the dict to fetch the values from
        keys: the keys to get the data with

    Returns:
        the fetched values
    """
    return [mapping[k] for k in keys if k in mapping]
