from flashback.accessing import values_at


class ValuesAtTest:
    def existing_keys_test(self) -> None:
        dictionary = {"key1": 1, "key2": 2, "key3": 3}
        values = values_at(dictionary, "key1", "key2")
        assert values == [1, 2]

    def missing_keys_test(self) -> None:
        dictionary = {"key1": 1, "key2": 2, "key3": 3}
        values = values_at(dictionary, "key1", "key4")
        assert values == [1]

    def all_missing_keys_test(self) -> None:
        dictionary = {"key1": 1, "key2": 2, "key3": 3}
        values = values_at(dictionary, "key4", "key5")
        assert values == []

    def no_keys_test(self) -> None:
        dictionary = {"key1": 1, "key2": 2, "key3": 3}
        values = values_at(dictionary)
        assert values == []

    def empty_dictionary_test(self) -> None:
        dictionary = {}
        values = values_at(dictionary, "key1", "key2")
        assert values == []

    def non_string_keys_test(self) -> None:
        dictionary = {1: "one", 2: "two", 3: "three"}
        values = values_at(dictionary, 1, 3)
        assert values == ["one", "three"]

    def mixed_keys_test(self) -> None:
        dictionary = {1: "one", "two": 2.0, 3.0: 3}
        values = values_at(dictionary, 1, "two", 3.0)
        assert values == ["one", 2.0, 3]
