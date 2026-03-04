from flashback.iterating import partition


class PartitionTest:
    def zero_items_test(self) -> None:
        trues, falses = partition(lambda _: True, [])

        assert not trues
        assert not falses

    def multiple_items_int_test(self) -> None:
        evens, odds = partition(lambda x: x % 2, [1, 2, 3, 4, 5])

        assert evens == [1, 3, 5]
        assert odds == [2, 4]

    def multiple_items_bool_test(self) -> None:
        evens, odds = partition(lambda x: x % 2 == 0, [1, 2, 3, 4, 5])

        assert evens == [2, 4]
        assert odds == [1, 3, 5]

    def multiple_items_str_test(self) -> None:
        trues, falses = partition(lambda x: x if "a" in x else None, ["a", "b", "c", "d", "aa"])

        assert trues == ["a", "aa"]
        assert falses == ["b", "c", "d"]

    def multiple_items_list_test(self) -> None:
        trues, falses = partition(lambda x: x, [["a"], [], [1], ["b"], [2], []])

        assert trues == [["a"], [1], ["b"], [2]]
        assert falses == [[], []]
