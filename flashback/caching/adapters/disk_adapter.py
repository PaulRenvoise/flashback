from contextlib import contextmanager
from datetime import datetime, timedelta
from fcntl import flock, LOCK_SH, LOCK_EX, LOCK_UN
from typing import Any, Generator, Hashable, Literal, Optional, Sequence, Tuple
import shelve
import tempfile
import uuid

from .base import BaseAdapter


class DiskAdapter(BaseAdapter):
    """
    Exposes a cache store using a locked shelf.

    See: https://docs.python.org/3/library/shelve.html.
    """

    def __init__(self, **kwargs: Any) -> None:
        super().__init__()

        self._store_path = f"{tempfile.gettempdir()}/{uuid.uuid4()}"

    def set(self, key: Hashable, value: Any, ttl: int) -> bool:
        if ttl == -1:
            expiry = None
        else:
            expiry = datetime.timestamp(datetime.now() + timedelta(seconds=ttl))

        with self._open_locked_store(LOCK_EX) as store:
            store[key] = (value, expiry)

        return True

    def batch_set(self, keys: Sequence[Hashable], values: Sequence[Any], ttls: Sequence[int]) -> bool:
        now = datetime.now()
        expiries = [None if ttl == -1 else datetime.timestamp(now + timedelta(seconds=ttl)) for ttl in ttls]

        values_expiries = zip(values, expiries)

        with self._open_locked_store(LOCK_EX) as store:
            store.update(dict(zip(keys, values_expiries)))

        return True

    def get(self, key: Hashable) -> Optional[Any]:
        self._evict()

        with self._open_locked_store(LOCK_SH) as store:
            return store.get(key, (None,))[0]

    def batch_get(self, keys: Sequence[Hashable]) -> Sequence[Optional[Any]]:
        self._evict()

        with self._open_locked_store(LOCK_SH) as store:
            return [store.get(key, (None,))[0] for key in keys]

    def delete(self, key: Hashable) -> bool:
        self._evict()

        with self._open_locked_store(LOCK_EX) as store:
            return bool(store.pop(key, False))

    def batch_delete(self, keys: Sequence[Hashable]) -> bool:
        self._evict()

        with self._open_locked_store(LOCK_EX) as store:
            res = [bool(store.pop(key, False)) for key in keys]

        return False not in res

    def exists(self, key: Hashable) -> bool:
        self._evict()

        with self._open_locked_store(LOCK_SH) as store:
            return key in store

    def flush(self) -> Literal[True]:
        with self._open_locked_store(LOCK_EX) as store:
            store.clear()

        return True

    def ping(self) -> Literal[True]:
        return True

    @property
    def connection_exceptions(self) -> Tuple:
        return ()

    @contextmanager
    def _open_locked_store(self, mode: int) -> Generator[Any, None, None]:
        with open(f"{self._store_path}.lock", "w", encoding="utf-8") as lock:
            flock(lock.fileno(), mode)  # blocking until lock is acquired

            try:
                with shelve.open(self._store_path, "c") as store:
                    yield store
            finally:
                flock(lock.fileno(), LOCK_UN)

    def _evict(self) -> None:
        now = datetime.timestamp(datetime.now())

        expired_keys = set()

        with self._open_locked_store(LOCK_EX) as store:
            for key, (_, expiry) in store.items():
                if expiry is not None and expiry < now:
                    expired_keys.add(key)

            for expired_key in expired_keys:
                del store[expired_key]
