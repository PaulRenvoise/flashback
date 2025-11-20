from collections.abc import Iterable


def uniq[T](iterable: Iterable[T]) -> list[T]:
    """
    Removes duplicates items from `iterable` while keeping their order.

    Examples:
        ```python
        from flashback.iterating import uniq

        for user_id in uniq([1058, 1058, 85, 9264, 19475, 85]):
            print(user_id)
        #=> 1058
        #=> 85
        #=> 9264
        #=> 19475

        # Keeps order
        assert list(set([1, 1, 3, 4, 5, 5])) != uniq([1, 1, 3, 4, 5, 5])
        ```

    Params:
        iterable: the iterable to remove duplicates from

    Returns:
        the iterable without duplicates
    """
    unique = []
    seen = set()

    for item in iterable:
        item_repr = repr(item)
        if item_repr in seen:
            continue

        unique.append(item)
        seen.add(item_repr)

    return unique
