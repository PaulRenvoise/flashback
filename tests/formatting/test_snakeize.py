from flashback.formatting import camelize, kebabize, pascalize, snakeize


class TestSnakeize:
    def test_lowercase(self):
        assert snakeize("stringio") == "stringio"

    def test_snakecase(self):
        assert snakeize("var_name") == "var_name"

    def test_kebabcase(self):
        assert snakeize("long-url-path") == "long_url_path"

    def test_camelcase(self):
        assert snakeize("currentThread") == "current_thread"

    def test_pascalcase(self):
        assert snakeize("StringIO") == "string_io"

    def test_protected_name(self):
        assert snakeize("_protectedName") == "_protected_name"

    def test_dunder_name(self):
        assert snakeize("__dunderName__") == "__dunder_name__"

    def test_lowercase_and_acronyms(self):
        assert snakeize("stringio", acronyms=["IO"]) == "string_io"

    def test_snakecase_and_acronyms(self):
        assert snakeize("var_name", acronyms=["VA"]) == "va_r_name"

    def test_kebabcase_and_acronyms(self):
        assert snakeize("long-url-path", acronyms=["URL"]) == "long_url_path"

    def test_camelcase_and_acronyms(self):
        assert snakeize("currentThread", acronyms=["THREAD"]) == "current_thread"

    def test_pascalcase_and_acronyms(self):
        assert snakeize("StringIO", acronyms=["IO"]) == "string_io"

    def test_camelize_revert(self):
        assert snakeize(camelize("current_thread")) == "current_thread"

    def test_kebabize_revert(self):
        assert snakeize(kebabize("long_url_path")) == "long_url_path"

    def test_pascalize_revert(self):
        assert snakeize(pascalize("string_io")) == "string_io"
