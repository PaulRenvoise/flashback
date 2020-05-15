# pylint: disable=no-self-use

from flashback.formatting import ordinalize


class TestOrdinalize:
    def test_st(self):
        assert ordinalize(1) == '1st'

    def test_nd(self):
        assert ordinalize(2) == '2nd'

    def test_rd(self):
        assert ordinalize(3) == '3rd'

    def test_th(self):
        assert ordinalize(8) == '8th'

    def test_tens(self):
        assert ordinalize(25) == '25th'

    def test_hundreds(self):
        assert ordinalize(103) == '103rd'

    def test_thousands(self):
        assert ordinalize(1241) == '1241st'

    def test_ten_thousands(self):
        assert ordinalize(20602) == '20602nd'

    def test_negative(self):
        assert ordinalize(-1) == '-1st'
