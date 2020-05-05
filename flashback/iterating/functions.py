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
        - `iterable (Iterable)` the list to reverse and enumerate

    Returns:
        - `zip` the generator containing the reversed enumeration
    """
    return zip(range(len(iterable) - 1, -1, -1), reversed(iterable))


def chunks(iterable, size=2, pad=Sentinel):
    """
    Iterates over an `iterable` by chunks of `size`.

    Examples:
        ```python
        from flashback.iterating import chunks

        for chunk in chunks([1, 2, 3, 4], size=2):
            print(sum(chunk))
        #=> 3
        #=> 7
        ```

    Params:
        - `iterable (Iterable)` the iterable to chunk
        - `size (int)` the size of the chunks to produce

    Returns:
        - `generator` the generator containing the chunks
    """
    chunk_generator = (iterable[index:index + size] for index in range(0, len(iterable), size))
    if pad is Sentinel:
        yield from chunk_generator
    else:
        for chunk in chunk_generator:
            len_diff = size - len(chunk)
            if len_diff > 0:
                chunk += (pad,) * len_diff

            yield chunk
