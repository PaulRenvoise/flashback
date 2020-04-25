from contextlib import contextmanager
from fcntl import flock, LOCK_SH, LOCK_EX, LOCK_UN
import shelve
import tempfile
import uuid

from .base import BaseAdapter


class DiskAdapter(BaseAdapter):
    """
    Exposes a cache store using a locked shelf (see: https://docs.python.org/3/library/shelve.html).
    """

    def __init__(self, **kwargs):
        super().__init__()

        self._store_path = f"{tempfile.gettempdir()}/{uuid.uuid4()}"

    def set(self, key, value):
        with self._open_locked_store(LOCK_EX) as store:
            store[key] = value

        return True

    def batch_set(self, keys, values):
        with self._open_locked_store(LOCK_EX) as store:
            store.update(dict(zip(keys, values)))

        return True

    def get(self, key):
        with self._open_locked_store(LOCK_SH) as store:
            return store.get(key, None)

    def batch_get(self, keys):
        with self._open_locked_store(LOCK_SH) as store:
            return [store.get(key, None) for key in keys]

    def delete(self, key):
        with self._open_locked_store(LOCK_EX) as store:
            return bool(store.pop(key, False))

    def batch_delete(self, keys):
        with self._open_locked_store(LOCK_EX) as store:
            res = [bool(store.pop(key, False)) for key in keys]

        # If we have one False, we need to return False
        return not False in res

    def exists(self, key):
        with self._open_locked_store(LOCK_SH) as store:
            return key in store

    def flush(self):
        with self._open_locked_store(LOCK_EX) as store:
            store.clear()

        return True

    def ping(self):
        return True

    @property
    def connection_exceptions(self):
        return ()

    @contextmanager
    def _open_locked_store(self, mode):
        with open(f"{self._store_path}.lock", 'w') as lock:
            flock(lock.fileno(), mode)  # blocking until lock is acquired

            try:
                with shelve.open(self._store_path, 'c') as store:
                    yield store
            finally:
                flock(lock.fileno(), LOCK_UN)
