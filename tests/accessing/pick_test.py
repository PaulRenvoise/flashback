from flashback.accessing import pick


class PickTest:
    def existing_keys_test(self) -> None:
        dictionary = {"key1": 1, "key2": 2, "key3": 3}
        result = pick(dictionary, "key1", "key2")
        assert result == {"key1": 1, "key2": 2}

    def some_missing_keys_test(self) -> None:
        dictionary = {"key1": 1, "key2": 2, "key3": 3}
        result = pick(dictionary, "key1", "key4")
        assert result == {"key1": 1}

    def all_missing_keys_test(self) -> None:
        dictionary = {"key1": 1, "key2": 2, "key3": 3}
        result = pick(dictionary, "key4", "key5")
        assert result == {}

    def no_keys_test(self) -> None:
        dictionary = {"key1": 1, "key2": 2, "key3": 3}
        result = pick(dictionary)
        assert result == {}

    def empty_dictionary_test(self) -> None:
        dictionary = {}
        result = pick(dictionary, "key1", "key2")
        assert result == {}

    def non_string_keys_test(self) -> None:
        dictionary = {1: "one", 2: "two", 3: "three"}
        result = pick(dictionary, 1, 3)
        assert result == {1: "one", 3: "three"}

    def mixed_keys_test(self) -> None:
        dictionary = {1: "one", "two": 2.0, 3.0: 3}
        result = pick(dictionary, 1, "two", 3.0)
        assert result == {1: "one", "two": 2.0, 3.0: 3}
