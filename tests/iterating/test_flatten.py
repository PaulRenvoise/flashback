from flashback.iterating import flatten


class TestFlatten:
    def test_zero_items(self):
        flattened = flatten([])

        assert not flattened

    def test_multiple_items(self):
        flattened = flatten([[1], 2, [3, 4], [5, 6, 7], 8])

        assert flattened == (1, 2, 3, 4, 5, 6, 7, 8)

    def test_strings(self):
        flattened = flatten([["abc", "def"], "ghi", ["jkl"]])

        assert flattened == ("abc", "def", "ghi", "jkl")

    def test_mixed_types(self):
        flattened = flatten([1, (2,), {3, 4}, range(5, 6)])

        assert flattened == (1, 2, 3, 4, 5)

    def test_nested_dicts(self):
        flattened = flatten([[{"key1": 1}], [{"key2": 2}, {"key3": 3}]])

        assert flattened == ({"key1": 1}, {"key2": 2}, {"key3": 3})
