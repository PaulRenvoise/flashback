# pylint: disable=no-self-use

from flashback.formatting import parameterize


class TestParameterize:
    def test_one_word(self):
        assert parameterize('Guy') == 'guy'

    def test_multiple_words(self):
        assert parameterize('Donald E. Knuth') == 'donald-e-knuth'

    def test_bad_characters(self):
        assert parameterize('*(o.o)*') == 'o-o'

    def test_underscores(self):
        assert parameterize('int object_index = 0') == 'int-object_index-0'

    def test_multiple_separators(self):
        assert parameterize('squeeze     all!') == 'squeeze-all'

    def test_unicode(self):
        assert parameterize('PŘÍLIŠ ŽLUŤOUČKÝ') == 'prilis-zlutoucky'

    def test_multiple_words_and_keep_case(self):
        assert parameterize('Donald E. Knuth', keep_case=True) == 'Donald-E-Knuth'

    def test_multiple_words_and_sep(self):
        assert parameterize('Donald E. Knuth', sep='//') == 'donald//e//knuth'

    def test_multiple_words_and_sep2(self):
        assert parameterize('Donald E. Knuth', sep='') == 'donaldeknuth'
