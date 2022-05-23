def dig(dictionary, *keys):
    """
    Retrieves the value corresponding to each `keys` repeatedly from `dictionary`.

    Examples:
        ```python
        from flashback.accessing import dig

        # Without dig
        dictionary.get("key1", {}).get("key2", {}).get("key3")

        # With dig
        dig(dictionary, "key1", "key2", "key3")
        ```

    Params:
        dictionary (dict): the dict to fetch the value from
        keys (tuple<str>): the consecutive keys to access

    Returns:
        Any|None: the final value
    """
    for key in keys[:-1]:
        # Handles when key does not exist
        # and when value is None
        dictionary = dictionary.get(key, {}) or {}

    return dictionary.get(keys[-1])
