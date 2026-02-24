from flashback.iterating import renumerate


class RenumerateTest:
    def zero_items_test(self) -> None:
        assert not list(renumerate([]))

    def one_item_test(self) -> None:
        assert list(renumerate(["a"])) == [(0, "a")]

    def two_items_test(self) -> None:
        assert list(renumerate(["a", "b"])) == [(1, "b"), (0, "a")]

    def three_items_test(self) -> None:
        assert list(renumerate(["a", "b", "c"])) == [(2, "c"), (1, "b"), (0, "a")]

    def iterator_test(self) -> None:
        iterator = renumerate(["a", "b"])

        assert next(iterator) == (1, "b")
