# pylint: disable=no-self-use,redefined-outer-name

import time

import pytest

from mock import patch
from mockredis import mock_redis_client

from flashback.caching.adapters import RedisAdapter


@pytest.fixture
@patch("flashback.caching.adapters.redis_adapter.Redis", mock_redis_client)
def adapter():
    return RedisAdapter()


class TestRedisAdapter:
    def test_set(self, adapter):
        assert adapter.set("a", "1", -1)

    def test_batch_set(self, adapter):
        assert adapter.batch_set(["a", "b", "c"], ["1", "2", "3"], [-1, -1, -1])

    def test_get(self, adapter):
        adapter.set("a", "1", -1)

        item = adapter.get("a")

        assert item == "1"

    def test_get_expired(self, adapter):
        adapter.set("a", "1", 1)

        time.sleep(1)
        adapter.store.do_expire()

        item = adapter.get("a")

        assert item is None

    def test_batch_get(self, adapter):
        adapter.batch_set(["a", "b"], ["1", "2"], [-1, -1])

        items = adapter.batch_get(["a", "b"])

        assert len(items) == 2
        assert items == ["1", "2"]

    def test_batch_get_expired(self, adapter):
        adapter.batch_set(["a", "b"], ["1", "2"], [-1, 1])

        time.sleep(1)
        adapter.store.do_expire()

        items = adapter.batch_get(["a", "b"])

        assert len(items) == 2
        assert items == ["1", None]

    def test_delete(self, adapter):
        adapter.set("a", "1", -1)

        assert adapter.delete("a")

    def test_delete_expired(self, adapter):
        adapter.set("a", "1", 1)

        time.sleep(1)
        adapter.store.do_expire()

        assert not adapter.delete("a")

    def test_batch_delete(self, adapter):
        adapter.batch_set(["a", "b"], ["1", "2"], [-1, -1])

        assert adapter.batch_delete(["a", "b"])

    def test_batch_delete_expired(self, adapter):
        adapter.batch_set(["a", "b"], ["1", "2"], [-1, 1])

        time.sleep(1)
        adapter.store.do_expire()

        assert not adapter.batch_delete(["a", "b"])

    def test_exists(self, adapter):
        adapter.set("a", "1", -1)

        assert adapter.exists("a")

    def test_exists_expired(self, adapter):
        adapter.set("a", "1", 1)

        time.sleep(1)
        adapter.store.do_expire()

        assert not adapter.exists("a")

    def test_flush(self, adapter):
        adapter.set("a", "1", -1)
        adapter.flush()

        item = adapter.get("a")

        assert item is None

    def test_ping(self, adapter):
        assert adapter.ping()

    def test_exposed_exceptions(self):
        from flashback.caching.adapters.redis_adapter import RedisError    # pylint: disable=unused-import,import-outside-toplevel
