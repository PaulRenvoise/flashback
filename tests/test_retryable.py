# coding: utf-8
# pylint: disable=no-self-use,no-member,protected-access

import math
import time

import pytest
from mock import Mock

from copernicus import retryable


class TestRetryable:
    def test_without_exception(self):
        mock_without_exception = Mock()

        make_retryable = retryable()
        decorated_function = make_retryable(mock_without_exception)
        decorated_function()

    def test_with_exception(self):
        mock_with_exception = Mock(side_effect=[Exception, None])

        before = time.time()

        make_retryable = retryable(exceptions=(Exception,))
        decorated_function = make_retryable(mock_with_exception)
        decorated_function()

        after = time.time() - before

        # We catch only 1 exception
        # 0.15 (first retry)
        assert math.isclose(after, 0.15, rel_tol=0.05)

    def test_with_plateau_after(self):
        mock_with_exception = Mock(side_effect=[Exception, Exception, None])

        before = time.time()

        make_retryable = retryable(plateau_after=1, exceptions=(Exception,))
        decorated_function = make_retryable(mock_with_exception)
        decorated_function()

        after = time.time() - before

        # We catch 2 exceptions, and plateau after 1 retry
        # 0.15 (first retry) + 0.15 (second retry)
        assert math.isclose(after, 0.30, rel_tol=0.05)

    def test_with_reset_after(self):
        mock_with_exception = Mock(side_effect=[Exception] * 4 + [None])

        before = time.time()

        make_retryable = retryable(reset_after=2, exceptions=(Exception,))
        decorated_function = make_retryable(mock_with_exception)
        decorated_function()

        after = time.time() - before

        # We catch 4 exceptions, and reset after 2 seconds
        # 0.15 (first retry) + 0.70 (second retry) + 1.65 (third retry) + 0.15 (fourth retry)
        assert math.isclose(after, 2.65, rel_tol=0.05)

    def test_with_max_retries(self):
        mock_with_exception = Mock(side_effect=[Exception, Exception, None])

        make_retryable = retryable(max_retries=1, exceptions=(Exception,))
        decorated_function = make_retryable(mock_with_exception)

        with pytest.raises(Exception):
            decorated_function()
