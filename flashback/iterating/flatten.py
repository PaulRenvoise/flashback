from collections.abc import Iterable
import typing as t

type Flattenable[T] = (
    T | list[Flattenable[T]] | tuple[Flattenable[T], ...] | set[Flattenable[T]] | frozenset[Flattenable[T]]
)


@t.overload
def flatten[T](iterable: Iterable[Flattenable[T]]) -> list[T]: ...


@t.overload
def flatten[T](iterable: Iterable[Flattenable[T] | range]) -> list[T | int]: ...


def flatten(iterable: Iterable[t.Any]) -> list[t.Any]:
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

        assert flatten([1, {2, 3}, (4,), range(5, 6)]) == [1, 2, 3, 4, 5]
        ```

    Params:
        iterable: the iterable to flatten

    Returns:
        the flattened iterable
    """
    items: list[t.Any] = []

    for item in iterable:
        if isinstance(item, range):
            items.extend(item)
        elif isinstance(item, (list, tuple, set, frozenset)):
            items.extend(flatten(item))
        else:
            items.append(item)

    return items
