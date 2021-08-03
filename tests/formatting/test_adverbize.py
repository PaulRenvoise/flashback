# pylint: disable=no-self-use

from flashback.formatting import adverbize


class TestAdverbize:
    def test_once(self):
        assert adverbize(1) == "once"

    def test_twice(self):
        assert adverbize(2) == "twice"

    def test_thrice(self):
        assert adverbize(3) == "thrice"

    def test_times(self):
        assert adverbize(8) == "8 times"

    def test_tens(self):
        assert adverbize(25) == "25 times"

    def test_hundreds(self):
        assert adverbize(103) == "103 times"

    def test_thousands(self):
        assert adverbize(1241) == "1241 times"

    def test_ten_thousands(self):
        assert adverbize(20602) == "20602 times"

    def test_negative(self):
        assert adverbize(-1) == "-1 times"
