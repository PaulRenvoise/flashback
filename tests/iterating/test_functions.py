# pylint: disable=no-self-use,redefined-outer-name

from flashback.iterating import *


class TestRenumerate:
    def test_zero_items(self):
        assert list(renumerate([])) == []

    def test_one_item(self):
        assert list(renumerate(['a'])) == [(0, 'a')]

    def test_two_items(self):
        assert list(renumerate(['a', 'b'])) == [(1, 'b'), (0, 'a')]

    def test_three_items(self):
        assert list(renumerate(['a', 'b', 'c'])) == [(2, 'c'), (1, 'b'), (0, 'a')]

    def test_iterator(self):
        iterator = renumerate(['a', 'b'])
        assert next(iterator) == (1, 'b')
