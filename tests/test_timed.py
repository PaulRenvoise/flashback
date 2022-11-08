# pylint: disable=no-member,protected-access

import time

from mock import Mock

from flashback import timed


def dummy_func(spy):
    spy()
    time.sleep(1)


class TestTimed:
    def test_execution(self):
        spy_func = Mock()

        decorated_func = timed(dummy_func)
        decorated_func(spy_func)

        assert spy_func.called
