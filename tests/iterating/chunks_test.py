from flashback.iterating import chunks


class ChunksTest:
    def zero_items_test(self) -> None:
        chunked = list(chunks([]))
        assert not chunked

    def multiple_items_test(self) -> None:
        chunked = list(chunks([1, 2, 3]))
        assert chunked == [(1, 2), (3,)]

    def multiple_items_with_size_test(self) -> None:
        chunked = list(chunks([1, 2, 3], size=1))
        assert chunked == [(1,), (2,), (3,)]

    def multiple_items_with_size_without_keyword_test(self) -> None:
        chunked = list(chunks([1, 2, 3], 1))
        assert chunked == [(1,), (2,), (3,)]

    def multiple_items_with_pad_test(self) -> None:
        chunked = list(chunks([1, 2, 3], pad=None))
        assert chunked == [(1, 2), (3, None)]

    def multiple_items_with_size_and_pad_test(self) -> None:
        chunked = list(chunks([1, 2, 3, 4, 5], size=3, pad=None))
        assert chunked == [(1, 2, 3), (4, 5, None)]

    def multiple_items_with_size_and_pad_without_keyword_test(self) -> None:
        chunked = list(chunks([1, 2, 3, 4, 5], 3, None))
        assert chunked == [(1, 2, 3), (4, 5, None)]

    def multiple_pad_items_with_pad_test(self) -> None:
        chunked = list(chunks([None, None, None], pad=None))
        assert chunked == [(None, None), (None, None)]
