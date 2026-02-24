from flashback.formatting import parameterize


class ParameterizeTest:
    def one_word_test(self) -> None:
        assert parameterize("Guy") == "guy"

    def multiple_words_test(self) -> None:
        assert parameterize("Donald E. Knuth") == "donald-e-knuth"

    def bad_characters_test(self) -> None:
        assert parameterize("*(o.o)*") == "o-o"

    def underscores_test(self) -> None:
        assert parameterize("int object_index = 0") == "int-object_index-0"

    def multiple_separators_test(self) -> None:
        assert parameterize("squeeze     all!") == "squeeze-all"

    def unicode_test(self) -> None:
        assert parameterize("PŘÍLIŠ ŽLUŤOUČKÝ") == "prilis-zlutoucky"

    def multiple_words_and_keep_case_test(self) -> None:
        assert parameterize("Donald E. Knuth", keep_case=True) == "Donald-E-Knuth"

    def multiple_words_and_sep_test(self) -> None:
        assert parameterize("Donald E. Knuth", sep="//") == "donald//e//knuth"

    def multiple_words_and_sep2_test(self) -> None:
        assert parameterize("Donald E. Knuth", sep="") == "donaldeknuth"
