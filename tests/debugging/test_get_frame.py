# pylint: disable=no-self-use,redefined-outer-name

import pytest
from mock import patch

from flashback.debugging import get_frame


class TestGetFrame:
    def test_current(self):
        frameinfo = get_frame()

        assert frameinfo.function == 'test_current'

    def test_previous(self):
        def dummy_func(depth):
            return get_frame(depth)

        frameinfo = dummy_func(1)

        assert frameinfo.function == 'test_previous'

    def test_future(self):
        frameinfo = get_frame(-1)

        assert frameinfo.function == 'test_future'

    def test_deep(self):
        frameinfo = get_frame(6)

        assert frameinfo.function == 'runtest'

    @patch('inspect.currentframe')
    def test_no_current_frame(self, mocked_currentframe):
        mocked_currentframe.side_effect = [None]
        with pytest.raises(ValueError):
            get_frame(1)

    def test_no_last_frame(self):
        # TODO: remove magic index
        # How to make sure that the last call to frame.f_back returns None?
        with pytest.raises(ValueError):
            get_frame(36)