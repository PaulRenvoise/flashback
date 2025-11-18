from unittest.mock import patch

import pytest
from mockredis import mock_redis_client
from pymemcache.test.utils import MockMemcacheClient

from flashback.caching import Cache


@pytest.fixture
def cache():
    return Cache()


class TestCache:
    @patch("flashback.caching.adapters.redis_adapter.Redis", mock_redis_client)
    @patch("flashback.caching.adapters.memcached_adapter.Client", MockMemcacheClient)
    def test_init(self):
        cache = Cache()

        assert cache.ping()

        cache = Cache(adapter="redis")

        assert cache.ping()

        cache = Cache(adapter="memcached")

        assert cache.ping()

    @patch.object(Cache, "flush")
    def test_init_with_flush(self, mocked_flush):
        cache = Cache(flush=True)

        assert mocked_flush.called
        assert cache.ping()

    def test_init_with_ttl(self):
        cache = Cache(ttl=10)

        assert cache.ping()

    def test_init_invalid(self):
        with pytest.raises(NotImplementedError):
            Cache(adapter="dummy")

    def test_set_ttl(self, cache):
        assert cache.set("a", "a", 1)

    def test_set_str(self, cache):
        assert cache.set("a", "a")

    def test_set_int(self, cache):
        assert cache.set("a", 1)

    def test_set_float(self, cache):
        assert cache.set("a", 1.0)

    def test_set_bool(self, cache):
        assert cache.set("a", True)

    def test_set_list(self, cache):
        assert cache.set("a", ["a", 1, False])

    def test_set_dict(self, cache):
        assert cache.set("a", {"a": 1})

    def test_batch_set(self, cache):
        assert cache.batch_set(["a", "b"], [1, 2])

    def test_batch_set_ttls(self, cache):
        assert cache.batch_set(["a", "b"], [1, 2], [1, 1])

    def test_batch_set_invalid(self, cache):
        with pytest.raises(ValueError):  # noqa: PT011
            cache.batch_set(["a"], [1, 2])

    def test_get_str(self, cache):
        cache.set("a", "abc")

        item = cache.get("a")

        assert item == "abc"

    def test_get_int(self, cache):
        cache.set("a", 1)

        item = cache.get("a")

        assert item == "1"

    def test_get_float(self, cache):
        cache.set("a", 1.0)

        item = cache.get("a")

        assert item == "1.0"

    def test_get_bool(self, cache):
        cache.set("a", True)

        item = cache.get("a")

        assert item is True

    def test_get_list(self, cache):
        cache.set("a", ["a", 1, False])

        item = cache.get("a")

        assert item == ["a", 1, False]

    def test_get_dict(self, cache):
        cache.set("a", {"a": 1})

        item = cache.get("a")

        assert item == {"a": 1}

    def test_get_empty(self, cache):
        item = cache.get("z")

        assert item is None

    def test_batch_get(self, cache):
        cache.batch_set(["a", "b"], [1, 2])

        items = cache.batch_get(["a", "b"])

        assert len(items) == 2
        assert items == ["1", "2"]

    def test_batch_get_partial(self, cache):
        cache.set("a", 1)

        items = cache.batch_get(["a", "z"])

        assert len(items) == 2
        assert items == ["1", None]

    def test_delete(self, cache):
        cache.set("a", 1)

        assert cache.delete("a")

    def test_delete_empty(self, cache):
        assert not cache.delete("z")

    def test_batch_delete(self, cache):
        cache.batch_set(["d", "e"], [1, 2])

        assert cache.batch_delete(["d", "e"])

    def test_batch_delete_partial(self, cache):
        cache.set("a", 1)

        assert not cache.batch_delete(["a", "z"])

    def test_exists(self, cache):
        cache.set("a", 1)

        assert cache.exists("a")

    def test_exists_empty(self, cache):
        assert not cache.exists("z")

    def test_flush(self, cache):
        cache.set("a", 1)
        cache.flush()

        item = cache.get("a")

        assert item is None

    def test_ping(self, cache):
        assert cache.ping()
