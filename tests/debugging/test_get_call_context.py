from inspect import FrameInfo

from flashback.debugging import get_frameinfo, get_call_context


def dummy_function() -> FrameInfo:
    return get_frameinfo()


def dummy_function_multiline() -> FrameInfo:  # Used for TestGetCallContext
    return get_frameinfo(depth=0)


class TestGetCallContext:
    def test_one_line_call(self) -> None:
        frameinfo = dummy_function()

        context, context_lineno, call_boundaries = get_call_context(frameinfo)

        assert len(context) == 11
        assert context_lineno == 2
        assert call_boundaries == (5, 6)

    def test_one_line_call_with_size(self) -> None:
        frameinfo = dummy_function()

        context, context_lineno, call_boundaries = get_call_context(frameinfo, size=20)

        assert len(context) == 27
        assert context_lineno == 1
        assert call_boundaries == (6, 7)

    def test_multiline_call(self) -> None:
        frameinfo = dummy_function_multiline()

        context, context_lineno, call_boundaries = get_call_context(frameinfo)

        assert len(context) == 11
        assert context_lineno == 6
        assert call_boundaries == (5, 6)

    def test_no_context(self) -> None:
        frameinfo = eval("get_frameinfo()")

        context, context_lineno, call_boundaries = get_call_context(frameinfo)

        assert len(context) == 0
        assert context_lineno is None
        assert not call_boundaries

    def test_eof(self) -> None:
        frameinfo = dummy_function_eof()

        context, context_lineno, call_boundaries = get_call_context(frameinfo)

        assert len(context) == 6
        assert context_lineno == 57
        assert call_boundaries == (5, 6)


def dummy_function_eof() -> FrameInfo:
    return get_frameinfo()
