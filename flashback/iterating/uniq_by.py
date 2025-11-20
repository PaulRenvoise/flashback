from collections.abc import Callable, Iterable
import typing as t


def uniq_by[T](func: Callable[[T], t.Any], iterable: Iterable[T]) -> list[T]:
    """
    Removes duplicates items from `iterable` based on a callable `func`, while keeping their order.

    Examples:
        ```python
        from flashback.iterating import uniq_by

        # Remove duplicates based on the values themselves
        for user_id in uniq_by([1058, 1058, 85, 9264, 19475, 85], lambda x: x):
            print(user_id)
        #=> 1058
        #=> 85
        #=> 9264
        #=> 19475

        # Remove duplicates based on the length of the string
        for item in uniq_by(["a", "ab", "abc", "abcd", "xyz", "pqrs"], len):
            print(item)
        #=> "a"
        #=> "ab"
        #=> "abc"
        #=> "abcd"
        ```

    Params:
        iterable: the iterable to remove duplicates from
        func: the callable to determine the uniqueness of each item

    Returns:
        the iterable without duplicates based on the result of the given func
    """
    unique = []
    seen = set()

    for item in iterable:
        item_repr = repr(func(item))
        if item_repr in seen:
            continue

        unique.append(item)
        seen.add(item_repr)

    return unique
