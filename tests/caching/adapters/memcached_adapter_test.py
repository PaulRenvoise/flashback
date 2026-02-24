from unittest.mock import patch
import time

import pytest
from pymemcache.client.base import Client
from pymemcache.test.utils import MockMemcacheClient

from flashback.caching.adapters import MemcachedAdapter


@pytest.fixture
@patch("flashback.caching.adapters.memcached_adapter.Client", MockMemcacheClient)
def adapter() -> MemcachedAdapter:
    MockMemcacheClient._check_integer = Client._check_integer  # noqa: SLF001

    # Custom implementation of _misc_cmd because MockMemcacheClient doesn't implement it
    def mocked_misc_cmd(self, commands, name, _noreply) -> list[bytes]:
        results = []
        for command in commands:
            prefix, *value = command.splitlines()
            if name == b"set":
                _, key, _, expire, _ = prefix.split(b" ")

                self.set(key, value[0], int(expire))

                results.append(b"STORED")
            elif name == b"delete":
                _, key = prefix.split(b" ")

                results.append(b"DELETED" if self.delete(key, False) else b"NOT_FOUND")

        return results

    MockMemcacheClient._misc_cmd = mocked_misc_cmd  # noqa: SLF001

    return MemcachedAdapter()


class MemcachedAdapterTest:
    def set_test(self, adapter: MemcachedAdapter) -> None:
        assert adapter.set("a", "1", -1)

    def batch_set_test(self, adapter: MemcachedAdapter) -> None:
        assert adapter.batch_set(["a", "b", "c"], ["1", "2", "3"], [-1, -1, -1])

    def get_test(self, adapter: MemcachedAdapter) -> None:
        adapter.set("a", "1", -1)

        item = adapter.get("a")

        assert item == b"1"

    def get_expired_test(self, adapter: MemcachedAdapter) -> None:
        adapter.set("a", "1", 1)

        time.sleep(1)

        item = adapter.get("a")

        assert item is None

    def batch_get_test(self, adapter: MemcachedAdapter) -> None:
        adapter.batch_set(["a", "b"], ["1", "2"], [-1, -1])

        items = adapter.batch_get(["a", "b"])

        assert len(items) == 2
        assert items == [b"1", b"2"]

    def batch_get_expired_test(self, adapter: MemcachedAdapter) -> None:
        adapter.batch_set(["a", "b"], ["1", "2"], [-1, 1])

        time.sleep(1)

        items = adapter.batch_get(["a", "b"])

        assert len(items) == 2
        assert items == [b"1", None]

    def delete_test(self, adapter: MemcachedAdapter) -> None:
        adapter.set("a", "1", -1)

        assert adapter.delete("a")

    def delete_expired_test(self, adapter: MemcachedAdapter) -> None:
        adapter.set("a", "1", 1)

        time.sleep(1)

        assert adapter.delete("a")

    def batch_delete_test(self, adapter: MemcachedAdapter) -> None:
        adapter.batch_set(["a", "b"], ["1", "2"], [-1, -1])

        assert adapter.batch_delete(["a", "b"])

    def batch_delete_expired_test(self, adapter: MemcachedAdapter) -> None:
        adapter.batch_set(["a", "b"], ["1", "2"], [-1, 1])

        time.sleep(1)

        assert adapter.batch_get(["a", "b"]) == [b"1", None]
        assert not adapter.batch_delete(["a", "b"])

    def exists_test(self, adapter: MemcachedAdapter) -> None:
        adapter.set("a", "1", -1)

        assert adapter.exists("a")

    def exists_expired_test(self, adapter: MemcachedAdapter) -> None:
        adapter.set("a", "1", 1)

        time.sleep(1)

        assert not adapter.exists("a")

    def flush_test(self, adapter: MemcachedAdapter) -> None:
        adapter.set("a", "1", -1)
        adapter.flush()

        item = adapter.get("a")

        assert item is None

    def ping_test(self, adapter: MemcachedAdapter) -> None:
        assert adapter.ping()

    def exposed_exceptions_test(self) -> None:
        from flashback.caching.adapters.memcached_adapter import MemcacheError  # noqa: F401, PLC0415
