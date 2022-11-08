# pylint: disable=no-member,protected-access,redefined-outer-name

import time

import pytest
from mock import Mock

from flashback import sampled


def dummy_func(spy):
    spy()


@pytest.fixture
def spy_func():
    return Mock()

class TestSampled:
    def test_sampled(self, spy_func):
        make_sampled = sampled()
        decorated_func = make_sampled(dummy_func)

        decorated_func(spy_func)

        assert spy_func.called

    def test_sampled_invalid_strategy(self):
        with pytest.raises(ValueError):
            sampled(strategy="invalid")

    def test_sampled_constant(self, spy_func):
        make_sampled = sampled(strategy="constant")
        decorated_func = make_sampled(dummy_func)

        decorated_func(spy_func)

        assert spy_func.called

    def test_sampled_constant_valid_rate(self, spy_func):
        make_sampled = sampled(strategy="constant", rate=0)
        decorated_func = make_sampled(dummy_func)

        decorated_func(spy_func)

        assert not spy_func.called

    def test_sampled_constant_invalid_rate(self):
        with pytest.raises(ValueError):
            sampled(strategy="constant", rate=2)

    def test_sampled_probabilistic(self, spy_func):
        make_sampled = sampled(strategy="probabilistic")
        decorated_func = make_sampled(dummy_func)

        for _ in range(100):
            decorated_func(spy_func)

        assert 30 < spy_func.call_count < 70

    def test_sampled_probabilistic_valid_rate(self, spy_func):
        make_sampled = sampled(strategy="probabilistic", rate=0.3)
        decorated_func = make_sampled(dummy_func)

        for _ in range(100):
            decorated_func(spy_func)

        assert 10 < spy_func.call_count < 50

    def test_sampled_probabilistic_invalid_rate(self):
        with pytest.raises(ValueError):
            sampled(strategy="probabilistic", rate=10)

    def test_sampled_ratelimiting(self, spy_func):
        make_sampled = sampled(strategy="ratelimiting")
        decorated_func = make_sampled(dummy_func)

        for _ in range(11):
            time.sleep(0.1)
            decorated_func(spy_func)

        assert 10 <= spy_func.call_count < 15

    def test_sampled_ratelimiting_valid_rate(self, spy_func):
        make_sampled = sampled(strategy="ratelimiting", rate=5)
        decorated_func = make_sampled(dummy_func)

        for _ in range(11):
            time.sleep(0.1)
            decorated_func(spy_func)

        assert 5 <= spy_func.call_count < 10

    def test_sampled_ratelimiting_invalid_rate(self):
        with pytest.raises(ValueError):
            sampled(strategy="ratelimiting", rate=-1)
