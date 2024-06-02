from __future__ import annotations

from collections.abc import Iterable, Generator
from itertools import islice
from typing import Any, TypeVar

from ..sentinel import Sentinel

T = TypeVar("T")


def chunks(iterable: Iterable[T], size: int = 2, pad: Any = Sentinel) -> Generator[tuple[T, ...], None, None]:
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
        iterable: the iterable to chunk
        size: the size of the chunks to produce

    Yields:
        the extracted chunk
    """
    iterable = iter(iterable)
    chunk_generator = iter(lambda: tuple(islice(iterable, size)), ())
    if pad is Sentinel:
        yield from chunk_generator
    else:
        for chunk in chunk_generator:
            len_diff = size - len(chunk)
            if len_diff > 0:
                yield chunk + (pad,) * len_diff
            else:
                yield chunk
