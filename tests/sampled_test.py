import time
from unittest.mock import Mock

import pytest

from flashback import sampled


def dummy_func(spy) -> None:
    spy()


@pytest.fixture
def spy_func() -> Mock:
    return Mock()


class SampledTest:
    def execution_test(self, spy_func) -> None:
        make_sampled = sampled()
        decorated_func = make_sampled(dummy_func)

        decorated_func(spy_func)

        assert spy_func.called

    def invalid_strategy_test(self) -> None:
        with pytest.raises(ValueError):  # noqa: PT011
            sampled(strategy="invalid")

    def constant_strategy_test(self, spy_func) -> None:
        make_sampled = sampled(strategy="constant")
        decorated_func = make_sampled(dummy_func)

        decorated_func(spy_func)

        assert spy_func.called

    def constant_strategy_valid_rate_test(self, spy_func: Mock) -> None:
        make_sampled = sampled(strategy="constant", rate=0)
        decorated_func = make_sampled(dummy_func)

        decorated_func(spy_func)

        assert not spy_func.called

    def constant_strategy_invalid_rate_test(self) -> None:
        with pytest.raises(ValueError, match="invalid rate"):
            sampled(strategy="constant", rate=2)

    def probabilistic_strategy_test(self, spy_func: Mock) -> None:
        make_sampled = sampled(strategy="probabilistic")
        decorated_func = make_sampled(dummy_func)

        for _ in range(100):
            decorated_func(spy_func)

        assert 30 < spy_func.call_count < 70

    def probabilistic_strategy_valid_rate_test(self, spy_func: Mock) -> None:
        make_sampled = sampled(strategy="probabilistic", rate=0.3)
        decorated_func = make_sampled(dummy_func)

        for _ in range(100):
            decorated_func(spy_func)

        assert 10 < spy_func.call_count < 50

    def probabilistic_strategy_invalid_rate_test(self) -> None:
        with pytest.raises(ValueError, match="invalid rate"):
            sampled(strategy="probabilistic", rate=10)

    def ratelimiting_strategy_test(self, spy_func: Mock) -> None:
        make_sampled = sampled(strategy="ratelimiting")
        decorated_func = make_sampled(dummy_func)

        for _ in range(11):
            time.sleep(0.1)
            decorated_func(spy_func)

        assert 10 <= spy_func.call_count < 15

    def ratelimiting_strategy_valid_rate_test(self, spy_func: Mock) -> None:
        make_sampled = sampled(strategy="ratelimiting", rate=5)
        decorated_func = make_sampled(dummy_func)

        for _ in range(11):
            time.sleep(0.1)
            decorated_func(spy_func)

        assert 5 <= spy_func.call_count < 10

    def ratelimiting_strategy_invalid_rate_test(self) -> None:
        with pytest.raises(ValueError, match="invalid rate"):
            sampled(strategy="ratelimiting", rate=-1)
