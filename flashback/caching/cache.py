# pylint: disable=no-member

import json

from ..importing import import_class_from_path


class Cache:
    """
    Defines a generic caching client, that can be used with several adapters.

    All lone numeric values (the ones being exlusively an int/float, not int/floats in dict, sets, lists, etc.)
    are converted to unicode strings (redis is the only service that does this conversion natively,
    but this ensure a homogeneous behaviour across adapters).

    All values are serialized using JSON before being forwarded to the adapter and stored.

    Examples:
        ```python
        TODO
        ```
    """

    def __init__(self, adapter='memory', flush=False, **kwargs):
        """
        Instantiates a connection with a cache storage with the given `adapter`.

        Params:
            - `adapter (str)` the adapter to use for the cache storage
            - `flush (bool)` whether or not to flush the cache storage after connecting
            - `kwargs (dict)` every additional keyword arguments, forwarded to the adapter

        Returns:
            - `None`
        """
        super().__init__()

        try:
            adapter_class = import_class_from_path(f"{adapter}_adapter", '.adapters')
            self.adapter = adapter_class(**kwargs)
        except (ImportError, AttributeError):
            raise NotImplementedError(f"Adapter '{adapter}' is not yet supported.")

        if flush:
            self.flush()

        # Notify that we have a new connection
        self.ping()

    def set(self, key, value):
        """
        Sets `key` to `value`.

        Examples:
            ```python
            TODO
            ```

        Params:
            - `key (str)` the key to set
            - `value (str)` the value to cache

        Returns:
            - `bool` whether or not the operation succeeded
        """
        json_value = json.dumps(self._convert_numeric(value))

        try:
            res = self.adapter.set(key, json_value)
        except self.adapter.connection_exceptions:
            res = False

        return res

    def batch_set(self, keys, values):
        """
        Sets a batch of `keys` to their respective `values`.

        Examples:
            ```python
            TODO
            ```

        Params:
            - `keys (Iterable<str>)` the list of keys to set
            - `values (Iterable<str>)` the list of values to cache

        Returns:
            - `bool` whether or not the operation succeeded

        Raises:
            - `ValueError` if the lengths of the keys and values differ
        """
        if len(keys) != len(values):
            raise ValueError("Invalid arguments, length of 'keys' and 'values' must be equal")

        json_values = [json.dumps(self._convert_numeric(value)) for value in values]

        try:
            res = self.adapter.batch_set(keys, json_values)
        except self.adapter.connection_exceptions:
            res = False

        return res

    def get(self, key):
        """
        Fetches the value stored under `key`.

        Examples:
            ```python
            TODO
            ```

        Params:
            - `key (str)` the key to fetch the value from

        Returns:
            - `str|None` the value read from the cache
        """
        try:
            json_value = self.adapter.get(key)
            value = self._decode_json(json_value)
        except self.adapter.connection_exceptions:
            value = None

        return value

    def batch_get(self, keys):
        """
        Fetches the values stored under `keys`.

        Examples:
            ```python
            TODO
            ```

        Params:
            - `keys (Iterable<str>)` the keys to fetch the values from

        Returns:
            - `list<str|None>` the values read from the cache
        """
        try:
            json_values = self.adapter.batch_get(keys)
            values = [self._decode_json(json_value) for json_value in json_values]
        except self.adapter.connection_exceptions:
            values = [None] * len(keys)

        return values

    def delete(self, key):
        """
        Deletes the given `key` from the cache storage.

        Examples:
            ```python
            TODO
            ```

        Params:
            - `key (str)` the key to remove

        Returns:
            - `bool` whether or not the operation succeeded
        """
        try:
            res = self.adapter.delete(key)
        except self.adapter.connection_exceptions:
            res = False

        return res

    def batch_delete(self, keys):
        """
        Deletes the given `keys` from the cache storage, ignoring non-existing keys.

        Examples:
            ```python
            TODO
            ```

        Params:
            - `keys (Iterable<str>)` the keys to remove from the cache

        Returns:
            - `bool` whether or not the operation succeeded
        """
        try:
            res = self.adapter.batch_delete(keys)
        except self.adapter.connection_exceptions:
            res = False

        return res

    def exists(self, key):
        """
        Checks whether or not the given `key` exists in the cache storage.

        Examples:
            ```python
            TODO
            ```

        Params:
            - `key (str)` the key to check the existence of

        Returns:
            - `bool` whether or not the key exists
        """
        try:
            res = self.adapter.exists(key)
        except self.adapter.connection_exceptions:
            res = False

        return res

    def flush(self):
        """
        Flushes all keys from the cache storage.

        Examples:
            ```python
            TODO
            ```

        Params:
            - `None`

        Returns:
            - `bool` always True

        Raises:
            - `flashback.caching.adapters.base.BaseAdapter.connection_exceptions` if no connection with the storage
        """
        return self.adapter.flush()

    def ping(self):
        """
        Checks if a valid connection exists with the caching storage.

        Examples:
            ```python
            TODO
            ```

        Params:
            - `None`

        Returns:
            - `bool` always True

        Raises:
            - `flashback.caching.adapters.base.BaseAdapter.connection_exceptions` if no connection with the storage
        """
        return self.adapter.ping()

    @staticmethod
    def _decode_json(json_value):
        try:
            return json.loads(json_value)
        except TypeError:  # non-strings (e.g. None)
            pass
        except ValueError:  # invalid JSONs
            pass

    @staticmethod
    def _convert_numeric(value):
        # We do not check is `isinstance` since `bool` is a subclass of `int`
        if type(value) in {int, float, complex}:  # pylint: disable=unidiomatic-typecheck
            value = repr(value)

        return value
