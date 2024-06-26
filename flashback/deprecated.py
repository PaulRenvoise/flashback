from __future__ import annotations

from collections.abc import Callable
import functools
import warnings


def deprecated(since: str | None = None, until: str | None = None, reason: str | None = None) -> Callable:
    """
    Warns when a deprecated callable is used.

    Examples:
        ```python
        from flashback import deprecated

        @deprecated
        def func():
            pass

        func()
        #=> func is deprecated.

        @deprecated(since="v2", until="v3", reason="it has moved")
        def func():
            pass

        func()
        #=> func is deprecated since v2 and will be removed in v3 because it has moved.
        ```

    Params:
        since: the date/version the callable was deprecated
        until: the date/version the callable will be removed
        reason: the reason of the deprecation

    Returns:
        a wrapper used to decorate a callable
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
            message += "."

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
