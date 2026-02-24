from flashback.formatting import ordinalize


class OrdinalizeTest:
    def st_test(self) -> None:
        assert ordinalize(1) == "1st"

    def nd_test(self) -> None:
        assert ordinalize(2) == "2nd"

    def rd_test(self) -> None:
        assert ordinalize(3) == "3rd"

    def th_test(self) -> None:
        assert ordinalize(8) == "8th"

    def tens_test(self) -> None:
        assert ordinalize(25) == "25th"

    def hundreds_test(self) -> None:
        assert ordinalize(103) == "103rd"

    def thousands_test(self) -> None:
        assert ordinalize(1241) == "1241st"

    def ten_thousands_test(self) -> None:
        assert ordinalize(20602) == "20602nd"

    def negative_test(self) -> None:
        assert ordinalize(-1) == "-1st"
