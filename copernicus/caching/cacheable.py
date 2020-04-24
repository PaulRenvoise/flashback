import inspect
import functools
import logging

from .cache import Cache


def cacheable(adapter='memory', **kwargs):
    """
    Caches the return of a callable under a type-aware key built with its arguments.

    Relies on the key building mechanism from `functools._make_key`.

    Examples:
        ```
        from copernicus.caching import cacheable

        @cacheable()
        def func(a, b):
            return a + b

        func(1, 2)
        #=> Cache miss
        #=> 3

        # The key is type
        func('1', '2')
        #=> Cache miss
        #=> '12'

        # The key takes in account the arguments' order as well
        func(2, 1)
        #=> Cache miss
        #=> 3

        func(1, 2)
        #=> Cache hit
        #=> 3
        ```

    Params:
        - `adapter (str)` the cache storage adapter to use
        - `kwargs (dict)` every keyword argument, forwarded to the cache adapter

    Returns:
        - `Callable` a wrapper used to decorate a callable
    """
    cache = Cache(adapter, **kwargs)

    def wrapper(func):
        # `.getmodule().__name__` returns the same value as `__name__` called from the module we decorate
        # Each time we call `getLogger()` with the same name, we receive the same logger since `logging` is a singleton
        # This "pretends" the logging was made from within the module/function we decorate
        logger = logging.getLogger(inspect.getmodule(func).__name__)

        @functools.wraps(func)
        def inner(*args, **kwargs):
            key = functools._make_key(args, kwargs, True)  # pylint: disable=protected-access
            value = cache.get(key)

            if value is not None:
                logger.debug('Cache hit')

                return value

            logger.debug('Cache miss')

            value = func(*args, **kwargs)
            cache.set(key, value)

            return value

        return inner

    return wrapper
