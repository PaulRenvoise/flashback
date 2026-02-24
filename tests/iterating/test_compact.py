from flashback.iterating import compact


class TestCompact:
    def test_zero_items(self) -> None:
        compacted = compact([])

        assert not compacted

    def test_multiple_items(self) -> None:
        compacted = compact([1, None, 2, 3, None, 4, 5, None])

        assert compacted == [1, 2, 3, 4, 5]

    def test_multiple_types(self) -> None:
        compacted: list[int | str] = compact([1, None, "2", 3, None, 4, 5, None])

        assert compacted == [1, "2", 3, 4, 5]

    def test_keep_falsy_values(self) -> None:
        compacted: list[int | str | bool] = compact([0, None, "", False, None])

        assert compacted == [0, "", False]

    def test_only_none(self) -> None:
        compacted = compact([None, None, None])

        assert not compacted
