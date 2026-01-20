from flashback.accessing import pick


class TestPick:
    def test_existing_keys(self) -> None:
        dictionary = {"key1": 1, "key2": 2, "key3": 3}
        result = pick(dictionary, "key1", "key2")
        assert result == {"key1": 1, "key2": 2}

    def test_some_missing_keys(self) -> None:
        dictionary = {"key1": 1, "key2": 2, "key3": 3}
        result = pick(dictionary, "key1", "key4")
        assert result == {"key1": 1}

    def test_all_missing_keys(self) -> None:
        dictionary = {"key1": 1, "key2": 2, "key3": 3}
        result = pick(dictionary, "key4", "key5")
        assert result == {}

    def test_no_keys(self) -> None:
        dictionary = {"key1": 1, "key2": 2, "key3": 3}
        result = pick(dictionary)
        assert result == {}

    def test_empty_dictionary(self) -> None:
        dictionary = {}
        result = pick(dictionary, "key1", "key2")
        assert result == {}

    def test_non_string_keys(self) -> None:
        dictionary = {1: "one", 2: "two", 3: "three"}
        result = pick(dictionary, 1, 3)
        assert result == {1: "one", 3: "three"}
