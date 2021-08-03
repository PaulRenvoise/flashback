import inspect
import functools
import logging

from .cache import Cache


def cached(adapter="memory", **kwargs):
    """
    Caches the return of a callable under a type-aware key built with its arguments.

    Relies on the key building mechanism from `functools._make_key`.

    Examples:
        ```python
        from flashback.caching import cached

        @cached()
        def func(a, b):
            return a + b

        func(1, 2)
        #=> Cache miss
        #=> 3

        # The cache key is typed
        func("1", "2")
        #=> Cache miss
        #=> "12"

        # The cache key takes in account the arguments' order as well
        func(2, 1)
        #=> Cache miss
        #=> 3

        func(1, 2)
        #=> Cache hit
        #=> 3
        ```

    Params:
        adapter (str): the cache storage adapter to use
        kwargs (dict): every keyword argument, forwarded to the cache adapter

    Returns:
        Callable: a wrapper used to decorate a callable
    """
    cache = Cache(adapter, **kwargs)

    def wrapper(func):
        # `.getmodule().__name__` returns the same value as `__name__` called from the module we
        # decorate.
        # Since `logging` is a singleton, everytime we call `logging.getLogger()` with the same
        # name, we receive the same logger, which "hides" this decorator as if the logging was
        # made from within the callable we decorate
        logger = logging.getLogger(inspect.getmodule(func).__name__)

        @functools.wraps(func)
        def inner(*args, **kwargs):
            key = functools._make_key(args, kwargs, True)  # pylint: disable=protected-access
            value = cache.get(key)

            if value is not None:
                logger.debug("Cache hit")

                return value

            logger.debug("Cache miss")

            value = func(*args, **kwargs)
            cache.set(key, value)

            return value

        return inner

    return wrapper
