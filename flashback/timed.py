from typing import Any, Callable
import functools
import inspect
import logging
import time


def timed(func: Callable) -> Callable:
    """
    Logs the start and end of a function call, and records the time spent executing it.

    Examples:
        ```python
        from flashback import timed

        @timed
        def printer():
            print("Executing")

        printer()
        #=> Started execution of printer
        #=> Executing
        #=> Completed execution of printer after 2.47955322265625e-05s
        ```

    Params:
        func: the callable to time

    Returns:
        a wrapper used to decorate a callable
    """
    # `.getmodule().__name__` returns the same value as `__name__` called from the module we
    # decorate.
    # Since `logging` is a singleton, everytime we call `logging.getLogger()` with the same
    # name, we receive the same logger, which "hides" this decorator as if the logging was
    # made from within the callable we decorate
    module  = inspect.getmodule(func)
    if module:
        logger = logging.getLogger(module.__name__)
    else:
        logger = logging.getLogger()

    @functools.wraps(func)
    def inner(*args: Any, **kwargs: Any) -> Any:
        logger.info("Started execution of %s", func.__name__)
        before = time.time()

        result = func(*args, **kwargs)

        after = time.time() - before
        logger.info("Completed execution of %s after %fs", func.__name__, after)

        return result

    return inner
