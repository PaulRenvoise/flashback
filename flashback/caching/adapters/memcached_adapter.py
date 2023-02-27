from pymemcache.client.base import Client
from pymemcache.exceptions import *  # pylint: disable=wildcard-import,unused-wildcard-import

from .base import BaseAdapter


class MemcachedAdapter(BaseAdapter):
    """
    Exposes a cache store using Memcached.

    Exposes `pymemcache`'s exceptions.
    """

    def __init__(self, host="localhost", port=11211, **kwargs):
        super().__init__()

        self.store = Client((host, port), **kwargs)

    def set(self, key, value, ttl):
        if ttl == -1:
            ttl = 0

        return self.store.set(key, value, expire=ttl)

    def batch_set(self, keys, values, ttls):
        # There's two reasons to recode pymemcache.set_multi():
        # - It returns a list of keys that failed to be inserted, and the base expects a boolean
        # - It only allows a unique ttl for all keys
        commands = []

        ttls = [0 if ttl == -1 else ttl for ttl in ttls]
        for key, value, ttl in zip(keys, values, ttls):
            ttl = self.store._check_integer(ttl, "expire")  # pylint: disable=protected-access
            key = self.store.check_key(key)
            value, flags = self.store.serde.serialize(key, value)

            command = b"set " + key
            command += b" " + str(flags).encode(self.store.encoding)
            command += b" " + ttl
            command += b" " + str(len(value)).encode(self.store.encoding) + b"\r\n"
            command += value.encode(self.store.encoding) + b"\r\n"
            commands.append(command)

        results = self.store._misc_cmd(commands, "set", False)  # pylint: disable=protected-access

        for line in results:
            if line == b"NOT_STORED":
                return False

        return True

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
        # Here as well, pymemcache.delete_multi() always returns True
        commands = []

        for key in keys:
            key = self.store.check_key(key)

            command = b"delete " + key +  b"\r\n"
            commands.append(command)

        results = self.store._misc_cmd(commands, "delete", False)  # pylint: disable=protected-access

        for line in results:
            if line == b"NOT_FOUND":
                return False

        return True

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
