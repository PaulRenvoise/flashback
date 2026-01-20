from collections.abc import Callable
import functools
import hashlib
import inspect
import logging
import typing as t

from .cache import Cache


def cached(adapter: str = "memory", hash_keys: bool = False, **kwargs) -> Callable[..., Callable[..., t.Any]]:
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
        adapter: the cache storage adapter to use
        kwargs: every keyword argument, forwarded to the cache adapter

    Returns:
        a wrapper used to decorate a callable
    """
    cache = Cache(adapter, **kwargs)

    def _build_key(func: Callable[..., t.Any], *args, **kwargs) -> str:
        name = getattr(func, "__qualname__", getattr(func, "__name__", repr(func)))

        def _format_argument(v: t.Any) -> str:
            return f"{v!r}<{type(v).__name__}>"

        positional = [_format_argument(a) for a in args]
        keyword = [f"{k}={_format_argument(v)}" for k, v in sorted(kwargs.items())]

        if positional and keyword:
            inner = ", ".join([*positional, "*", *keyword])
        elif positional:
            inner = ", ".join(positional)
        else:
            inner = ", ".join(keyword)

        return f"{name}({inner})"

    if hash_keys:

        def _make_key(func, *args, **kwargs) -> str:
            key = _build_key(func, *args, **kwargs)
            return hashlib.md5(key.encode()).hexdigest()
    else:

        def _make_key(func, *args, **kwargs) -> str:
            return _build_key(func, *args, **kwargs)

    def wrapper(func: Callable[..., t.Any]) -> Callable[..., t.Any]:
        # `.getmodule().__name__` returns the same value as `__name__` called from the module we
        # decorate.
        # Since `logging` is a singleton, everytime we call `logging.getLogger()` with the same
        # name, we receive the same logger, which "hides" this decorator as if the logging was
        # made from within the callable we decorate
        module = inspect.getmodule(func)
        logger = logging.getLogger(None if module is None else module.__name__)

        @functools.wraps(func)
        def inner(*args, **kwargs) -> t.Any:
            key = _make_key(func, *args, **kwargs)
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
