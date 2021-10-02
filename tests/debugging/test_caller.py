# pylint: disable=no-self-use,redefined-outer-name

from io import StringIO
import sys

import pytest
from mock import patch

from flashback.debugging import caller


@pytest.fixture
def output():
    return StringIO()


class TestCaller:
    def test_execution(self, output):
        caller_instance = caller(output=output)
        captured = output.getvalue()

        assert caller_instance.__name__ == "pytest_pyfunc_call"
        assert len(captured.splitlines()) == 12

    def test_execution_with_depth(self, output):
        caller_instance = caller(depth=30, output=output)
        captured = output.getvalue()

        assert caller_instance.__name__ == "main"
        # Prior to python 3.8, the lineno for multiline calls is wrong
        if sys.version >= "3.8":
            assert len(captured.splitlines()) == 14
        else:
            assert len(captured.splitlines()) == 12

    def test_execution_with_context(self, output):
        caller_instance = caller(context=10, output=output)
        captured = output.getvalue()

        assert caller_instance.__name__ == "pytest_pyfunc_call"
        assert len(captured.splitlines()) == 22

    @patch("inspect.currentframe")
    def test_no_frame(self, mocked_currentframe, output):
        mocked_currentframe.side_effect = [None]

        caller_instance = caller(output=output)
        captured = output.getvalue()

        assert caller_instance is None
        assert len(captured.splitlines()) == 2
        assert "No code context found" in captured

    @patch("inspect.findsource")
    def test_no_context(self, mocked_findsource, output):
        mocked_findsource.side_effect = OSError("could not get source code")

        caller_instance = caller(depth=3, output=output)  # depth=3 because we have a decorator
        captured = output.getvalue()

        assert caller_instance.__name__ == "pytest_pyfunc_call"
        assert len(captured.splitlines()) == 2

    @patch("flashback.debugging.get_callable")
    def test_no_callable(self, mocked_get_callable, output):
        mocked_get_callable.side_effect = [None]

        caller_instance = caller(output=output)
        captured = output.getvalue()

        assert caller_instance is None
        assert len(captured.splitlines()) == 12
