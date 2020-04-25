# pylint: disable=no-self-use,no-member,protected-access

from mock import patch
from mockredis import mock_redis_client

from copernicus.caching import cacheable


def dummy_func(left, right):
    return left + right


class TestCacheable:
    @patch('copernicus.caching.adapters.redis_adapter.Redis', mock_redis_client)
    def test_execution(self):
        assert callable(cacheable())
        assert callable(cacheable(adapter='redis'))

    @patch('copernicus.caching.Cache.set')
    @patch('copernicus.caching.Cache.get')
    def test_cache_miss(self, mocked_cache_get, mocked_cache_set):
        mocked_cache_get.side_effect = [None]
        mocked_cache_set.side_effect = [True]

        make_cacheable = cacheable()
        decorated_function = make_cacheable(dummy_func)

        decorated_function(1, 2)

        assert mocked_cache_get.called
        assert mocked_cache_set.called

    @patch('copernicus.caching.Cache.set')
    @patch('copernicus.caching.Cache.get')
    def test_cache_miss_with_type(self, mocked_cache_get, mocked_cache_set):
        mocked_cache_get.side_effect = [None, None, None]
        mocked_cache_set.side_effect = [True, True, True]

        make_cacheable = cacheable()
        decorated_function = make_cacheable(dummy_func)

        decorated_function(1, 2)

        assert mocked_cache_get.called
        assert mocked_cache_set.called

        decorated_function(True, 2)

        assert mocked_cache_get.called
        assert mocked_cache_set.called

        decorated_function('1', '2')

        assert mocked_cache_get.called
        assert mocked_cache_set.called

    @patch('copernicus.caching.Cache.set')
    @patch('copernicus.caching.Cache.get')
    def test_cache_miss_with_order(self, mocked_cache_get, mocked_cache_set):
        mocked_cache_get.side_effect = [None, None]
        mocked_cache_set.side_effect = [True, True]

        make_cacheable = cacheable()
        decorated_function = make_cacheable(dummy_func)

        decorated_function(1, 2)

        assert mocked_cache_get.called
        assert mocked_cache_set.called

        decorated_function(2, 1)

        assert mocked_cache_get.called
        assert mocked_cache_set.called

    @patch('copernicus.caching.Cache.set')
    @patch('copernicus.caching.Cache.get')
    def test_cache_hit(self, mocked_cache_get, mocked_cache_set):
        mocked_cache_get.side_effect = [None, 3]
        mocked_cache_set.side_effect = [True]

        make_cacheable = cacheable()
        decorated_function = make_cacheable(dummy_func)

        decorated_function(1, 2)

        # Erase the calls made by the first call to `decorated_function`
        mocked_cache_get.reset_mock()
        mocked_cache_set.reset_mock()

        decorated_function(1, 2)

        assert mocked_cache_get.called
        assert not mocked_cache_set.called
