import json

from .base import BaseAdapter


class MemoryAdapter(BaseAdapter):
    """
    Exposes a cache store using a in-memory dict.
    """

    def __init__(self, **kwargs):
        super().__init__()

        self.store = {}

    def set(self, key, value):
        self.store[key] = value

        return True

    def batch_set(self, keys, values):
        self.store.update(dict(zip(keys, [value for value in values])))

        return True

    def get(self, key):
        return self.store.get(key, None)

    def batch_get(self, keys):
        return [self.store.get(key, None) for key in keys]

    def delete(self, key):
        return bool(self.store.pop(key, False))

    def batch_delete(self, keys):
        res = [bool(self.store.pop(key, False)) for key in keys]

        # If we have one False, we need to return False
        return not False in res

    def exists(self, key):
        return key in self.store

    def flush(self):
        self.store.clear()

        return True

    def ping(self):
        return True

    @property
    def connection_exceptions(self):
        return ()
