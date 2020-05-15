def compact(iterable):
    """
    Removes None items from `iterable`.

    Params:
        - `iterable (Iterable<Any>)` the iterable to remove None from

    Returns:
        - `tuple<Any>` the iterable without duplicates
    """
    return tuple(item for item in iterable if item is not None)
