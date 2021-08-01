from itertools import islice

from ..sentinel import Sentinel


def chunks(iterable, size=2, pad=Sentinel):
    """
    Iterates over an `iterable` by chunks of `size`.

    Handles infinite iterables.

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
        iterable (Iterable<Any>): the iterable to chunk
        size (int): the size of the chunks to produce

    Yields:
        tuple<Any>: the extracted chunk
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
