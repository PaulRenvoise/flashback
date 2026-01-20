from flashback.formatting import adverbize


class TestAdverbize:
    def test_once(self) -> None:
        assert adverbize(1) == "once"

    def test_twice(self) -> None:
        assert adverbize(2) == "twice"

    def test_thrice(self) -> None:
        assert adverbize(3) == "thrice"

    def test_times(self) -> None:
        assert adverbize(8) == "8 times"

    def test_tens(self) -> None:
        assert adverbize(25) == "25 times"

    def test_hundreds(self) -> None:
        assert adverbize(103) == "103 times"

    def test_thousands(self) -> None:
        assert adverbize(1241) == "1241 times"

    def test_ten_thousands(self) -> None:
        assert adverbize(20602) == "20602 times"

    def test_negative(self) -> None:
        assert adverbize(-1) == "-1 times"
