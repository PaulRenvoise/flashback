def partition(predicate, iterable):
    """
    Splits an `iterable` into two lists containing items that validate or not the given
    `predicate`.

    Items that validated the predicate are first in the returned tuple.

    Examples:
        ```python
        from flashback.iterating import partitions

        evens, odds = partition(lambda x: x % 2, [1, 2, 3, 4, 5])

        assert evens == [2, 4]
        assert odds == [1, 3, 5]
        ```

    Params:
        predicate (lambda): the lambda to apply on each item of `iterable`
        iterable (Iterable<Any>): the iterable to partition

    Returns:
        tuple<tuple<Any>>: the iterable's items separated depending on `predicate`
    """
    trues = []
    falses = []

    for item in iterable:
        if predicate(item):
            trues.append(item)
        else:
            falses.append(item)

    return (tuple(trues), tuple(falses))
