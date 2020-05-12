# pylint: disable=no-self-use,redefined-outer-name

from io import StringIO
import sys

import pytest
from mock import patch

from flashback.debugging import caller, get_callable, get_call_context, get_frameinfo


def dummy_function():
    return get_frameinfo()


def dummy_function_multiline():  # Used for TestGetCallContext
    return get_frameinfo(
        depth=0
    )


def dummy_closure():
    def _closure():
        return get_frameinfo()

    return _closure


def dummy_nested_function():
    def _nested_function():
        return get_frameinfo()

    return _nested_function()


class DummyClass():
    def dummy_method(self):
        return get_frameinfo()

    @classmethod
    def dummy_classmethod(cls):
        return get_frameinfo()

    @staticmethod
    def dummy_staticmethod():
        return get_frameinfo()

dummy_lambda = lambda: get_frameinfo()  # pylint: disable=unnecessary-lambda


@pytest.fixture
def output():
    return StringIO()


class TestCaller:
    def test_execution(self, output):
        caller_instance = caller(output=output)
        captured = output.getvalue()

        assert caller_instance.__name__ == 'pytest_pyfunc_call'
        assert len(captured.splitlines()) == 12

    def test_execution_with_depth(self, output):
        caller_instance = caller(depth=35, output=output)
        captured = output.getvalue()

        assert caller_instance.__name__ == 'main'
        # Prior to python 3.8, the lineno for multiline calls is wrong
        if sys.version >= '3.8':
            assert len(captured.splitlines()) == 14
        else:
            assert len(captured.splitlines()) == 12

    def test_execution_with_context(self, output):
        caller_instance = caller(context=10, output=output)
        captured = output.getvalue()

        assert caller_instance.__name__ == 'pytest_pyfunc_call'
        assert len(captured.splitlines()) == 22

    @patch('inspect.currentframe')
    def test_no_frame(self, mocked_currentframe, output):
        mocked_currentframe.side_effect = [None]

        caller_instance = caller(output=output)
        captured = output.getvalue()

        assert caller_instance is None
        assert len(captured.splitlines()) == 2
        assert 'No code context found' in captured

    @patch('inspect.findsource')
    def test_no_context(self, mocked_findsource, output):
        mocked_findsource.side_effect = OSError('could not get source code')

        caller_instance = caller(depth=3, output=output)  # depth=3 because we have a decorator
        captured = output.getvalue()

        assert caller_instance.__name__ == 'pytest_pyfunc_call'
        assert len(captured.splitlines()) == 2

    @patch('flashback.debugging.get_callable')
    def test_no_callable(self, mocked_get_callable, output):
        mocked_get_callable.side_effect = [None]

        caller_instance = caller(output=output)
        captured = output.getvalue()

        assert caller_instance is None
        assert len(captured.splitlines()) == 12


class TestGetCallable:
    def test_function(self):
        frameinfo = dummy_function()

        callable_instance = get_callable(frameinfo)

        assert callable_instance.__name__ == 'dummy_function'

    def test_closure(self):
        frameinfo = dummy_closure()()

        callable_instance = get_callable(frameinfo)

        assert callable_instance is None

    def test_nested(self):
        frameinfo = dummy_nested_function()

        callable_instance = get_callable(frameinfo)

        assert callable_instance is None

    def test_lambda(self):
        frameinfo = dummy_lambda()

        callable_instance = get_callable(frameinfo)

        assert callable_instance is None

    def test_method(self):
        dummy_class = DummyClass()
        frameinfo = dummy_class.dummy_method()

        callable_instance = get_callable(frameinfo)

        assert callable_instance.__name__ == 'dummy_method'

    def test_classmethod(self):
        frameinfo = DummyClass.dummy_classmethod()

        callable_instance = get_callable(frameinfo)

        assert callable_instance.__name__ == 'dummy_classmethod'

    def test_staticmethod(self):
        dummy_class = DummyClass()
        frameinfo = dummy_class.dummy_staticmethod()

        callable_instance = get_callable(frameinfo)

        assert callable_instance is None


class TestGetCallContext:
    def test_one_line_call(self):
        frameinfo = dummy_function()

        context, context_lineno, call_boundaries = get_call_context(frameinfo)

        assert len(context) == 11
        assert context_lineno == 8
        assert call_boundaries == (5, 6)

    def test_one_line_call_with_size(self):
        frameinfo = dummy_function()

        context, context_lineno, call_boundaries = get_call_context(frameinfo, size=20)

        assert len(context) == 33  # Should be 41, but reaching the top of the file
        assert context_lineno == 1
        assert call_boundaries == (12, 13)

    def test_multiline_call(self):
        frameinfo = dummy_function_multiline()

        context, context_lineno, call_boundaries = get_call_context(frameinfo)

        # Prior to python 3.8, the lineno for multiline calls is wrong
        if sys.version >= '3.8':
            assert len(context) == 13
            assert context_lineno == 12
            assert call_boundaries == (5, 8)
        else:
            assert len(context) == 11
            assert context_lineno == 11
            assert call_boundaries == (5, 8)

    def test_no_context(self):
        frameinfo = eval('get_frameinfo()')  # pylint: disable=eval-used

        context, context_lineno, call_boundaries = get_call_context(frameinfo)

        assert len(context) == 0
        assert context_lineno is None
        assert call_boundaries == ()

    def test_eof(self):
        frameinfo = dummy_function_eof()

        context, context_lineno, call_boundaries = get_call_context(frameinfo)

        assert len(context) == 6
        assert context_lineno == 253
        assert call_boundaries == (5, 6)


class TestGetFrameInfo:
    def test_current(self):
        frameinfo = get_frameinfo()

        assert frameinfo.function == 'test_current'

    def test_previous(self):
        def dummy_func(depth):
            return get_frameinfo(depth)

        frameinfo = dummy_func(1)

        assert frameinfo.function == 'test_previous'

    def test_future(self):
        frameinfo = get_frameinfo(-1)

        assert frameinfo.function == 'test_future'

    def test_deep(self):
        frameinfo = get_frameinfo(6)

        assert frameinfo.function == 'runtest'

    @patch('inspect.currentframe')
    def test_no_current_frame(self, mocked_currentframe):
        mocked_currentframe.side_effect = [None]
        with pytest.raises(ValueError):
            get_frameinfo(1)

    def test_no_last_frame(self):
        # TODO: remove magic index
        # How to make sure that the last call to frame.f_back returns None?
        with pytest.raises(ValueError):
            get_frameinfo(36)


def dummy_function_eof():
    return get_frameinfo()
