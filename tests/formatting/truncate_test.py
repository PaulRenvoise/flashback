from flashback.formatting import truncate


class TruncateTest:
    def long_text_test(self) -> None:
        text = truncate(
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin ornare bibendum arcu vel accumsan. Ut vitae rhoncus leo, in lobortis dui.",  # noqa: E501
        )
        assert (
            text
            == "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin ornare bibendum arcu vel accumsan. Ut vitae rhoncus..."  # noqa: E501
        )

    def short_text_test(self) -> None:
        text = truncate("Hello world")
        assert text == "Hello world"

    def text_with_limit_test(self) -> None:
        text = truncate("This helper is very useful for preview of descriptions", limit=50)
        assert text == "This helper is very useful for preview of..."

    def empty_suffix_test(self) -> None:
        text = truncate("This is a sample text", limit=10, suffix="")
        assert text == "This is a"

    def suffix_longer_than_text_test(self) -> None:
        text = truncate("Once upon a time", limit=10, suffix=", and the story goes on")
        assert text == "On, and the story goes on"

    def no_space_test(self) -> None:
        text = truncate("spectrophotofluorometrically", limit=25)
        assert text == "spectrophotofluoromet..."

    def space_at_beginning_test(self) -> None:
        text = truncate("I spectrophotofluorometrically assessed this sample", limit=25)
        assert text == "I spectrophotofluorom..."
