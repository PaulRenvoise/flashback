from typing import Any, Hashable, Literal, Optional, Sequence, Tuple

from pymemcache.client.base import Client  # type: ignore
from pymemcache.exceptions import MemcacheUnexpectedCloseError, MemcacheServerError, MemcacheUnknownError  # type: ignore
from pymemcache.exceptions import *  # pylint: disable=unused-wildcard-import,wildcard-import

from .base import BaseAdapter


class MemcachedAdapter(BaseAdapter):
    """
    Exposes a cache store using Memcached.

    Exposes `pymemcache`'s exceptions.
    """

    def __init__(self, host: str = "localhost", port: int = 11211, **kwargs: Any) -> None:
        super().__init__()

        self.store = Client((host, port), **kwargs)

    def set(self, key: Hashable, value: Any, ttl: int) -> bool:
        if ttl == -1:
            ttl = 0

        return self.store.set(key, value, expire=ttl)

    def batch_set(self, keys: Sequence[Hashable], values: Sequence[Any], ttls: Sequence[int]) -> bool:
        # There's two reasons to recode pymemcache.set_multi():
        # - It returns a list of keys that failed to be inserted, and the base expects a boolean
        # - It only allows a unique ttl for all keys
        commands = []

        encoding = self.store.encoding

        ttls = [0 if ttl == -1 else ttl for ttl in ttls]
        for key, value, ttl in zip(keys, values, ttls):
            checked_ttl = self.store._check_integer(ttl, "expire")  # pylint: disable=protected-access
            checked_key = self.store.check_key(key)
            checked_value, checked_flags = self.store.serde.serialize(key, value)


            command = b"set " + checked_key
            command += b" " + str(checked_flags).encode(encoding)
            command += b" " + checked_ttl
            command += b" " + str(len(checked_value)).encode(encoding) + b"\r\n"
            command += checked_value.encode(encoding) + b"\r\n"
            commands.append(command)

        results = self.store._misc_cmd(commands, "set", False)  # pylint: disable=protected-access

        for line in results:
            if line == b"NOT_STORED":
                return False

        return True

    def get(self, key: Hashable) -> Optional[Any]:
        value = self.store.get(key)

        return value

    def batch_get(self, keys: Sequence[Hashable]) -> Sequence[Optional[Any]]:
        key_to_value = self.store.get_multi(keys)
        values = [key_to_value[key] if key in key_to_value else None for key in keys]

        return values

    def delete(self, key: Hashable) -> bool:
        return self.store.delete(key, noreply=False)

    def batch_delete(self, keys: Sequence[Hashable]) -> bool:
        # Here as well, pymemcache.delete_multi() always returns True
        commands = []

        for key in keys:
            checked_key = self.store.check_key(key)

            command = b"delete " + checked_key +  b"\r\n"
            commands.append(command)

        results = self.store._misc_cmd(commands, "delete", False)  # pylint: disable=protected-access

        for line in results:
            if line == b"NOT_FOUND":
                return False

        return True

    def exists(self, key: Hashable) -> bool:
        # Can't just cast to bool since we can store falsey values
        return self.store.get(key) is not None

    def flush(self) -> Literal[True]:
        return self.store.flush_all(noreply=False)

    def ping(self) -> Literal[True]:
        # Raises if not connected or any connection error
        self.store.stats()

        return True

    @property
    def connection_exceptions(self) -> Tuple[Exception, ...]:
        return (MemcacheUnexpectedCloseError, MemcacheServerError, MemcacheUnknownError)
