# pylint: disable=no-self-use,redefined-outer-name

import time
from types import MethodType

import pytest
from mock import patch, Mock
from pymemcache.client.base import Client
from pymemcache.test.utils import MockMemcacheClient

from flashback.caching.adapters import MemcachedAdapter


@pytest.fixture
@patch('flashback.caching.adapters.memcached_adapter.Client', MockMemcacheClient)
def adapter():
    MockMemcacheClient._check_integer = Client._check_integer

    return MemcachedAdapter()


class TestMemcachedAdapter:
    def test_set(self, adapter):
        assert adapter.set('a', '1', -1)

    def test_batch_set(self, adapter):
        def mocked_misc_cmd(self, commands, name, noreply):
            results = []
            for command in commands:
                prefix, value = command.splitlines()
                _, key, flags, expire, length = prefix.split(b' ')

                self.set(key, value, int(expire))

                results.append(b'STORED')

            return results
        adapter.store._misc_cmd = MethodType(mocked_misc_cmd, adapter.store)

        assert adapter.batch_set(['a', 'b', 'c'], ['1', '2', '3'], [-1, -1, -1])

    def test_get(self, adapter):
        adapter.set('a', '1', -1)

        item = adapter.get('a')

        assert item == b'1'

    def test_get_expired(self, adapter):
        adapter.set('a', '1', 1)

        time.sleep(1)

        item = adapter.get('a')

        assert item is None

    def test_batch_get(self, adapter):
        def mocked_misc_cmd(self, commands, name, noreply):
            results = []
            for command in commands:
                prefix, value = command.splitlines()
                _, key, flags, expire, length = prefix.split(b' ')

                self.set(key, value, int(expire))

                results.append(b'STORED')

            return results
        adapter.store._misc_cmd = MethodType(mocked_misc_cmd, adapter.store)

        adapter.batch_set(['a', 'b'], ['1', '2'], [-1, -1])

        items = adapter.batch_get(['a', 'b'])

        assert len(items) == 2
        assert items == [b'1', b'2']

    def test_batch_get_expired(self, adapter):
        def mocked_misc_cmd(self, commands, name, noreply):
            results = []
            for command in commands:
                prefix, value = command.splitlines()
                _, key, flags, expire, length = prefix.split(b' ')

                self.set(key, value, int(expire))

                results.append(b'STORED')

            return results
        adapter.store._misc_cmd = MethodType(mocked_misc_cmd, adapter.store)

        adapter.batch_set(['a', 'b'], ['1', '2'], [-1, 1])

        time.sleep(1)

        items = adapter.batch_get(['a', 'b'])

        assert len(items) == 2
        assert items == [b'1', None]

    def test_delete(self, adapter):
        adapter.set('a', '1', -1)

        assert adapter.delete('a')

    def test_delete_expired(self, adapter):
        adapter.set('a', '1', 1)

        time.sleep(1)

        assert adapter.delete('a')

    def test_batch_delete(self, adapter):
        def mocked_misc_cmd(self, commands, name, noreply):
            results = []
            for command in commands:
                prefix, *value = command.splitlines()
                if prefix.startswith(b'set '):
                    _, key, flags, expire, length = prefix.split(b' ')

                    self.set(key, value[0], int(expire))

                    results.append(b'STORED')
                elif prefix.startswith(b'delete '):
                    _, key = prefix.split(b' ')

                    self.delete(key)

                    results.append(b'DELETED')

            return results
        adapter.store._misc_cmd = MethodType(mocked_misc_cmd, adapter.store)

        adapter.batch_set(['a', 'b'], ['1', '2'], [-1, -1])

        assert adapter.batch_delete(['a', 'b'])

    def test_batch_delete_expired(self, adapter):
        def mocked_misc_cmd(self, commands, name, noreply):
            results = []
            for command in commands:
                prefix, *value = command.splitlines()
                if prefix.startswith(b'set '):
                    _, key, flags, expire, length = prefix.split(b' ')

                    self.set(key, value[0], int(expire))

                    results.append(b'STORED')
                elif prefix.startswith(b'delete '):
                    _, key = prefix.split(b' ')

                    results.append(b'DELETED' if self.delete(key, False) else b'NOT_FOUND')

            return results
        adapter.store._misc_cmd = MethodType(mocked_misc_cmd, adapter.store)

        adapter.batch_set(['a', 'b'], ['1', '2'], [-1, 1])

        time.sleep(1)

        assert adapter.batch_get(['a', 'b']) == [b'1', None]
        assert not adapter.batch_delete(['a', 'b'])

    def test_exists(self, adapter):
        adapter.set('a', '1', -1)

        assert adapter.exists('a')

    def test_exists_expired(self, adapter):
        adapter.set('a', '1', 1)

        time.sleep(1)

        assert not adapter.exists('a')

    def test_flush(self, adapter):
        adapter.set('a', '1', -1)
        adapter.flush()

        item = adapter.get('a')

        assert item is None

    def test_ping(self, adapter):
        assert adapter.ping()

    def test_exposed_exceptions(self):
        from flashback.caching.adapters.memcached_adapter import MemcacheError    # pylint: disable=unused-import,import-outside-toplevel
