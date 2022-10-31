from datetime import datetime, timedelta
from threading import RLock
from typing import Any, Dict, Hashable, Literal, Optional, Sequence, Tuple

from .base import BaseAdapter


class MemoryAdapter(BaseAdapter):
    """
    Exposes a cache store using a in-memory dict.
    """

    def __init__(self, **kwargs: Any) -> None:
        super().__init__()

        self._lock = RLock()
        self.store: Dict[Hashable, Any] = {}

    def set(self, key: Hashable, value: Any, ttl: int) -> bool:
        if ttl == -1:
            expiry = None
        else:
            expiry = datetime.timestamp(datetime.now() + timedelta(seconds=ttl))

        with self._lock:
            self.store[key] = (value, expiry)

        return True

    def batch_set(self, keys: Sequence[Hashable], values: Sequence[Any], ttls: Sequence[int]) -> bool:
        now = datetime.now()
        expiries = [None if ttl == -1 else datetime.timestamp(now + timedelta(seconds=ttl)) for ttl in ttls]

        values_expiries = zip(values, expiries)

        with self._lock:
            self.store.update(dict(zip(keys, values_expiries)))

        return True

    def get(self, key: Hashable) -> Optional[Any]:
        self._evict()

        return self.store.get(key, (None,))[0]

    def batch_get(self, keys: Sequence[Hashable]) -> Sequence[Optional[Any]]:
        self._evict()

        return [self.store.get(key, (None,))[0] for key in keys]

    def delete(self, key: Hashable) -> bool:
        self._evict()

        with self._lock:
            value = self.store.pop(key, False)

        return bool(value)

    def batch_delete(self, keys: Sequence[Hashable]) -> bool:
        self._evict()

        with self._lock:
            res = [bool(self.store.pop(key, False)) for key in keys]

        return False not in res

    def exists(self, key: Hashable) -> bool:
        self._evict()

        return key in self.store

    def flush(self) -> Literal[True]:
        self.store.clear()

        return True

    def ping(self) -> Literal[True]:
        return True

    @property
    def connection_exceptions(self) -> Tuple:
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
