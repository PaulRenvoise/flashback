from __future__ import annotations

from typing import Any, TextIO
import sys

from .parser import Parser
from .formatter import Formatter


PARSER = Parser()
FORMATTER = Formatter()


def xp(*arguments: tuple[Any, ...], o: TextIO = sys.stderr, f: bool = True, w: int = 120) -> tuple[Any, ...] | None:
    """
    Provides a simple and concise way of printing for debugging purposes.

    Returns the arguments received, to allow chaining of calls, and inline debugging statements.

    Consumes generators to print them (be careful with infinite ones!).

    Inspired by:

    - https://github.com/samuelcolvin/python-devtools
    - https://github.com/gruns/icecream
    - https://github.com/wolever/pprintpp

    Examples:
        ```python
        from flashback.debugging import xp

        # Simple as that
        xp(1)
        #=> xp.py:22
        #=>     1 (int)

        # Can print several arguments at once
        a = "This is a short sentence"
        b = dict(string="value", int=1)
        c = ("l", "i", "s", "t")
        d = {1, 2, 3, 4}

        xp(a, b, c, d)
        #=> xp.py:33
        #=>   a:
        #=>     "This is a short sentence" (str)
        #=>   b:
        #=>     {
        #=>         "string": "value",
        #=>         "int": 1,
        #=>     } (dict)
        #=>   c:
        #=>     ("l", "i", "s", "t") (tuple)
        #=>   d:
        #=>     {1, 2, 3, 4} (set)

        # Also print more complex objects
        # And returns their values
        def dummy_func(a, b):
            return a + b

        result = xp(dummy_func(1, 1))
        #=> xp.py:51
        #=>   dummy_func(1, 1)
        #=>     2 (int)

        assert result == 2
        #=> True
        ```

    Params:
        arguments: every positional arguments
        o: the target output of print
        f: whether of not the output is flushed
        w: the maximum width before wrapping the output

    Returns:
        the arguments or their results
    """
    filename, lineno, parsed_arguments, warning = PARSER.parse(*arguments)
    output = FORMATTER.format(filename, lineno, parsed_arguments, warning, width=w)

    print(output, file=o, flush=f)

    # Forwards the arguments received to the (possible) next operation
    if len(arguments) == 0:
        result = None
    elif len(arguments) == 1:
        result = arguments[0]
    else:
        result = arguments

    return result
