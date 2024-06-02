from unittest.mock import patch

import pytest

from flashback.debugging import get_frameinfo


class TestGetFrameInfo:
    def test_current(self):
        frameinfo = get_frameinfo()

        assert frameinfo.function == "test_current"

    def test_previous(self):
        def dummy_func(depth):
            return get_frameinfo(depth)

        frameinfo = dummy_func(1)

        assert frameinfo.function == "test_previous"

    def test_future(self):
        frameinfo = get_frameinfo(-1)

        assert frameinfo.function == "test_future"

    def test_deep(self):
        frameinfo = get_frameinfo(6)

        assert frameinfo.function == "pytest_runtest_call"

    @patch("inspect.currentframe")
    def test_no_current_frame(self, mocked_currentframe):
        mocked_currentframe.side_effect = [None]
        with pytest.raises(ValueError):  # noqa: PT011
            get_frameinfo(1)

    def test_no_last_frame(self):
        # TODO: remove magic index
        # How to make sure that the last call to frame.f_back returns None?
        with pytest.raises(ValueError):  # noqa: PT011
            get_frameinfo(37)
