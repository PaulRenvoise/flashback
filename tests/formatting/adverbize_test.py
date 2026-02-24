from flashback.formatting import adverbize


class AdverbizeTest:
    def once_test(self) -> None:
        assert adverbize(1) == "once"

    def twice_test(self) -> None:
        assert adverbize(2) == "twice"

    def thrice_test(self) -> None:
        assert adverbize(3) == "thrice"

    def times_test(self) -> None:
        assert adverbize(8) == "8 times"

    def tens_test(self) -> None:
        assert adverbize(25) == "25 times"

    def hundreds_test(self) -> None:
        assert adverbize(103) == "103 times"

    def thousands_test(self) -> None:
        assert adverbize(1241) == "1241 times"

    def ten_thousands_test(self) -> None:
        assert adverbize(20602) == "20602 times"

    def negative_test(self) -> None:
        assert adverbize(-1) == "-1 times"
