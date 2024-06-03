from __future__ import annotations

from collections.abc import Sequence
from datetime import datetime, timedelta
from threading import RLock
from typing import Any

from .base import BaseAdapter


class MemoryAdapter(BaseAdapter):
    """
    Exposes a cache store using a in-memory dict.
    """

    def __init__(self, **_kwargs) -> None:
        super().__init__()

        self._lock = RLock()
        self.store = {}

    def set(self, key: str, value: Any, ttl: int) -> bool:
        if ttl == -1:
            expiry = None
        else:
            # TODO: use relativedelta
            expiry = datetime.timestamp(datetime.now() + timedelta(seconds=ttl))

        with self._lock:
            self.store[key] = (value, expiry)

        return True

    def batch_set(self, keys: Sequence[str], values: Sequence[Any], ttls: Sequence[int]) -> bool:
        now = datetime.now()
        expiries = [None if ttl == -1 else datetime.timestamp(now + timedelta(seconds=ttl)) for ttl in ttls]

        values = zip(values, expiries)

        with self._lock:
            self.store.update(dict(zip(keys, values)))

        return True

    def get(self, key: str) -> Any | None:
        self._evict()

        return self.store.get(key, (None,))[0]

    def batch_get(self, keys: Sequence[str]) -> Sequence[Any | None]:
        self._evict()

        return [self.store.get(key, (None,))[0] for key in keys]

    def delete(self, key: str) -> bool:
        self._evict()

        with self._lock:
            value = self.store.pop(key, False)

        return bool(value)

    def batch_delete(self, keys: Sequence[str]) -> bool:
        self._evict()

        with self._lock:
            res = [bool(self.store.pop(key, False)) for key in keys]

        return False not in res

    def exists(self, key: str) -> bool:
        self._evict()

        return key in self.store

    def flush(self) -> bool:
        self.store.clear()

        return True

    def ping(self) -> bool:
        return True

    @property
    def connection_exceptions(self) -> tuple[Exception, ...]:
        return ()

    def _evict(self) -> None:
        now = datetime.timestamp(datetime.now())

        expired_keys = set()

        for key, (_, expiry) in self.store.items():
            if expiry is not None and expiry < now:
                expired_keys.add(key)

        with self._lock:
            for expired_key in expired_keys:
                del self.store[expired_key]
