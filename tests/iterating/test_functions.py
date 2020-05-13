# pylint: disable=no-self-use

from collections import deque

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
        assert chunked == [(1, 2), (3, 4)]

    def test_multiple_items_without_pad(self):
        chunked = list(chunks([1, 2, 3]))
        assert chunked == [(1, 2), (3,)]

    def test_multiple_items_with_pad(self):
        chunked = list(chunks([1, 2, 3], pad=None))
        assert chunked == [(1, 2), (3, None)]

    def test_multiple_pad_items_with_pad(self):
        chunked = list(chunks([None, None, None], pad=None))
        assert chunked == [(None, None), (None, None)]


class TestPartition:
    def test_zero_items(self):
        trues, falses = partition(lambda x: x % 2, [])

        assert trues == ()
        assert falses == ()

    def test_multiple_items_bool(self):
        evens, odds = partition(lambda x: x % 2 == 0, [1, 2, 3, 4, 5])

        assert evens == (2, 4)
        assert odds == (1, 3, 5)

    def test_multiple_items_str(self):
        trues, falses = partition(lambda x: x if 'a' in x else None, ['a', 'b', 'c', 'd', 'aa'])

        assert trues == ('a', 'aa')
        assert falses == ('b', 'c', 'd')

    def test_multiple_items_list(self):
        trues, falses = partition(lambda x: x, [['a'], [], [1], ['b'], [2], []])

        assert trues == (['a'], [1], ['b'], [2])
        assert falses == ([], [])


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
