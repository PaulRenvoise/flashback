from abc import ABC, abstractmethod


class BaseAdapter(ABC):
    """
    Defines an abstract class that needs to be implemented to register a new adapter.
    """
    @abstractmethod
    def __init__(self, **kwargs):
        """
        Instanciates the adapter, without testing the connection (ping is used for that).

        Params:
            kwargs (dict): every given keyword arguments
        """

    @abstractmethod
    def set(self, key, value, ttl):
        """
        Caches a `value` under a given `key`.

        Params:
            key (str): the key under which to cache the value
            value (str): the value to cache
            ttl (int): the number of seconds before expiring the key

        Returns:
            bool: whether or not the operation succeeded

        Raises:
            Base.connection_exceptions: if no connection to the underlying storage is active
        """

    @abstractmethod
    def batch_set(self, keys, values, ttls):
        """
        Caches each value from a list of `values` to its respective key in a list of `keys`.

        Params:
            keys (Iterable<str>): the keys under which to cache the values
            values (Iterable<str>): the values to cache
            ttls (Iterable<int>): the number of seconds before expiring the keys

        Returns:
            bool: whether or not the operation succeeded

        Raises:
            Base.connection_exceptions: if no connection to the underlying storage is active
        """

    @abstractmethod
    def get(self, key):
        """
        Fetches the value stored under `key`.

        Params:
            key (str): the key to retreive the value from

        Returns:
            str|None: the value read from the cache

        Raises:
            Base.connection_exceptions: if no connection to the underlying storage is active
        """

    @abstractmethod
    def batch_get(self, keys):
        """
        Fetches each value stored under its respective key in a list of `keys`.

        Params:
            keys (Iterable<str>): the keys to retreive the values from

        Returns:
            list<str|None>: the values read from the cache

        Raises:
            Base.connection_exceptions: if no connection to the underlying storage is active
        """

    @abstractmethod
    def delete(self, key):
        """
        Removes the given cache `key`.

        Params:
            key (str): the key to remove

        Returns:
            bool: whether or not the operation succeeded

        Raises:
            Base.connection_exceptions: if no connection to the underlying storage is active
        """

    @abstractmethod
    def batch_delete(self, keys):
        """
        Removes the cache of a given list of `keys`, ignores non-existing keys.

        Params:
            keys (Iterable<str>): the keys to remove from the cache

        Returns:
            bool: whether or not the operation succeeded

        Raises:
            Base.connection_exceptions: if no connection to the underlying storage is active
        """

    @abstractmethod
    def exists(self, key):
        """
        Checks the existence of a given `key` in the storage.

        Params:
            key (str): the key to check the existence of

        Returns:
            bool: whether or not the key exists

        Raises:
            Base.connection_exceptions: if no connection to the underlying storage is active
        """

    @abstractmethod
    def flush(self):
        """
        Flushes all keys and values from the adapter's storage.

        Returns:
            bool: always True

        Raises:
            Base.connection_exceptions: if no connection to the underlying storage is active
        """

    @abstractmethod
    def ping(self):
        """
        Checks if a valid connection is setup with the underlying storage.

        Returns:
            bool: always True

        Raises:
            Base.connection_exceptions: if no connection to the underlying storage is active
        """

    @property
    @abstractmethod
    def connection_exceptions(self):
        """
        Lists the exceptions raised by the adapter when a faulty/invalid connection is detected.

        Returns:
            tuple<Exception>: the list of exceptions
        """
