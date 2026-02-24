from flashback.iterating import flatten


class FlattenTest:
    def zero_items_test(self) -> None:
        flattened = flatten([])

        assert not flattened

    def multiple_items_test(self) -> None:
        flattened = flatten([[1], 2, [3, 4], [5, 6, 7], 8])

        assert flattened == [1, 2, 3, 4, 5, 6, 7, 8]

    def strings_test(self) -> None:
        flattened = flatten([["abc", "def"], "ghi", ["jkl"]])

        assert flattened == ["abc", "def", "ghi", "jkl"]

    def mixed_flattenable_types_test(self) -> None:
        flattened = flatten([1, (2,), {3}, range(4, 5)])

        assert flattened == [1, 2, 3, 4]

    def mixed_flattenable_values_types_test(self) -> None:
        flattened = flatten(["one", (2,), {"three"}, range(5, 6)])

        assert flattened == ["one", 2, "three", 5]

    def nested_dicts_test(self) -> None:
        flattened = flatten([[{"key1": 1}], [{"key2": 2}, {"key3": 3}]])

        assert flattened == [{"key1": 1}, {"key2": 2}, {"key3": 3}]
