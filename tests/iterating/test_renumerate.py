from flashback.iterating import renumerate


class TestRenumerate:
    def test_zero_items(self):
        assert not list(renumerate([]))

    def test_one_item(self):
        assert list(renumerate(["a"])) == [(0, "a")]

    def test_two_items(self):
        assert list(renumerate(["a", "b"])) == [(1, "b"), (0, "a")]

    def test_three_items(self):
        assert list(renumerate(["a", "b", "c"])) == [(2, "c"), (1, "b"), (0, "a")]

    def test_iterator(self):
        iterator = renumerate(["a", "b"])

        assert next(iterator) == (1, "b")
