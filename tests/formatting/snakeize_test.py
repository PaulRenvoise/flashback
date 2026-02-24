from flashback.formatting import camelize, kebabize, pascalize, snakeize


class SnakeizeTest:
    def lowercase_test(self) -> None:
        assert snakeize("stringio") == "stringio"

    def snakecase_test(self) -> None:
        assert snakeize("var_name") == "var_name"

    def kebabcase_test(self) -> None:
        assert snakeize("long-url-path") == "long_url_path"

    def camelcase_test(self) -> None:
        assert snakeize("currentThread") == "current_thread"

    def pascalcase_test(self) -> None:
        assert snakeize("StringIO") == "string_io"

    def protected_name_test(self) -> None:
        assert snakeize("_protectedName") == "_protected_name"

    def dunder_name_test(self) -> None:
        assert snakeize("__dunderName__") == "__dunder_name__"

    def empty_acronyms_test(self) -> None:
        assert snakeize("stringio", acronyms=[]) == "stringio"

    def lowercase_and_acronyms_test(self) -> None:
        assert snakeize("stringio", acronyms=["IO"]) == "string_io"

    def snakecase_and_acronyms_test(self) -> None:
        assert snakeize("var_name", acronyms=["VA"]) == "va_r_name"

    def kebabcase_and_acronyms_test(self) -> None:
        assert snakeize("long-url-path", acronyms=["URL"]) == "long_url_path"

    def camelcase_and_acronyms_test(self) -> None:
        assert snakeize("currentThread", acronyms=["THREAD"]) == "current_thread"

    def pascalcase_and_acronyms_test(self) -> None:
        assert snakeize("StringIO", acronyms=["IO"]) == "string_io"

    def camelize_revert_test(self) -> None:
        assert snakeize(camelize("current_thread")) == "current_thread"

    def kebabize_revert_test(self) -> None:
        assert snakeize(kebabize("long_url_path")) == "long_url_path"

    def pascalize_revert_test(self) -> None:
        assert snakeize(pascalize("string_io")) == "string_io"
