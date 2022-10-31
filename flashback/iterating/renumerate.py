from typing import Any, Sequence


def renumerate(sequence: Sequence[Any]) -> zip:
    """
    Enumerates an `sequence` starting from the end.

    Examples:
        ```python
        from flashback.iterating import renumerate

        # Drop-in replacement for enumerate()
        lst = ["a", "b", "c"]
        for index, item in renumerate(lst):
            print(index, item)
        #=> 2 "c"
        #=> 1 "b"
        #=> 0 "a"

        # Still returns an iterator
        iter = renumerate(lst)
        assert next(iter) == (2, "c")
        ```

    Params:
        sequence: the list to reverse and enumerate

    Returns:
        the iterator containing the reversed enumeration
    """
    return zip(range(len(sequence) - 1, -1, -1), reversed(sequence))
