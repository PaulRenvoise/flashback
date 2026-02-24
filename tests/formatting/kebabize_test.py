from flashback.formatting import camelize, kebabize, pascalize, snakeize


class KebabizeTest:
    def lowercase_test(self) -> None:
        assert kebabize("stringio") == "stringio"

    def snakecase_test(self) -> None:
        assert kebabize("var_name") == "var-name"

    def kebabcase_test(self) -> None:
        assert kebabize("long-url-path") == "long-url-path"

    def camelcase_test(self) -> None:
        assert kebabize("currentThread") == "current-thread"

    def pascalcase_test(self) -> None:
        assert kebabize("StringIO") == "string-io"

    def protected_name_test(self) -> None:
        assert kebabize("_protectedName") == "_protected-name"

    def dunder_name_test(self) -> None:
        assert kebabize("__dunderName__") == "__dunder-name__"

    def empty_acronyms_test(self) -> None:
        assert kebabize("stringio", acronyms=[]) == "stringio"

    def lowercase_and_acronyms_test(self) -> None:
        assert kebabize("stringio", acronyms=["IO"]) == "string-io"

    def snakecase_and_acronyms_test(self) -> None:
        assert kebabize("var_name", acronyms=["VA"]) == "va-r-name"

    def kebabcase_and_acronyms_test(self) -> None:
        assert kebabize("long-url-path", acronyms=["URL"]) == "long-url-path"

    def camelcase_and_acronyms_test(self) -> None:
        assert kebabize("currentThread", acronyms=["THREAD"]) == "current-thread"

    def pascalcase_and_acronyms_test(self) -> None:
        assert kebabize("StringIO", acronyms=["IO"]) == "string-io"

    def camelize_revert_test(self) -> None:
        assert kebabize(camelize("current-thread")) == "current-thread"

    def snakeize_revert_test(self) -> None:
        assert kebabize(snakeize("var-name")) == "var-name"

    def pascalize_revert_test(self) -> None:
        assert kebabize(pascalize("string-io")) == "string-io"
