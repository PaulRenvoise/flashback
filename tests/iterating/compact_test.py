from flashback.iterating import compact


class CompactTest:
    def zero_items_test(self) -> None:
        compacted = compact([])

        assert not compacted

    def multiple_items_test(self) -> None:
        compacted = compact([1, None, 2, 3, None, 4, 5, None])

        assert compacted == [1, 2, 3, 4, 5]

    def multiple_types_test(self) -> None:
        compacted: list[int | str] = compact([1, None, "2", 3, None, 4, 5, None])

        assert compacted == [1, "2", 3, 4, 5]

    def keep_falsy_values_test(self) -> None:
        compacted: list[int | str | bool] = compact([0, None, "", False, None])

        assert compacted == [0, "", False]

    def only_none_test(self) -> None:
        compacted = compact([None, None, None])

        assert not compacted
