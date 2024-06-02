import time
from unittest.mock import Mock

import pytest

from flashback import timeoutable


def dummy_func(spy):
    time.sleep(2)
    spy()


class TestTimeoutable:
    def test_timeoutable(self):
        make_timeoutable = timeoutable(1)
        decorated_func = make_timeoutable(dummy_func)

        with pytest.raises(TimeoutError, match="execution timed out"):
            decorated_func(None)

    def test_timeoutable_without_timeout(self):
        spy_func = Mock()
        make_timeoutable = timeoutable(3)
        decorated_func = make_timeoutable(dummy_func)

        decorated_func(spy_func)

        assert spy_func.called

    def test_timeoutable_with_message(self):
        make_timeoutable = timeoutable(1, message="dummy_func timed out")
        decorated_func = make_timeoutable(dummy_func)
        with pytest.raises(TimeoutError, match="dummy_func timed out"):
            decorated_func(None)
