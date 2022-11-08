# pylint: disable=no-member,protected-access

import time

import pytest
from mock import Mock

from flashback import timeoutable


def dummy_func(spy):
    time.sleep(2)
    spy()


class TestTimeoutable:
    def test_timeoutable(self):
        make_timeoutable = timeoutable(1)
        decorated_func = make_timeoutable(dummy_func)

        with pytest.raises(TimeoutError) as e:
            decorated_func(None)
            assert e.message == "execution timed out"

    def test_timeoutable_without_timeout(self):
        spy_func = Mock()
        make_timeoutable = timeoutable(3)
        decorated_func = make_timeoutable(dummy_func)

        decorated_func(spy_func)

        assert spy_func.called

    def test_timeoutable_with_message(self):
        make_timeoutable = timeoutable(1, message="dummy_func timed out")
        decorated_func = make_timeoutable(dummy_func)
        with pytest.raises(TimeoutError) as e:
            decorated_func(None)
            assert e.message == "dummy_func timed out"
