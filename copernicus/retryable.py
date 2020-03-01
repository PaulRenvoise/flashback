import functools
import inspect
import logging
import math
import time

from .formatting.functions import ordinalize


def retryable(max_retries=-1, plateau_after=10, reset_after=3600, exceptions=()):
    """
    Retries to call a function when a given connection exception is raised.

    The back-off implemented starts at 0s and ends up a 60s after 10 retries, like so:
        0.15, 0.70, 1.65, 3.30, 6.15, 11.09, 19.63, 34.41, 60.0

    Examples:
        ```
        ```

    Params:
        - `max_retries (int)` the maximum number of retries before raising the initial error (-1 retries indefinitely)
        - `plateau_after (int)` the number of retries after which to plateau the delay
        - `reset_after (int)` the number of seconds after which to reset the delay
        - `exceptions (tuple<Exception>)` the exceptions to trigger a retry on

    Returns :
        - `callable` a wrapper used to decorate a method/function
    """
    def wrapper(func):
        # `.getmodule().__name__` returns the same value as `__name__` called from the module we decorate
        # Since logging is a singleton, everytime we call `.getLogger()` with the same name, we receive the same logger
        # This let us 'hide' this decorator as if the logging was made from within the module we decorate
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
                    logger.warning("Caught %s", caught_exception)

                    if time_waited > reset_after:
                        current_try = 1

                    if retry_count < plateau_after:
                        retry_delay = round(math.exp(0.54856421 * current_try - 0.83273953) - 0.60263468, 2)

                        current_try += 1

                    retry_count += 1
                    if max_retries != -1 and retry_count > max_retries:
                        logger.warning('Reached the maximum number of retries, raising')

                        # Add a few debug info to the exception
                        caught_exception.retry_count = retry_count
                        caught_exception.time_waited = time_waited

                        raise caught_exception

                    logger.warning("Retrying for the %s time in %.2fs", ordinalize(retry_count), retry_delay)

                    time.sleep(retry_delay)

                    time_waited += retry_delay

        return inner

    return wrapper
