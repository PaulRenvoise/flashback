# pylint: disable=no-self-use

from flashback.formatting import truncate


class TestTruncate:
    def test_long_text(self):
        text = truncate('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin ornare bibendum arcu vel accumsan. Ut vitae rhoncus leo, in lobortis dui.')  # pylint: disable=line-too-long
        assert text == 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin ornare bibendum arcu vel accumsan. Ut vitae rhoncus...'  # pylint: disable=line-too-long

    def test_short_text(self):
        text = truncate('Hello world')
        assert text == 'Hello world'

    def test_text_with_limit(self):
        text = truncate('This helper is very useful for preview of descriptions', limit=50)
        assert text == 'This helper is very useful for preview of...'

    def test_empty_suffix(self):
        text = truncate('This is a sample text', limit=10, suffix='')
        assert text == 'This is a'

    def test_suffix_longer_than_text(self):
        text = truncate('Once upon a time', limit=10, suffix=', and the story goes on')
        assert text == 'On, and the story goes on'

    def test_no_space(self):
        text = truncate('spectrophotofluorometrically', limit=25)
        assert text == 'spectrophotofluoromet...'

    def test_space_at_beginning(self):
        text = truncate('I spectrophotofluorometrically assessed this sample', limit=25)
        assert text == 'I spectrophotofluorom...'
