import ast
import inspect
from textwrap import dedent


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
            "from flashback.debugging import get_frameinfo, get_call_context\n",
            "\n",
            "def dummy_func():\n",
            "    return get_frameinfo()\n",
            "\n",
            "frameinfo = dummy_func()\n",
            "\n",
            "context, context_line, call_boundaries = get_call_context(frameinfo)\n",
            "\n",
        ]
        assert context_line == 1
        assert call_boundaries == (3, 4)
        ```

    Params:
        frameinfo (inspect.FrameInfo): the frameinfo to extract the context from
        size (int): the number of lines surrounding the call statement to take as context

    Returns:
        list<str>: the context extracted with at most `size` context lines before and after
        int|None: the line number of the context's first line
        typle<int>: the start and end of the call statement, as indices of the returned context
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
        call_line = dedent("".join(source[index_start:index_end]))

        try:
            ast.parse(call_line, filename=frameinfo.filename).body[0].value  # pylint: disable=expression-not-assigned

            break
        except (SyntaxError, AttributeError):
            pass

    call_statement_len = call_line.count("\n")

    context_start = max(0, lineno - (size + 1))
    context_end = min(len(source), lineno + call_statement_len + (size - 1))
    context = source[context_start:context_end]

    context_lineno = context_start + 1

    call_start = lineno - context_start - 1
    call_boundaries = (call_start, call_start + call_statement_len)

    return context, context_lineno, call_boundaries
