from flashback.formatting import oxford_join


class OxfordJoinTest:
    def zero_items_test(self) -> None:
        assert oxford_join([]) == ""

    def one_item_test(self) -> None:
        assert oxford_join(["one"]) == "one"

    def two_items_test(self) -> None:
        assert oxford_join(["one", "two"]) == "one and two"

    def three_items_test(self) -> None:
        assert oxford_join(["one", "two", "three"]) == "one, two, and three"

    def two_items_and_sep_and_couple_sep_test(self) -> None:
        assert oxford_join(["one", "two"], sep="; ", couple_sep=" or ") == "one or two"

    def three_items_and_sep_and_last_sep_test(self) -> None:
        assert oxford_join(["one", "two", "three"], sep="; ", last_sep="; plus ") == "one; two; plus three"

    def two_items_and_quotes_test(self) -> None:
        assert oxford_join(["one", "two"], quotes=True) == '"one" and "two"'
