def flatten(iterable):
    """
    Unpacks nested iterables into the root `iterable`.

    Examples:
        ```python
        from flashback.iterating import flatten

        for item in flatten(["a", ["b", ["c", "d"]], "e"]):
            print(item)
        #=> "a"
        #=> "b"
        #=> "c"
        #=> "d"
        #=> "e"

        assert flatten([1, {2, 3}, (4,), range(5, 6)]) == (1, 2, 3, 4, 5)
        ```

    Params:
        iterable (Iterable<Any>): the iterable to flatten

    Returns:
        tuple<Any>: the flattened iterable
    """
    items = []
    for item in iterable:
        if isinstance(item, (list, tuple, set, frozenset, range)):
            for nested_item in flatten(item):
                items.append(nested_item)
        else:
            items.append(item)

    return tuple(items)
