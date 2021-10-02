def renumerate(iterable):
    """
    Enumerates an `iterable` starting from the end.

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
        iterable (Iterable<Any>): the list to reverse and enumerate

    Returns:
        Iterator: the iterator containing the reversed enumeration
    """
    return zip(range(len(iterable) - 1, -1, -1), reversed(iterable))
