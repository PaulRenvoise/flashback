from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from pymemcache.client.base import Client
from pymemcache.exceptions import *  # noqa: F403

from .base import BaseAdapter


class MemcachedAdapter(BaseAdapter):
    """
    Exposes a cache store using Memcached.

    Exposes `pymemcache`'s exceptions.
    """

    def __init__(self, host: str = "localhost", port: int = 11211, **kwargs) -> None:
        super().__init__()

        self.store = Client((host, port), **kwargs)

    def set(self, key: str, value: Any, ttl: int) -> bool:
        if ttl == -1:
            ttl = 0

        return self.store.set(key, value, expire=ttl)

    def batch_set(self, keys: Sequence[str], values: Sequence[Any], ttls: Sequence[int]) -> bool:
        # There's two reasons to recode pymemcache.set_multi():
        # - It returns a list of keys that failed to be inserted, and the base expects a boolean
        # - It only allows a unique ttl for all keys
        commands = []

        ttls = [0 if ttl == -1 else ttl for ttl in ttls]
        for key, value, ttl in zip(keys, values, ttls):
            stored_ttl = self.store._check_integer(ttl, "expire")  # noqa: SLF001
            stored_key = self.store.check_key(key)
            stored_value, stored_flags = self.store.serde.serialize(key, value)

            command = b"set " + stored_key
            command += b" " + str(stored_flags).encode(self.store.encoding)
            command += b" " + stored_ttl
            command += b" " + str(len(stored_value)).encode(self.store.encoding) + b"\r\n"
            command += stored_value.encode(self.store.encoding) + b"\r\n"
            commands.append(command)

        results = self.store._misc_cmd(commands, "set", False)  # noqa: SLF001

        return all(line != b"NOT_STORED" for line in results)

    def get(self, key: str) -> Any | None:
        return self.store.get(key)

    def batch_get(self, keys: Sequence[str]) -> Sequence[Any | None]:
        key_to_value = self.store.get_multi(keys)
        return [key_to_value.get(key, None) for key in keys]

    def delete(self, key: str) -> bool:
        return self.store.delete(key, noreply=False)

    def batch_delete(self, keys: Sequence[str]) -> bool:
        # Here as well, pymemcache.delete_multi() always returns True
        commands = []

        for key in keys:
            stored_key = self.store.check_key(key)

            command = b"delete " + stored_key + b"\r\n"
            commands.append(command)

        results = self.store._misc_cmd(commands, "delete", False)  # noqa: SLF001

        return all(line != b"NOT_FOUND" for line in results)

    def exists(self, key: str) -> bool:
        # Can't just cast to bool since we can store falsey values
        return self.store.get(key) is not None

    def flush(self) -> bool:
        return self.store.flush_all(noreply=False)

    def ping(self) -> bool:
        return bool(self.store.stats())

    @property
    def connection_exceptions(self) -> tuple[Exception, ...]:
        return (MemcacheUnexpectedCloseError, MemcacheServerError, MemcacheUnknownError)  # noqa: F405
