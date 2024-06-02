from flashback.accessing import values_at


class TestValuesAt:
    def test_existing_keys(self) -> None:
        dictionary = {"key1": 1, "key2": 2, "key3": 3}
        values = values_at(dictionary, "key1", "key2")
        assert values == [1, 2]

    def test_with_missing_keys(self) -> None:
        dictionary = {"key1": 1, "key2": 2, "key3": 3}
        values = values_at(dictionary, "key1", "key4")
        assert values == [1]

    def test_with_all_missing_keys(self) -> None:
        dictionary = {"key1": 1, "key2": 2, "key3": 3}
        values = values_at(dictionary, "key4", "key5")
        assert values == []

    def test_with_no_keys(self) -> None:
        dictionary = {"key1": 1, "key2": 2, "key3": 3}
        values = values_at(dictionary)
        assert values == []

    def test_with_empty_dictionary(self) -> None:
        dictionary = {}
        values = values_at(dictionary, "key1", "key2")
        assert values == []

    def test_with_non_string_keys(self) -> None:
        dictionary = {1: "one", 2: "two", 3: "three"}
        values = values_at(dictionary, 1, 3)
        assert values == ["one", "three"]
