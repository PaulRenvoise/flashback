import inspect
import os
import sys

from .formatter import Formatter
from .get_callable import get_callable
from .get_call_context import get_call_context
from .get_frameinfo import get_frameinfo


ANSI_DIM_START = "\x1b[2m"
ANSI_DIM_END = "\x1b[0m"

def caller(depth=2, context=5, output=sys.stderr):
    """
    Prints debug information about the caller of the current callable being executed, and returns
    the caller object if found.

    Examples:
        ```python
        from flashback.debugging import caller

        def add(*args):
            sum(args)

            return caller(context=2)

        def subtract(*args):
            args = [args[0]] + [-num for num in args[1:]]

            return add(*args)

        caller_instance = add(1, 2, 3)
        #=> Called by '__main__.<module>' (/Users/plk/Work/flashback/test.py:13):
        #=> 11     return add(*args)
        #=> 12
        #=> 13 caller_instance = add(1, 2, 3)
        #=> 14 #=> Called by '__main__.<module>' (/Users/plk/Work/flashback/test.py:13):
        #=> 15 #=> 11     return add(*args)

        # None because it is called by '<module>'
        assert caller_instance is None

        caller_instance = subtract(1, 2, 3)
        #=> Called by '__main__.subtract' (/Users/plk/Work/flashback/test.py:11):
        #=>  9     args = [args[0]] + [-num for num in args[1:]]
        #=> 10
        #=> 11     return add(*args)
        #=> 12
        #=> 13 caller_instance = add(1, 2, 3)

        assert caller_instance == subtract
        ```

    Params:
        depth (int): the depth to go back in the stack
        context (int): the number of context lines around the call made to the callable to take

    Returns:
        Callable|None: the callable calling if found
    """
    try:
        frameinfo = get_frameinfo(depth)
    except ValueError:
        print("Called by '__main__.<module>' (<unknown>:1):", file=output)
        print(f"{ANSI_DIM_START}No code context found{ANSI_DIM_END}", file=output)

        return None

    filename = os.path.abspath(frameinfo.filename)
    lineno = frameinfo.lineno

    # Extract call context, with -context/+context lines of context at most
    call_context, call_context_lineno, call_boundaries = get_call_context(frameinfo, size=context)

    caller_instance = get_callable(frameinfo)

    module = inspect.getmodule(frameinfo.frame, _filename=filename)
    module_name = module.__name__ if module else '__main__'
    # From the found instance (if any), calls __qualname__. At worst, falls back to the frameinfo's
    # co_name. Having access to __qualname__ directly in the frame is in the works since 2011:
    # - https://bugs.python.org/issue12857
    # - https://bugs.python.org/issue13672
    function_name = caller_instance.__qualname__ if caller_instance else frameinfo.frame.f_code.co_name

    formatter = Formatter()
    print(f"Called by '{module_name}.{function_name}' ({filename}:{lineno}):", file=output)
    if call_context:
        code = formatter.format_code(call_context, start_lineno=call_context_lineno, highlight=call_boundaries)

        print(code, file=output)
    else:
        print(f"{ANSI_DIM_START}No code context found{ANSI_DIM_END}", file=output)

    return caller_instance
