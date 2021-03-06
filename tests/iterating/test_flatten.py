# pylint: disable=no-self-use

from flashback.iterating import flatten


class TestFlatten:
    def test_zero_items(self):
        flattened = flatten([])

        assert flattened == ()

    def test_multiple_items(self):
        flattened = flatten([[1], 2, [3, 4], [5, 6, 7], 8])

        assert flattened == (1, 2, 3, 4, 5, 6, 7, 8)

    def test_mixed_types(self):
        flattened = flatten([1, (2,), {3, 4}, range(5, 6)])

        assert flattened == (1, 2, 3, 4, 5)
