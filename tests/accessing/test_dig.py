import pytest

from flashback.accessing import dig


class TestDig:
    def test_no_keys(self) -> None:
        container = {}
        value = dig(container)
        assert value is None

    class TestDict:
        def test_one_key(self) -> None:
            container = {"key1": 1}
            value = dig(container, "key1")
            assert value == 1

        def test_multiple_keys(self) -> None:
            container = {"key1": {"key2": {"key3": 1}}}
            value = dig(container, "key1", "key2", "key3")
            assert value == 1

        def test_one_key_missing(self) -> None:
            container = {"key1": {"key2": {"key3": 1}}}
            value = dig(container, "key1", "key2", "key30")
            assert value is None

        def test_multiple_keys_missing(self) -> None:
            container = {"key1": {"key2": {"key3": 1}}}
            value = dig(container, "key10", "key20", "key30")
            assert value is None

        def test_none(self) -> None:
            container = {"key1": {"key2": None}}
            value = dig(container, "key1", "key2", "key3")
            assert value is None

        def test_error(self) -> None:
            container = {"key1": {"key2": 123}}
            with pytest.raises(AttributeError):
                dig(container, "key1", "key2", "key3")

    class TestList:
        def test_one_index(self) -> None:
            container = [1]
            value = dig(container, 0)
            assert value == 1

        def test_multiple_indices(self) -> None:
            container = [[[1], 2], 3]
            value = dig(container, 0, 0, 0)
            assert value == 1

        def test_one_index_missing(self) -> None:
            container = [[[1], 2], 3]
            value = dig(container, 0, 0, 3)
            assert value is None

        def test_multiple_indices_missing(self) -> None:
            container = [[[1], 2], 3]
            value = dig(container, 10, 20, 30)
            assert value is None

        def test_none(self) -> None:
            container = [[None], 2]
            value = dig(container, 0, 0, 0)
            assert value is None

        def test_error(self) -> None:
            container = [[1], 2]
            with pytest.raises(AttributeError):
                dig(container, 0, 0, 0)

    class TestMixed:
        def test_one_key_index(self) -> None:
            container = {"key1": [1]}
            value = dig(container, "key1", 0)
            assert value == 1

        def test_multiple_keys_indices(self) -> None:
            container = {"key1": {"key2": [{"key3": [1]}]}}
            value = dig(container, "key1", "key2", 0, "key3", 0)
            assert value == 1

        def test_one_key_missing(self) -> None:
            container = {"key1": {"key2": [{"key3": [1]}]}}
            value = dig(container, "key1", "key20")
            assert value is None

        def test_one_index_missing(self) -> None:
            container = {"key1": {"key2": [{"key3": [1]}]}}
            value = dig(container, "key1", "key2", 1)
            assert value is None

        def test_multiple_keys_indices_missing(self) -> None:
            container = {"key1": {"key2": [{"key3": [1]}]}}
            value = dig(container, "key10", 0)
            assert value is None

        def test_none(self) -> None:
            container = {"key1": [None]}
            value = dig(container, "key1", 0)
            assert value is None

        def test_error(self) -> None:
            container = {"key1": [{"key2": 123}]}
            with pytest.raises(AttributeError):
                dig(container, "key1", 0, "key2", 0)
