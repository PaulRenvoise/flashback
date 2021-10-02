import functools
import signal


def timeoutable(seconds=5, message="execution timed out"):
    """
    Times out a callable's execution if its runtime exceeds `seconds`.

    Examples:
        ```python
        import time
        from flashback import timeoutable

        @timeoutable(1)
        def fast():
            time.sleep(0.1)

            return True

        fast()
        #=> True

        @timeoutable(1)
        def slow():
            time.sleep(3)

            return True

        slow()
        #=> TimeoutError: Execution timed out
        ```

    Params:
        seconds (int): the number of seconds to wait before timing out
        message (str): the custom message to display when timing out

    Return:
        Callable: a wrapper used to decorate a callable

    Raises:
        TimeoutError: if the callable's execution time is longer than `seconds`
    """
    def wrapper(func):
        def _sigalrm_handler(_signum, _frame):
            raise TimeoutError(message)

        @functools.wraps(func)
        def inner(*args, **kwargs):
            signal.signal(signal.SIGALRM, _sigalrm_handler)
            signal.alarm(seconds)

            try:
                return func(*args, **kwargs)
            finally:
                signal.alarm(0)

        return inner

    return wrapper
