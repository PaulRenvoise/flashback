from flashback.iterating import uniq_by


class UniqByTest:
    def zero_items_test(self) -> None:
        # Yes, it exists: https://en.wiktionary.org/wiki/uniquified
        uniquified = uniq_by(lambda x: x, [])
        assert not uniquified

    def multiple_items_test(self) -> None:
        uniquified = uniq_by(lambda x: x, [1, 2, 3, 4, 5, 2, 5, 5])
        assert uniquified == [1, 2, 3, 4, 5]

    def unhashable_items_test(self) -> None:
        uniquified = uniq_by(
            lambda x: tuple(x.items()),
            [{"a": 1}, {"b": 2}, {"c": 3}, {"b": 2}, {"d": 4}, {"a": 1}, {"d": 4}],
        )
        assert uniquified == [{"a": 1}, {"b": 2}, {"c": 3}, {"d": 4}]

    def order_test(self) -> None:
        iterable = ["z", "a", "z", "c", "c", "b", "d", "b"]
        uniquified = uniq_by(lambda x: x, iterable)
        setified = list(set(iterable))

        assert uniquified != setified

    def key_function_test(self) -> None:
        iterable = ["apple", "banana", "cherry", "apricot", "blueberry"]
        uniquified = uniq_by(lambda x: x[0], iterable)
        assert uniquified == ["apple", "banana", "cherry"]
