from flashback.iterating import flat_map


class TestFlatMap:
    def test_zero_items(self) -> None:
        flat_mapped = flat_map(lambda x: x * 2, [])

        assert not list(flat_mapped)

    def test_multiple_items(self) -> None:
        flat_mapped = flat_map(lambda x: x * 2, [[1], 2, [3, 4], [5, 6, 7], 8])

        assert list(flat_mapped) == [2, 4, 6, 8, 10, 12, 14, 16]

    def test_strings(self) -> None:
        flat_mapped = flat_map(lambda x: "_" + x, [["abc", "def"], "ghi", ["jkl"]])

        assert list(flat_mapped) == ["_abc", "_def", "_ghi", "_jkl"]

    def test_mixed_flattenable_types(self) -> None:
        flat_mapped = flat_map(lambda x: x / 2, [1, (2,), {3, 4}, range(5, 6)])

        assert list(flat_mapped) == [0.5, 1.0, 1.5, 2.0, 2.5]

    def test_mixed_flattenable_values_types(self) -> None:
        flat_mapped = flat_map(lambda x: "_" + str(x), [1, ("abc",), {2}, range(3, 4)])

        assert list(flat_mapped) == ["_1", "_abc", "_2", "_3"]
