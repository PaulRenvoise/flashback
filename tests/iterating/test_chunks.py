from flashback.iterating import chunks


class TestChunks:
    def test_zero_items(self) -> None:
        chunked = list(chunks([]))
        assert not chunked

    def test_multiple_items(self) -> None:
        chunked = list(chunks([1, 2, 3, 4]))
        assert chunked == [(1, 2), (3, 4)]

    def test_multiple_items_without_pad(self) -> None:
        chunked = list(chunks([1, 2, 3]))
        assert chunked == [(1, 2), (3,)]

    def test_multiple_items_with_pad(self) -> None:
        chunked = list(chunks([1, 2, 3], pad=None))
        assert chunked == [(1, 2), (3, None)]

    def test_multiple_pad_items_with_pad(self) -> None:
        chunked = list(chunks([None, None, None], pad=None))
        assert chunked == [(None, None), (None, None)]
