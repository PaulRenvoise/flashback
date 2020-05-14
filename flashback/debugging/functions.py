import ast
import inspect
import os
import sys
from textwrap import dedent

from .formatter import Formatter


ANSI_DIM_START = '\033[2m'
ANSI_DIM_END = '\033[0m'

def get_frameinfo(depth=0, context=1):
    """
    Finds the frame at `depth` and builds a `inspect.FrameInfo` from it.

    Executes 10 times faster than `inspect.stack()[depth]` if depth is superior to 1, else only 2
    times.

    Handles negative `depth` by returning the current frame from the caller's perspective, just
    like `sys._getframe()` does.

    Examples:
        ```python
        import inspect
        from flashback.debugging import get_frameinfo

        assert get_frameinfo() == inspect.stack()[0]

        def dummy_func():
            return get_frameinfo()

        frameinfo = dummy_func()
        assert frameinfo.function == 'dummy_func'
        ```

    Params:
        - `depth (int)` the depth at which to find the frame
        - `context (int)` the number of lines surrounding the frame to use in the traceback

    Returns:
        - `inspect.FrameInfo`: the FrameInfo object for the frame

    Raises:
        - `ValueError` if `depth` is greater than the length of the call stack
    """
    # Could use `sys._getframe(1)` but safer to go through its wrapper
    frame = inspect.currentframe()
    # Skips the actual current frame (the execution of get_frame())
    depth = depth + 1 if depth > -1 else 1
    for _ in range(depth):
        if frame is None:
            raise ValueError('call stack is not deep enough')

        frame = frame.f_back

    if frame is None:
        raise ValueError('call stack is not deep enough')

    frameinfo = (frame,) + inspect.getframeinfo(frame, context)
    return inspect.FrameInfo(*frameinfo)


def get_callable(frameinfo):
    """
    Finds the callable being executed during the given `frameinfo`.

    Starts by using the co_name found in the frame, then looks for a 'self' or 'cls' in the
    locals (in this case, callable is a method). If no class object or instance exists, looks
    into the frameinfo's globals (in that case, callable is just a function).

    Note, as of 12/05/2020:
    - Static methods are not found neither in locals nor globals, and they're
    not bound to a class or instance.
    - Closures and nested functions are not found neither in locals nor globals.
    - Lambdas exists in globals, but they're named as '<lambda>' in co_name, so we can't find them.

    Examples:
        ```python
        from flashback.debugging import get_frameinfo, get_callable

        def dummy_func():
            return get_frameinfo()

        frameinfo = dummy_func()

        assert get_callable(frameinfo) == dummy_func

        class DummyClass():
            def dummy_method(self):
                return get_frameinfo()

            @classmethod
            def dummy_classmethod(cls):
                return get_frameinfo()

        dummy_class = DummyClass()
        frameinfo = dummy_class.dummy_method()

        assert get_callable(frameinfo) == dummy_class.dummy_method

        frameinfo = DummyClass.dummy_classmethod()

        assert get_callable(frameinfo) == DummyClass.dummy_classmethod
        ```

    Params:
        - `frameinfo (inspect.FrameInfo)` the frameinfo to extract the callable from

    Returns:
        - `Callable|None` the callable instance if found
    """
    frame = frameinfo.frame

    function_name = frame.f_code.co_name

    caller_class = frame.f_locals.get('self', None)
    if caller_class is None:
        caller_class = frame.f_locals.get('cls', None)

    caller_instance = getattr(caller_class, function_name, None)
    if caller_instance is None:
        caller_instance = frame.f_globals.get(function_name, None)

    return caller_instance


def get_call_context(frameinfo, size=5):
    """
    Extracts the context surrounding the call statement of the given `frameinfo`, and returns its
    code, its first line number, and the boundaries of the call statement.

    Returns empty results if the frame has no code_context, or if the call is not found in the
    source file.

    Examples:
        ```python
        from flashback.debugging import get_frameinfo, get_call_context

        def dummy_func():
            return get_frameinfo()

        frameinfo = dummy_func()

        context, context_line, call_boundaries = get_call_context(frameinfo)

        assert context == [
            'from flashback.debugging import get_frameinfo, get_call_context\n',
            '\n',
            'def dummy_func():\n',
            '    return get_frameinfo()\n',
            '\n',
            'frameinfo = dummy_func()\n',
            '\n',
            'context, context_line, call_boundaries = get_call_context(frameinfo)\n',
            '\n',
        ]
        assert context_line == 1
        assert call_boundaries == (3, 4)
        ```

    Params:
        - `frameinfo (inspect.FrameInfo)` the frameinfo to extract the context from
        - `size (int)` the number of lines surrounding the call statement to take as context

    Returns:
        - `list<str>` the context extracted with at most `size` context lines before and after
        - `int|None` the line number of the context's first line
        - `typle<int>` the start and end of the call statement, as indices of the returned context
    """
    if not frameinfo.code_context:
        return [], None, ()

    try:
        source, _ = inspect.findsource(frameinfo.frame)
    except OSError:
        return [], None, ()

    # Prior to python 3.8, the frameinfo.lineno is sometimes wrong (lower than it actually is),
    # especially with nested function calls having newlines.
    # Could go backward in the file until it reaches an arbitrary maximum
    # trying to find the start of the call statement but it could end up finding
    # a prior call to the frame's call statement.
    lineno = frameinfo.lineno
    index_start = lineno - 1

    for index_end in range(index_start + 1, len(source) + 1):
        call_line = dedent(''.join(source[index_start:index_end]))

        try:
            ast.parse(call_line, filename=frameinfo.filename).body[0].value  # pylint: disable=expression-not-assigned

            break
        except (SyntaxError, AttributeError):
            pass

    call_statement_len = call_line.count('\n')

    context_start = max(0, lineno - (size + 1))
    context_end = min(len(source), lineno + call_statement_len + (size - 1))
    context = source[context_start:context_end]

    context_lineno = context_start + 1

    call_start = lineno - context_start - 1
    call_boundaries = (call_start, call_start + call_statement_len)

    return context, context_lineno, call_boundaries


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
        - `depth (int)` the depth to go back in the stack
        - `context (int)` the number of context lines around the call made to the callable to take

    Returns:
        - `Callable|None` the callable calling if found
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
