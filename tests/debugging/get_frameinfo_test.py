from inspect import FrameInfo
from unittest.mock import patch

import pytest

from flashback.debugging import get_frameinfo


class GetFrameInfoTest:
    def current_test(self) -> None:
        frameinfo = get_frameinfo()

        assert frameinfo.function == "current_test"

    def previous_test(self) -> None:
        def dummy_func(depth) -> FrameInfo:
            return get_frameinfo(depth)

        frameinfo = dummy_func(1)

        assert frameinfo.function == "previous_test"

    def future_test(self) -> None:
        frameinfo = get_frameinfo(-1)

        assert frameinfo.function == "future_test"

    def deep_test(self) -> None:
        frameinfo = get_frameinfo(6)

        assert frameinfo.function == "pytest_runtest_call"

    @patch("inspect.currentframe")
    def no_current_frame_test(self, mocked_currentframe) -> None:
        mocked_currentframe.side_effect = [None]
        with pytest.raises(ValueError):  # noqa: PT011
            get_frameinfo(1)

    def no_last_frame_test(self) -> None:
        # TODO: remove magic index
        # How to make sure that the last call to frame.f_back returns None?
        with pytest.raises(ValueError):  # noqa: PT011
            get_frameinfo(37)
