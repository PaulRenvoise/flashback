from itertools import islice

from ..sentinel import Sentinel


def renumerate(iterable):
    """
    Enumerates an `iterable` starting from the end.

    Examples:
        ```python
        from flashback.iterating import renumerate

        # Drop-in replacement for enumerate()
        lst = ['a', 'b', 'c']
        for index, item in renumerate(lst):
            print(index, item)
        #=> 2 'c'
        #=> 1 'b'
        #=> 0 'a'

        # Still returns an iterator
        iter = renumerate(lst)
        assert next(iter) == (2, 'c')
        ```

    Params:
        - `iterable (Iterable<Any>)` the list to reverse and enumerate

    Returns:
        - `Iterator` the iterator containing the reversed enumeration
    """
    return zip(range(len(iterable) - 1, -1, -1), reversed(iterable))


def chunks(iterable, size=2, pad=Sentinel):
    """
    Iterates over an `iterable` by chunks of `size`.

    Handles in

    Examples:
        ```python
        from itertools import count
        from flashback.iterating import chunks

        # Handles iterables
        for chunk in chunks([1, 2, 3, 4]):
            print(sum(chunk))
        #=> 3
        #=> 7

        # And infinite ones as well
        for chunk in chunks(counter(), size=5):
            print(sum(chunk))
        #=> 15
        #=> 40
        #=> 65
        #=> 90
        #=> ...
        ```

    Params:
        - `iterable (Iterable<Any>)` the iterable to chunk
        - `size (int)` the size of the chunks to produce

    Yields:
        - `tuple<Any>` the extracted chunk
    """
    iterable = iter(iterable)
    chunk_generator = iter(lambda: tuple(islice(iterable, size)), ())
    if pad is Sentinel:
        yield from chunk_generator
    else:
        for chunk in chunk_generator:
            len_diff = size - len(chunk)
            if len_diff > 0:
                chunk += (pad,) * len_diff

            yield chunk


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
        - `predicate (lambda)` the lambda to apply on each item of `iterable`
        - `iterable (Iterable<Any>)` the iterable to partition

    Returns:
        - `tuple<tuple<Any>>` the iterable's items separated depending on `predicate`
    """
    trues = []
    falses = []

    for item in iterable:
        if predicate(item):
            trues.append(item)
        else:
            falses.append(item)

    return (tuple(trues), tuple(falses))
