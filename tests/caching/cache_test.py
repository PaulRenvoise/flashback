from unittest.mock import patch, Mock

import pytest
from mockredis import mock_redis_client
from pymemcache.test.utils import MockMemcacheClient

from flashback.caching import Cache


@pytest.fixture
def cache() -> Cache:
    return Cache()


class CacheTest:
    class InitTest:
        @patch("flashback.caching.adapters.redis_adapter.Redis", mock_redis_client)
        @patch("flashback.caching.adapters.memcached_adapter.Client", MockMemcacheClient)
        def simple_test(self) -> None:
            cache = Cache()

            assert cache.ping()

            cache = Cache(adapter="redis")

            assert cache.ping()

            cache = Cache(adapter="memcached")

            assert cache.ping()

        @patch.object(Cache, "flush")
        def with_flush_test(self, mocked_flush: Mock) -> None:
            cache = Cache(flush=True)

            assert mocked_flush.called
            assert cache.ping()

        def with_ttl_test(self) -> None:
            cache = Cache(ttl=10)

            assert cache.ping()

        def invalid_test(self) -> None:
            with pytest.raises(NotImplementedError):
                Cache(adapter="dummy")

    class SetTest:
        def ttl_test(self, cache: Cache) -> None:
            assert cache.set("a", "a", 1)

        def str_test(self, cache: Cache) -> None:
            assert cache.set("a", "a")

        def int_test(self, cache: Cache) -> None:
            assert cache.set("a", 1)

        def float_test(self, cache: Cache) -> None:
            assert cache.set("a", 1.0)

        def bool_test(self, cache: Cache) -> None:
            assert cache.set("a", True)

        def list_test(self, cache: Cache) -> None:
            assert cache.set("a", ["a", 1, False])

        def dict_test(self, cache: Cache) -> None:
            assert cache.set("a", {"a": 1})

    class BatchSetTest:
        def simple_test(self, cache: Cache) -> None:
            assert cache.batch_set(["a", "b"], [1, 2])

        def ttls_test(self, cache: Cache) -> None:
            assert cache.batch_set(["a", "b"], [1, 2], [1, 1])

        def invalid_test(self, cache: Cache) -> None:
            with pytest.raises(ValueError):  # noqa: PT011
                cache.batch_set(["a"], [1, 2])

    class GetTest:
        def str_test(self, cache: Cache) -> None:
            cache.set("a", "abc")

            item = cache.get("a")

            assert item == "abc"

        def int_test(self, cache: Cache) -> None:
            cache.set("a", 1)

            item = cache.get("a")

            assert item == "1"

        def float_test(self, cache: Cache) -> None:
            cache.set("a", 1.0)

            item = cache.get("a")

            assert item == "1.0"

        def bool_test(self, cache: Cache) -> None:
            cache.set("a", True)

            item = cache.get("a")

            assert item is True

        def list_test(self, cache: Cache) -> None:
            cache.set("a", ["a", 1, False])

            item = cache.get("a")

            assert item == ["a", 1, False]

        def dict_test(self, cache: Cache) -> None:
            cache.set("a", {"a": 1})

            item = cache.get("a")

            assert item == {"a": 1}

        def empty_test(self, cache: Cache) -> None:
            item = cache.get("z")

            assert item is None

    class BatchGetTest:
        def simple_test(self, cache: Cache) -> None:
            cache.batch_set(["a", "b"], [1, 2])

            items = cache.batch_get(["a", "b"])

            assert len(items) == 2
            assert items == ["1", "2"]

        def partial_test(self, cache: Cache) -> None:
            cache.set("a", 1)

            items = cache.batch_get(["a", "z"])

            assert len(items) == 2
            assert items == ["1", None]

    class DeleteTest:
        def simple_test(self, cache: Cache) -> None:
            cache.set("a", 1)

            assert cache.delete("a")

        def empty_test(self, cache: Cache) -> None:
            assert not cache.delete("z")

    class BatchDeleteTest:
        def simple_test(self, cache: Cache) -> None:
            cache.batch_set(["d", "e"], [1, 2])

            assert cache.batch_delete(["d", "e"])

        def partial_test(self, cache: Cache) -> None:
            cache.set("a", 1)

            assert not cache.batch_delete(["a", "z"])

    class ExistsTest:
        def simple_test(self, cache: Cache) -> None:
            cache.set("a", 1)

            assert cache.exists("a")

        def empty_test(self, cache: Cache) -> None:
            assert not cache.exists("z")

    class FlushTest:
        def simple_test(self, cache: Cache) -> None:
            cache.set("a", 1)
            cache.flush()

            item = cache.get("a")

            assert item is None

    class PingTest:
        def simple_test(self, cache: Cache) -> None:
            assert cache.ping()
