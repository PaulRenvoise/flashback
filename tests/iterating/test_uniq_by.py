from flashback.iterating import uniq_by


class TestUniqBy:
    def test_zero_items(self) -> None:
        uniquified = uniq_by(lambda x: x, [])
        assert not uniquified

    def test_multiple_items(self) -> None:
        uniquified = uniq_by(lambda x: x, [1, 2, 3, 4, 5, 2, 5, 5])
        assert uniquified == (1, 2, 3, 4, 5)

    def test_unhashable_items(self) -> None:
        uniquified = uniq_by(
            lambda x: tuple(x.items()),
            [{"a": 1}, {"b": 2}, {"c": 3}, {"b": 2}, {"d": 4}, {"a": 1}, {"d": 4}],
        )
        assert uniquified == ({"a": 1}, {"b": 2}, {"c": 3}, {"d": 4})

    def test_order(self) -> None:
        iterable = ["z", "a", "z", "c", "c", "b", "d", "b"]
        uniquified = uniq_by(lambda x: x, iterable)
        setified = list(set(iterable))

        assert uniquified != setified

    def test_key_function(self) -> None:
        iterable = ["apple", "banana", "cherry", "apricot", "blueberry"]
        uniquified = uniq_by(lambda x: x[0], iterable)
        assert uniquified == ("apple", "banana", "cherry")
