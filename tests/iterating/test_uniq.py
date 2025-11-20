from flashback.iterating import uniq


class TestUniq:
    def test_zero_items(self) -> None:
        # Yes, it exists: https://en.wiktionary.org/wiki/uniquified
        uniquified = uniq([])

        assert not uniquified

    def test_multiple_items(self) -> None:
        uniquified = uniq([1, 2, 3, 4, 5, 2, 5, 5])

        assert uniquified == [1, 2, 3, 4, 5]

    def test_unhashable_items(self) -> None:
        uniquified = uniq([{"a": 1}, {"b": 2}, {"c": 3}, {"b": 2}, {"d": 4}, {"a": 1}, {"d": 4}])

        assert uniquified == [{"a": 1}, {"b": 2}, {"c": 3}, {"d": 4}]

    def test_order(self) -> None:
        iterable = ["z", "a", "z", "c", "c", "b", "d", "b"]
        uniquified = uniq(iterable)
        setified = list(set(iterable))

        assert uniquified != setified
