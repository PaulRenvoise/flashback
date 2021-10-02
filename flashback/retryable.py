import functools
import inspect
import logging
import math
import time

from .formatting import ordinalize


def retryable(max_retries=-1, plateau_after=10, reset_after=3600, exceptions=()):
    """
    Retries to call a callable when a given exception is raised.

    The back-off starts at 0s and ends up at 60s after 10 retries:
    ```python
    0.15, 0.70, 1.65, 3.30, 6.15, 11.09, 19.63, 34.41, 60.0
    ```

    With a `max_retries` of `-1`, the decorated callable will be retried indefinitely.

    Examples:
        ```python
        from flashback import retryable

        @retryable(exceptions=(TypeError,))
        def will_be_retried(arg):
            if isinstance(arg, str):
                raise RuntimeError
            else:
                raise TypeError

        will_be_retried("str")
        #=> RuntimeError

        will_be_retried(0)
        #=> Caught TypeError
        #=> Retrying for the 1st time in 0.15s
        #=> Caught TypeError
        #=> Retrying for the 2nd time in 0.70s
        #=> Caught TypeError
        #=> Retrying for the 3rd time in 1.65s
        #=> Caught TypeError
        #=> Retrying for the 4th time in 3.30s
        #=> Caught TypeError
        #=> Retrying for the 5th time in 6.15s
        #=> ...
        ```

    Params:
        max_retries (int): the max number of retries before raising the initial error
        plateau_after (int): the number of retries after which to plateau the delay
        reset_after (int): the number of seconds after which to reset the delay
        exceptions (tuple<Exception>): the exceptions to trigger a retry on

    Returns :
        Callable: a wrapper used to decorate a callable
    """
    def wrapper(func):
        # `.getmodule().__name__` returns the same value as `__name__` called from the module we
        # decorate.
        # Since `logging` is a singleton, everytime we call `logging.getLogger()` with the same
        # name, we receive the same logger, which "hides" this decorator as if the logging was
        # made from within the callable we decorate
        logger = logging.getLogger(inspect.getmodule(func).__name__)

        @functools.wraps(func)
        def inner(*args, **kwargs):
            retry_count = 0
            current_try = 1

            retry_delay = 0
            time_waited = 0

            while True:
                try:
                    return func(*args, **kwargs)
                except exceptions as caught_exception:
                    logger.warning("Caught %s", caught_exception.__class__.__name__)

                    if time_waited > reset_after:
                        current_try = 1

                    if retry_count < plateau_after:
                        retry_delay = round(math.exp(0.54856421 * current_try - 0.83273953) - 0.60263468, 2)

                        current_try += 1

                    retry_count += 1
                    if max_retries != -1 and retry_count > max_retries:
                        logger.warning("Reached the maximum number of retries, raising")

                        # Add a few debug info to the exception
                        caught_exception.retry_count = retry_count
                        caught_exception.time_waited = time_waited

                        raise caught_exception

                    logger.warning("Retrying for the %s time in %.2fs", ordinalize(retry_count), retry_delay)

                    time.sleep(retry_delay)

                    time_waited += retry_delay

        return inner

    return wrapper
