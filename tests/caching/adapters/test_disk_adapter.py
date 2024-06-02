import time

import pytest

from flashback.caching.adapters import DiskAdapter


@pytest.fixture()
def adapter():
    return DiskAdapter()


class TestDiskAdapter:
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

        items = adapter.batch_get(["a", "b"])

        assert len(items) == 2
        assert items == ["1", None]

    def test_delete(self, adapter):
        adapter.set("a", "1", -1)

        assert adapter.delete("a")

    def test_delete_expired(self, adapter):
        adapter.set("a", "1", 1)

        time.sleep(1)

        assert not adapter.delete("a")

    def test_batch_delete(self, adapter):
        adapter.batch_set(["a", "b"], ["1", "2"], [-1, -1])

        assert adapter.batch_delete(["a", "b"])

    def test_batch_delete_expired(self, adapter):
        adapter.batch_set(["a", "b"], ["1", "2"], [-1, 1])

        time.sleep(1)

        assert not adapter.batch_delete(["a", "b"])

    def test_exists(self, adapter):
        adapter.set("a", "1", -1)

        assert adapter.exists("a")

    def test_exists_expired(self, adapter):
        adapter.set("a", "1", 1)

        time.sleep(1)

        assert not adapter.exists("a")

    def test_flush(self, adapter):
        adapter.set("a", "1", -1)
        adapter.flush()

        item = adapter.get("a")

        assert item is None

    def test_ping(self, adapter):
        assert adapter.ping()
