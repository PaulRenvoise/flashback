from flashback.iterating import flat_map


class FlatMapTest:
    def zero_items_test(self) -> None:
        flat_mapped = flat_map(lambda x: x * 2, [])

        assert not list(flat_mapped)

    def multiple_items_test(self) -> None:
        flat_mapped = flat_map(lambda x: x * 2, [[1], 2, [3, 4], [5, 6, 7], 8])

        assert list(flat_mapped) == [2, 4, 6, 8, 10, 12, 14, 16]

    def strings_test(self) -> None:
        flat_mapped = flat_map(lambda x: "_" + x, [["abc", "def"], "ghi", ["jkl"]])

        assert list(flat_mapped) == ["_abc", "_def", "_ghi", "_jkl"]

    def mixed_flattenable_types_test(self) -> None:
        flat_mapped = flat_map(lambda x: x / 2, [1, (2,), {3, 4}, range(5, 6)])

        assert list(flat_mapped) == [0.5, 1.0, 1.5, 2.0, 2.5]

    def mixed_flattenable_values_types_test(self) -> None:
        flat_mapped = flat_map(lambda x: "_" + str(x), [1, ("abc",), {2}, range(3, 4)])

        assert list(flat_mapped) == ["_1", "_abc", "_2", "_3"]
