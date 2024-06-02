from typing import Any


def values_at(dictionary: dict[Any, Any], *keys: tuple[Any]) -> list[Any]:
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
