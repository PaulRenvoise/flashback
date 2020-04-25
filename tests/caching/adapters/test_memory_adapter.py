# pylint: disable=no-self-use,redefined-outer-name

import pytest

from flashback.caching.adapters import MemoryAdapter


@pytest.fixture
def adapter():
    return MemoryAdapter()


class TestMemoryAdapter:
    def test_set(self, adapter):
        assert adapter.set('a', 1)

    def test_batch_set(self, adapter):
        assert adapter.batch_set(['a', 'b', 'c'], [1, 2, 3])

    def test_get(self, adapter):
        adapter.set('a', 1)

        item = adapter.get('a')

        assert item == 1

    def test_get_empty(self, adapter):
        item = adapter.get('z')

        assert item is None

    def test_batch_get(self, adapter):
        adapter.batch_set(['a', 'b'], [1, 2])

        items = adapter.batch_get(['a', 'b'])

        assert len(items) == 2
        assert items == [1, 2]

    def test_batch_get_partial(self, adapter):
        adapter.set('a', 1)

        items = adapter.batch_get(['a', 'z'])

        assert len(items) == 2
        assert items == [1, None]

    def test_batch_get_empty(self, adapter):
        items = adapter.batch_get(['a', 'z'])

        assert len(items) == 2
        assert items == [None, None]

    def test_delete(self, adapter):
        adapter.set('a', 1)

        assert adapter.delete('a')

    def test_delete_empty(self, adapter):
        assert not adapter.delete('z')

    def test_batch_delete(self, adapter):
        adapter.batch_set(['a', 'b'], [1, 2])

        assert adapter.batch_delete(['a', 'b'])

    def test_batch_delete_partial(self, adapter):
        adapter.set('a', 1)

        assert not adapter.batch_delete(['a', 'z'])

    def test_batch_delete_empty(self, adapter):
        assert not adapter.batch_delete(['a', 'b'])

    def test_exists(self, adapter):
        adapter.set('a', 1)

        assert adapter.exists('a')

    def test_exists_empty(self, adapter):
        assert not adapter.exists('z')

    def test_flush(self, adapter):
        adapter.set('a', 1)
        adapter.flush()

        item = adapter.get('a')

        assert item is None

    def test_ping(self, adapter):
        assert adapter.ping()
