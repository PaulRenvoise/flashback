# pylint: disable=no-self-use

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


class TestChunks:
    def test_zero_items(self):
        chunked = list(chunks([]))
        assert chunked == []

    def test_multiple_items(self):
        chunked = list(chunks([1, 2, 3, 4]))
        assert chunked == [[1, 2], [3, 4]]

    def test_multiple_items_without_pad(self):
        chunked = list(chunks([1, 2, 3]))
        assert chunked == [[1, 2], [3]]

    def test_multiple_items_with_pad(self):
        chunked = list(chunks([1, 2, 3], pad=None))
        assert chunked == [[1, 2], [3, None]]

    def test_multiple_pad_items_with_pad(self):
        chunked = list(chunks([None, None, None], pad=None))
        assert chunked == [[None, None], [None, None]]
