import pytest

from flashback.accessing import dig


class DigTest:
    def no_keys_test(self) -> None:
        container = {}
        value = dig(container)
        assert value is None

    class DictTest:
        def one_key_test(self) -> None:
            container = {"key1": 1}
            value = dig(container, "key1")
            assert value == 1

        def multiple_keys_test(self) -> None:
            container = {"key1": {"key2": {"key3": 1}}}
            value = dig(container, "key1", "key2", "key3")
            assert value == 1

        def one_key_missing_test(self) -> None:
            container = {"key1": {"key2": {"key3": 1}}}
            value = dig(container, "key1", "key2", "key30")
            assert value is None

        def multiple_keys_missing_test(self) -> None:
            container = {"key1": {"key2": {"key3": 1}}}
            value = dig(container, "key10", "key20", "key30")
            assert value is None

        def none_test(self) -> None:
            container = {"key1": {"key2": None}}
            value = dig(container, "key1", "key2", "key3")
            assert value is None

        def empty_test(self) -> None:
            container = {}
            value = dig(container, "key1", "key2")
            assert value is None

        def error_test(self) -> None:
            container = {"key1": {"key2": 123}}
            with pytest.raises(TypeError):
                dig(container, "key1", "key2", "key3")

    class ListTest:
        def one_index_test(self) -> None:
            container = [1]
            value = dig(container, 0)
            assert value == 1

        def multiple_indices_test(self) -> None:
            container = [[[1], 2], 3]
            value = dig(container, 0, 0, 0)
            assert value == 1

        def one_index_missing_test(self) -> None:
            container = [[[1], 2], 3]
            value = dig(container, 0, 0, 3)
            assert value is None

        def multiple_indices_missing_test(self) -> None:
            container = [[[1], 2], 3]
            value = dig(container, 10, 20, 30)
            assert value is None

        def none_test(self) -> None:
            container = [[None], 2]
            value = dig(container, 0, 0, 0)
            assert value is None

        def empty_test(self) -> None:
            container = []
            value = dig(container, 0, 0)
            assert value is None

        def empty_str_test(self) -> None:
            container = []
            with pytest.raises(TypeError):
                dig(container, "0", "0")

        def error_test(self) -> None:
            container = [[1], 2]
            with pytest.raises(TypeError):
                dig(container, 0, 0, 0)

    class MixedTest:
        def one_key_index_test(self) -> None:
            container = {"key1": [1]}
            value = dig(container, "key1", 0)
            assert value == 1

        def multiple_keys_indices_test(self) -> None:
            container = {"key1": {"key2": [{"key3": [1]}]}}
            value = dig(container, "key1", "key2", 0, "key3", 0)
            assert value == 1

        def one_key_missing_test(self) -> None:
            container = {"key1": {"key2": [{"key3": [1]}]}}
            value = dig(container, "key1", "key20")
            assert value is None

        def one_index_missing_test(self) -> None:
            container = {"key1": {"key2": [{"key3": [1]}]}}
            value = dig(container, "key1", "key2", 1)
            assert value is None

        def multiple_keys_indices_missing_test(self) -> None:
            container = {"key1": {"key2": [{"key3": [1]}]}}
            value = dig(container, "key10", 0)
            assert value is None

        def none_test(self) -> None:
            container = {"key1": [None]}
            value = dig(container, "key1", 0)
            assert value is None

        def error_test(self) -> None:
            container = {"key1": [{"key2": 123}]}
            with pytest.raises(TypeError):
                dig(container, "key1", 0, "key2", 0)
