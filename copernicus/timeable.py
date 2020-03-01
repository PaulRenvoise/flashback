import functools
import inspect
import logging
import time


def timeable(func):
    """
    Logs the start and end of a function call, and records the time spent executing it.

    Examples:
        ```
        from copernicus import timeable

        @timeable
        def printer():
            print('Executing')

        printer()
        #=> Started execution of printer
        #=> Executing
        #=> Completed execution of printer after 2.47955322265625e-05s
        ```

    Params:
        - `func (callable)` the function to time

    Returns:
        - `callable` a wrapper used to decorate a method/function
    """
    # `.getmodule().__name__` returns the same value as `__name__` called from the module we decorate
    # Each time we call `getLogger()` with the same name, we receive the same logger since `logging` is a singleton
    # This "pretends" the logging was made from within the module/function we decorate
    logger = logging.getLogger(inspect.getmodule(func).__name__)

    @functools.wraps(func)
    def inner(*args, **kwargs):
        logger.info("Started execution of %s", func.__name__)
        before = time.time()

        result = func(*args, **kwargs)

        after = time.time() - before
        logger.info("Completed execution of %s after %fs", func.__name__, after)

        return result

    return inner
