# pylint: disable=no-self-use

from flashback.accessing import dig


class TestDig:
    def test_zero_keys(self):
        dictionary = {"key1": 1}
        value = dig(dictionary, "key1")
        assert value == 1

    def test_multiple_keys(self):
        dictionary = {"key1": {"key2": {"key3": 1}}}
        value = dig(dictionary, "key1", "key2", "key3")
        assert value == 1

    def test_one_key_missing(self):
        dictionary = {"key1": {"key2": {"key3": 1}}}
        value = dig(dictionary, "key1", "key2", "key30")
        assert value is None

    def test_multiple_keys_missing(self):
        dictionary = {"key1": {"key2": {"key3": 1}}}
        value = dig(dictionary, "key10", "key20", "key30")
        assert value is None

    def test_none(self):
        dictionary = {"key1": {"key2": None}}
        value = dig(dictionary, "key1", "key2", "key3")
        assert value is None
