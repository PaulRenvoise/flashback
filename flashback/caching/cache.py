from __future__ import annotations

from collections.abc import Sequence
from typing import Any

import json

from ..importing import import_class_from_path


class Cache:
    """
    Defines a generic caching client, that can be used with several adapters.

    All lone scalar (being exlusively ints/floats, not ints/floats in dict, sets, lists, etc.)
    are converted to unicode strings (redis is the only service that does this conversion natively,
    but this ensure a homogeneous behaviour across adapters).

    All values are serialized using JSON before being forwarded to the adapter and stored.

    Examples:
        ```python
        from flashback.caching import Cache

        cache = Cache(adapter="memory")

        # Has default operations for key-value stores
        cache.set("key", "val")
        #=> True

        cache.get("key")
        #=> "val"

        cache.delete("key")
        #=> True

        cache.exists("key")
        #=> False

        # Plus batch operations
        cache.batch_set(["key1", "key2", "key3"], ["val1", "val2", "val3"])
        #=> True

        cache.batch_get(["key1", "key2", "key3"]) == ["val1", "val2", "val3"]
        #=> ["val1", "val2", "val3"]

        cache.batch_delete(["key1", "key2", "key3"])
        #=> True

        # And some more
        cache.ping()
        #=> True

        cache.flush()
        #=> True
        ```
    """

    def __init__(self, adapter: str = "memory", ttl: int = -1, flush: bool = False, **kwargs) -> None:
        """
        Params:
            adapter: the adapter to use for the storage
            ttl: the number of seconds before expiring the keys (default: -1 (never))
            flush: whether or not to flush the storage after connecting
            kwargs: every additional keyword arguments, forwarded to the adapter
        """
        super().__init__()

        self.ttl = ttl

        try:
            adapter_class = import_class_from_path(f"{adapter}_adapter", ".adapters")

            self.adapter = adapter_class(**kwargs)
        except (ImportError, AttributeError) as e:
            raise NotImplementedError(f"adapter {adapter!r} is not yet supported") from e

        if flush:
            self.flush()

        # Notifies that we have a new connection
        self.ping()

    def set(self, key: str, value: Any, ttl: int | None = None) -> bool:
        """
        Sets `key` to `value`.

        Examples:
            ```python
            from flashback.caching import Cache

            cache = Cache()

            cache.set("key", "val")
            #=> True
            ```

        Params:
            key: the key to set
            value: the value to cache
            ttl: the number of seconds before expiring the key (default: init ttl)

        Returns:
            whether or not the operation succeeded
        """
        json_value = json.dumps(self._convert_numeric(value))

        try:
            res = self.adapter.set(key, json_value, ttl=ttl or self.ttl)
        except self.adapter.connection_exceptions:
            res = False

        return res

    def batch_set(self, keys: Sequence[str], values: Sequence[Any], ttls: Sequence[int] | None = None) -> bool:
        """
        Sets a batch of `keys` to their respective `values`.

        Examples:
            ```python
            from flashback.caching import Cache

            cache = Cache()

            cache.batch_set(["key1", "key2"], ["val1", "val2"])
            #=> True
            ```

        Params:
            keys: the list of keys to set
            values: the list of values to cache
            ttls: the number of seconds before expiring the keys (default: init ttl)

        Returns:
            whether or not the operation succeeded

        Raises:
            ValueError: if the lengths of the keys and values differ
        """
        if ttls is None:
            ttls = [self.ttl for _ in range(len(keys))]

        if len(set(map(len, [keys, values, ttls]))) > 1:
            raise ValueError("invalid arguments, length of 'keys', 'values', and 'ttls' must be equal")

        json_values = [json.dumps(self._convert_numeric(value)) for value in values]

        try:
            res = self.adapter.batch_set(keys, json_values, ttls=ttls)
        except self.adapter.connection_exceptions:
            res = False

        return res

    def get(self, key: str) -> Any | None:
        """
        Fetches the value stored under `key`.

        Examples:
            ```python
            from flashback.caching import Cache

            cache = Cache()
            cache.set("key", "val")

            cache.get("key")
            #=> "val"

            cache.get("yek")
            #=> None
            ```

        Params:
            key: the key to fetch the value from

        Returns:
            the value read from the storage
        """
        try:
            json_value = self.adapter.get(key)
            value = self._decode_json(json_value)
        except self.adapter.connection_exceptions:
            value = None

        return value

    def batch_get(self, keys: Sequence[str]) -> Sequence[Any | None]:
        """
        Fetches the values stored under `keys`.

        Examples:
            ```python
            from flashback.caching import Cache

            cache = Cache()
            cache.set("key", "val")

            cache.batch_get(["key", "yek"])
            #=> ["val", None]
            ```

        Params:
            keys: the keys to fetch the values from

        Returns:
            the values read from the storage
        """
        try:
            json_values = self.adapter.batch_get(keys)
            values = [self._decode_json(json_value) for json_value in json_values]
        except self.adapter.connection_exceptions:
            values = [None] * len(keys)

        return values

    def delete(self, key: str) -> bool:
        """
        Deletes the given `key` from the storage.

        Examples:
            ```python
            from flashback.caching import Cache

            cache = Cache()
            cache.set("key", "val")

            cache.delete("key")
            #=> True

            cache.delete("yek")
            #=> False
            ```

        Params:
            key: the key to remove

        Returns:
            whether or not the operation succeeded
        """
        try:
            res = self.adapter.delete(key)
        except self.adapter.connection_exceptions:
            res = False

        return res

    def batch_delete(self, keys: Sequence[str]) -> bool:
        """
        Deletes the given `keys` from the storage, ignoring non-existing keys.

        Examples:
            ```python
            from flashback.caching import Cache

            cache = Cache()
            cache.batch_set(["key1", "key2"], ["val1", "val2"])

            cache.batch_delete(["key1", "key2"])
            #=> True

            cache.batch_delete(["yek"])
            #=> False
            ```

        Params:
            keys: the keys to remove from the cache

        Returns:
            whether or not the operation succeeded
        """
        try:
            res = self.adapter.batch_delete(keys)
        except self.adapter.connection_exceptions:
            res = False

        return res

    def exists(self, key: str) -> bool:
        """
        Checks whether or not the given `key` exists in the storage.

        Examples:
            ```python
            from flashback.caching import Cache

            cache = Cache()
            cache.set("key", "val")

            cache.exists("key")
            #=> True

            cache.exists("yek")
            #=> False
            ```

        Params:
            key: the key to check the existence of

        Returns:
            whether or not the key exists
        """
        try:
            res = self.adapter.exists(key)
        except self.adapter.connection_exceptions:
            res = False

        return res

    def flush(self) -> bool:
        """
        Flushes all keys from the storage.

        Examples:
            ```python
            from flashback.caching import Cache

            cache = Cache()
            cache.set("key", "val")

            cache.flush()
            #=> True
            ```

        Returns:
            always True

        Raises:
            flashback.caching.adapters.base.BaseAdapter.connection_exceptions: if no connection with the storage
        """
        return self.adapter.flush()

    def ping(self) -> bool:
        """
        Checks if a valid connection exists with the storage.

        Examples:
            ```python
            from flashback.caching import Cache

            cache = Cache()

            cache.ping()
            #=> True
            ```

        Returns:
            always True

        Raises:
            flashback.caching.adapters.base.BaseAdapter.connection_exceptions: if no connection with the storage
        """
        return self.adapter.ping()

    @staticmethod
    def _decode_json(json_value: str) -> Any:
        try:
            return json.loads(json_value)
        except TypeError:  # non-strings (e.g. None)
            return json_value

    @staticmethod
    def _convert_numeric(value):
        # We do not check if isinstance since bool is a subclass of int
        if type(value) in {int, float, complex}:
            value = repr(value)

        return value
