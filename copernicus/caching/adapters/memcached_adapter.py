from pymemcache.client.base import Client
from pymemcache.exceptions import * # pylint: disable=wildcard-import,unused-wildcard-import

from .base import BaseAdapter


class MemcachedAdapter(BaseAdapter):
    """
    Exposes a cache store using Memcached.

    Exposes `pymemcache`'s exceptions.
    """

    def __init__(self, host='localhost', port=11211, **kwargs):
        super().__init__()

        self.store = Client((host, port), **kwargs)

    def set(self, key, value):
        return self.store.set(key, value)

    def batch_set(self, keys, values):
        # pymemcache returns a list of the keys that failed to be inserted,
        # we convert that to a boolean
        return not bool(self.store.set_multi(dict(zip(keys, values))))

    def get(self, key):
        value = self.store.get(key)

        return value

    def batch_get(self, keys):
        key_to_value = self.store.get_multi(keys)
        values = [key_to_value[key] if key in key_to_value else None for key in keys]

        return values

    def delete(self, key):
        return self.store.delete(key, noreply=False)

    def batch_delete(self, keys):
        # We do not use `pymemcache`'s `delete_multi` since it always return True
        return False not in [self.store.delete(key, noreply=False) for key in keys]

    def exists(self, key):
        # Can't just cast to bool since we can store falsey values
        return self.store.get(key) is not None

    def flush(self):
        return self.store.flush_all(noreply=False)

    def ping(self):
        return bool(self.store.stats())

    @property
    def connection_exceptions(self):
        return (MemcacheUnexpectedCloseError, MemcacheServerError, MemcacheUnknownError)
