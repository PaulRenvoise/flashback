from __future__ import annotations

from collections.abc import Iterable


def oxford_join(
    iterable: Iterable[str],
    sep: str = ", ",
    couple_sep: str = " and ",
    last_sep: str = ", and ",
    quotes: bool = False,
) -> str:
    """
    Joins a list of string to a comma-separated sentence in a more english fashion than the
    builtin `.join()`.

    Examples:
        ```python
        from flashback.formatting import oxford_join

        oxford_join("A", "B")
        #=> "A and B"

        oxford_join("A", "B", "C")
        #=> "A, B, and C"

        oxford_join("A", "B", "C", last_sep=", or ")
        #=> "A, B, or C"
        ```

    Params:
        iterable: the sequence holding the items to join
        sep: the separator used when there is more than two items in the iterable
        couple_sep: the separator to use if there is only two items in the iterable
        last_sep: the separator to use for the last two items of the iterable
        quotes: whether or not to add quotes around each item of the iterable

    Returns:
        str: the joined strings
    """
    if not iterable:
        return ""

    if quotes:
        iterable = [f'"{item}"' for item in iterable]
    else:
        iterable = [str(item) for item in iterable]

    if len(iterable) == 1:
        return iterable[0]

    if len(iterable) == 2:
        return couple_sep.join(iterable)

    enumeration = sep.join(iterable[:-1])

    return f"{enumeration}{last_sep}{iterable[-1]}"
