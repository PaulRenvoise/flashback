from flashback.iterating import uniq


class UniqTest:
    def zero_items_test(self) -> None:
        # Yes, it exists: https://en.wiktionary.org/wiki/uniquified
        uniquified = uniq([])

        assert not uniquified

    def multiple_items_test(self) -> None:
        uniquified = uniq([1, 2, 3, 4, 5, 2, 5, 5])

        assert uniquified == [1, 2, 3, 4, 5]

    def unhashable_items_test(self) -> None:
        uniquified = uniq([{"a": 1}, {"b": 2}, {"c": 3}, {"b": 2}, {"d": 4}, {"a": 1}, {"d": 4}])

        assert uniquified == [{"a": 1}, {"b": 2}, {"c": 3}, {"d": 4}]

    def order_test(self) -> None:
        iterable = ["z", "a", "z", "c", "c", "b", "d", "b"]
        uniquified = uniq(iterable)
        setified = list(set(iterable))

        assert uniquified != setified
