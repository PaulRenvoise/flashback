from flashback.iterating import partition


class TestPartition:
    def test_zero_items(self):
        trues, falses = partition(lambda _: True, [])

        assert not trues
        assert not falses

    def test_multiple_items_int(self):
        evens, odds = partition(lambda x: x % 2, [1, 2, 3, 4, 5])

        assert evens == [1, 3, 5]
        assert odds == [2, 4]

    def test_multiple_items_bool(self):
        evens, odds = partition(lambda x: x % 2 == 0, [1, 2, 3, 4, 5])

        assert evens == [2, 4]
        assert odds == [1, 3, 5]

    def test_multiple_items_str(self):
        trues, falses = partition(lambda x: x if "a" in x else None, ["a", "b", "c", "d", "aa"])

        assert trues == ["a", "aa"]
        assert falses == ["b", "c", "d"]

    def test_multiple_items_list(self):
        trues, falses = partition(lambda x: x, [["a"], [], [1], ["b"], [2], []])

        assert trues == [["a"], [1], ["b"], [2]]
        assert falses == [[], []]
