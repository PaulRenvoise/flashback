import time
from unittest.mock import Mock

from flashback import timed


def dummy_func(spy) -> None:
    spy()
    time.sleep(1)


class TimedTest:
    def execution_test(self) -> None:
        spy_func = Mock()

        decorated_func = timed(dummy_func)
        decorated_func(spy_func)

        assert spy_func.called
