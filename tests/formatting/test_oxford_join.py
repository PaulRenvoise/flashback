from flashback.formatting import oxford_join


class TestOxfordJoin:
    def test_zero_items(self) -> None:
        assert oxford_join([]) == ""

    def test_one_item(self) -> None:
        assert oxford_join(["one"]) == "one"

    def test_two_items(self) -> None:
        assert oxford_join(["one", "two"]) == "one and two"

    def test_three_items(self) -> None:
        assert oxford_join(["one", "two", "three"]) == "one, two, and three"

    def test_two_items_and_sep_and_couple_sep(self) -> None:
        assert oxford_join(["one", "two"], sep="; ", couple_sep=" or ") == "one or two"

    def test_three_items_and_sep_and_last_sep(self) -> None:
        assert oxford_join(["one", "two", "three"], sep="; ", last_sep="; plus ") == "one; two; plus three"

    def test_two_items_and_quotes(self) -> None:
        assert oxford_join(["one", "two"], quotes=True) == '"one" and "two"'
