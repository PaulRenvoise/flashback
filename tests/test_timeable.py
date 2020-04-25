# pylint: disable=no-self-use,no-member,protected-access

import time

from mock import Mock

from flashback import timeable


def dummy_func(spy):
    spy.__call__()
    time.sleep(1)


class TestTimeable:
    def test_execution(self):
        spy_func = Mock()

        decorated_func = timeable(dummy_func)
        decorated_func(spy_func)

        assert spy_func.called
