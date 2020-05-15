def uniq(iterable):
    """
    Removes duplicates items from `iterable` while respecting their apparition order.

    Params:
        - `iterable (Iterable<Any>)` the iterable to remove duplicates from

    Returns:
        - `tuple<Any>` the iterable without duplicates
    """
    unique = []
    seen = set()

    for item in iterable:
        if item in seen:
            continue

        unique.append(item)
        seen.add(item)

    return tuple(unique)
