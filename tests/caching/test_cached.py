# pylint: disable=no-member,protected-access

from mock import patch
from mockredis import mock_redis_client

from flashback.caching import cached


def dummy_func(left, right):
    return left + right


class TestCached:
    @patch("flashback.caching.adapters.redis_adapter.Redis", mock_redis_client)
    def test_execution(self):
        assert callable(cached())
        assert callable(cached(adapter="redis"))

    @patch("flashback.caching.Cache.set")
    @patch("flashback.caching.Cache.get")
    def test_cache_miss(self, mocked_cache_get, mocked_cache_set):
        mocked_cache_get.side_effect = [None]
        mocked_cache_set.side_effect = [True]

        make_cacheable = cached()
        decorated_function = make_cacheable(dummy_func)

        decorated_function(1, 2)

        assert mocked_cache_get.called
        assert mocked_cache_set.called

    @patch("flashback.caching.Cache.set")
    @patch("flashback.caching.Cache.get")
    def test_cache_miss_with_type(self, mocked_cache_get, mocked_cache_set):
        mocked_cache_get.side_effect = [None, None, None]
        mocked_cache_set.side_effect = [True, True, True]

        make_cacheable = cached()
        decorated_function = make_cacheable(dummy_func)

        decorated_function(1, 2)

        assert mocked_cache_get.called
        assert mocked_cache_set.called

        decorated_function(True, 2)

        assert mocked_cache_get.called
        assert mocked_cache_set.called

        decorated_function("1", "2")

        assert mocked_cache_get.called
        assert mocked_cache_set.called

    @patch("flashback.caching.Cache.set")
    @patch("flashback.caching.Cache.get")
    def test_cache_miss_with_order(self, mocked_cache_get, mocked_cache_set):
        mocked_cache_get.side_effect = [None, None]
        mocked_cache_set.side_effect = [True, True]

        make_cacheable = cached()
        decorated_function = make_cacheable(dummy_func)

        decorated_function(1, 2)

        assert mocked_cache_get.called
        assert mocked_cache_set.called

        decorated_function(2, 1)

        assert mocked_cache_get.called
        assert mocked_cache_set.called

    @patch("flashback.caching.Cache.set")
    @patch("flashback.caching.Cache.get")
    def test_cache_hit(self, mocked_cache_get, mocked_cache_set):
        mocked_cache_get.side_effect = [None, 3]
        mocked_cache_set.side_effect = [True]

        make_cacheable = cached()
        decorated_function = make_cacheable(dummy_func)

        decorated_function(1, 2)

        # Erase the calls made by the first call to `decorated_function`
        mocked_cache_get.reset_mock()
        mocked_cache_set.reset_mock()

        decorated_function(1, 2)

        assert mocked_cache_get.called
        assert not mocked_cache_set.called
