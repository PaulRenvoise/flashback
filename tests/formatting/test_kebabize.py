from flashback.formatting import camelize, kebabize, pascalize, snakeize


class TestKebabize:
    def test_lowercase(self) -> None:
        assert kebabize("stringio") == "stringio"

    def test_snakecase(self) -> None:
        assert kebabize("var_name") == "var-name"

    def test_kebabcase(self) -> None:
        assert kebabize("long-url-path") == "long-url-path"

    def test_camelcase(self) -> None:
        assert kebabize("currentThread") == "current-thread"

    def test_pascalcase(self) -> None:
        assert kebabize("StringIO") == "string-io"

    def test_protected_name(self) -> None:
        assert kebabize("_protectedName") == "_protected-name"

    def test_dunder_name(self) -> None:
        assert kebabize("__dunderName__") == "__dunder-name__"

    def test_lowercase_and_acronyms(self) -> None:
        assert kebabize("stringio", acronyms=["IO"]) == "string-io"

    def test_snakecase_and_acronyms(self) -> None:
        assert kebabize("var_name", acronyms=["VA"]) == "va-r-name"

    def test_kebabcase_and_acronyms(self) -> None:
        assert kebabize("long-url-path", acronyms=["URL"]) == "long-url-path"

    def test_camelcase_and_acronyms(self) -> None:
        assert kebabize("currentThread", acronyms=["THREAD"]) == "current-thread"

    def test_pascalcase_and_acronyms(self) -> None:
        assert kebabize("StringIO", acronyms=["IO"]) == "string-io"

    def test_camelize_revert(self) -> None:
        assert kebabize(camelize("current-thread")) == "current-thread"

    def test_snakeize_revert(self) -> None:
        assert kebabize(snakeize("var-name")) == "var-name"

    def test_pascalize_revert(self) -> None:
        assert kebabize(pascalize("string-io")) == "string-io"
