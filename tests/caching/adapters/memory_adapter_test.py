import time

import pytest

from flashback.caching.adapters import MemoryAdapter


@pytest.fixture
def adapter() -> MemoryAdapter:
    return MemoryAdapter()


class MemoryAdapterTest:
    def set_test(self, adapter: MemoryAdapter) -> None:
        assert adapter.set("a", "1", -1)

    def batch_set_test(self, adapter: MemoryAdapter) -> None:
        assert adapter.batch_set(["a", "b", "c"], ["1", "1", "1"], [-1, -1, -1])

    def get_test(self, adapter: MemoryAdapter) -> None:
        adapter.set("a", "1", -1)

        item = adapter.get("a")

        assert item == "1"

    def get_expired_test(self, adapter: MemoryAdapter) -> None:
        adapter.set("a", "1", 1)

        time.sleep(1)

        item = adapter.get("a")

        assert item is None

    def batch_get_test(self, adapter: MemoryAdapter) -> None:
        adapter.batch_set(["a", "b"], ["1", "2"], [-1, -1])

        items = adapter.batch_get(["a", "b"])

        assert len(items) == 2
        assert items == ["1", "2"]

    def batch_get_expired_test(self, adapter: MemoryAdapter) -> None:
        adapter.batch_set(["a", "b"], ["1", "2"], [-1, 1])

        time.sleep(1)

        items = adapter.batch_get(["a", "b"])

        assert len(items) == 2
        assert items == ["1", None]

    def delete_test(self, adapter: MemoryAdapter) -> None:
        adapter.set("a", "1", -1)

        assert adapter.delete("a")

    def delete_expired_test(self, adapter: MemoryAdapter) -> None:
        adapter.set("a", "1", 1)

        time.sleep(1)

        assert not adapter.delete("a")

    def batch_delete_test(self, adapter: MemoryAdapter) -> None:
        adapter.batch_set(["a", "b"], ["1", "2"], [-1, -1])

        assert adapter.batch_delete(["a", "b"])

    def batch_delete_expired_test(self, adapter: MemoryAdapter) -> None:
        adapter.batch_set(["a", "b"], ["1", "2"], [-1, 1])

        time.sleep(1)

        assert not adapter.batch_delete(["a", "b"])

    def exists_test(self, adapter: MemoryAdapter) -> None:
        adapter.set("a", "1", -1)

        assert adapter.exists("a")

    def exists_expired_test(self, adapter: MemoryAdapter) -> None:
        adapter.set("a", "1", 1)

        time.sleep(1)

        assert not adapter.exists("a")

    def flush_test(self, adapter: MemoryAdapter) -> None:
        adapter.set("a", "1", -1)
        adapter.flush()

        item = adapter.get("a")

        assert item is None

    def ping_test(self, adapter: MemoryAdapter) -> None:
        assert adapter.ping()
