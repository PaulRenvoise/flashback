# pylint: disable=no-self-use

from flashback.iterating import uniq


class TestUniq:
    def test_zero_items(self):
        # Yes, it exists: https://en.wiktionary.org/wiki/uniquified
        uniquified = uniq([])

        assert uniquified == ()

    def test_multiple_items(self):
        uniquified = uniq([1, 2, 3, 4, 5, 2, 5, 5])

        assert uniquified == (1, 2, 3, 4, 5)

    def test_order(self):
        iterable = ['z', 'a', 'z', 'c', 'c', 'b', 'd', 'b']
        uniquified = uniq(iterable)
        setified = list(set(iterable))

        assert uniquified == ('z', 'a', 'c', 'b', 'd')
        assert uniquified != setified
