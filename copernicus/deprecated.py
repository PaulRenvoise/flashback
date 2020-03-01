import functools
import warnings


def deprecated(since=None, until=None, reason=None):
    """
    Warns that a deprecated method/function is used.

    Examples:
        ```
        from copernicus import deprecated

        @deprecated
        def func():
            pass

        func()
        #=> func is deprecated.

        @deprecated(since='today', until='tomorrow', reason='it is a test')
        def func():
            pass

        func()
        #=> func is deprecated since today and will be removed tomorrow because it is a test.
        ```

    Params:
        - `since (str)` the version at which the function was deprecated
        - `until (str)` the version at which the function will be removed
        - `reason (str)` the reason of the deprecation, must complete the phrase "because [...]" without final dot

    Returns:
        - `callable` a wrapper used to decorate a method/function
    """
    def wrapper(func):
        message = f"{func.__name__} is deprecated"
        if since:
            message += f" since {since}"
        if until:
            message += f" and will be removed in {until}"
        if reason:
            message += f" because {reason}."
        else:
            message += '.'

        doc = func.__doc__ or ""
        if len(doc) > 0:
            doc += "\n\n"
        doc += f".. deprecated:: {message}"

        func.__doc__ = doc

        @functools.wraps(func)
        def inner(*args, **kwargs):
            warnings.warn(message, category=DeprecationWarning, stacklevel=2)

            return func(*args, **kwargs)

        return inner

    return wrapper
