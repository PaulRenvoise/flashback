from flashback.debugging import get_frameinfo, get_call_context


def dummy_function():
    return get_frameinfo()


def dummy_function_multiline():  # Used for TestGetCallContext
    return get_frameinfo(depth=0)


class TestGetCallContext:
    def test_one_line_call(self):
        frameinfo = dummy_function()

        context, context_lineno, call_boundaries = get_call_context(frameinfo)

        assert len(context) == 10
        assert context_lineno == 1
        assert call_boundaries == (4, 5)

    def test_one_line_call_with_size(self):
        frameinfo = dummy_function()

        context, context_lineno, call_boundaries = get_call_context(frameinfo, size=20)

        assert len(context) == 25
        assert context_lineno == 1
        assert call_boundaries == (4, 5)

    def test_multiline_call(self):
        frameinfo = dummy_function_multiline()

        context, context_lineno, call_boundaries = get_call_context(frameinfo)

        assert len(context) == 11
        assert context_lineno == 4
        assert call_boundaries == (5, 6)

    def test_no_context(self):
        frameinfo = eval("get_frameinfo()")

        context, context_lineno, call_boundaries = get_call_context(frameinfo)

        assert len(context) == 0
        assert context_lineno is None
        assert not call_boundaries

    def test_eof(self):
        frameinfo = dummy_function_eof()

        context, context_lineno, call_boundaries = get_call_context(frameinfo)

        assert len(context) == 6
        assert context_lineno == 55
        assert call_boundaries == (5, 6)


def dummy_function_eof():
    return get_frameinfo()
