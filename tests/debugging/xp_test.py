from io import StringIO

import pytest
import regex

from flashback.debugging import xp

CRE_ANSI = regex.compile(r"(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]", regex.IGNORECASE)


@pytest.fixture
def output() -> StringIO:
    return StringIO()


class XpTest:
    def simple_test(self, output: StringIO) -> None:
        xp(None, o=output)

        assert CRE_ANSI.sub("", output.getvalue()) == ("tests/debugging/xp_test.py:18\n    None (NoneType)\n")

    def raw_test(self, output: StringIO) -> None:
        xp(None, o=output)

        assert output.getvalue() == (
            "\x1b[2mtests/debugging/xp_test.py:23\x1b[0m\n"
            "\x1b[38;5;7m    \x1b[39m\x1b[38;5;167mNone\x1b[39m \x1b[2m(NoneType)\x1b[0m\n"
        )

    def flush_test(self, output: StringIO) -> None:
        xp(None, o=output, f=False)

        assert CRE_ANSI.sub("", output.getvalue()) == ("tests/debugging/xp_test.py:31\n    None (NoneType)\n")

    def width_test(self, output: StringIO) -> None:
        xp("This string is longer than 40 chars.", o=output, w=40)

        assert CRE_ANSI.sub("", output.getvalue()) == (
            "tests/debugging/xp_test.py:36\n"
            "    (\n"
            "        'This string is longer than 40'\n"
            "        ' chars.'\n"
            "    ) (str)\n"
        )

    def return_test(self, output: StringIO) -> None:
        result = xp(1 + 1, o=output)

        assert CRE_ANSI.sub("", output.getvalue()) == ("tests/debugging/xp_test.py:47\n  1 + 1:\n    2 (int)\n")
        assert result == 2

    def return_none_test(self, output: StringIO) -> None:
        result = xp(o=output)

        assert CRE_ANSI.sub("", output.getvalue()) == ("tests/debugging/xp_test.py:53\n")
        assert result is None

    def return_multiple_test(self, output: StringIO) -> None:
        result = xp(1, 2, 3, o=output)

        assert CRE_ANSI.sub("", output.getvalue()) == (
            "tests/debugging/xp_test.py:59\n    1 (int)\n    2 (int)\n    3 (int)\n"
        )
        assert result == (1, 2, 3)

    def no_space_test(self, output: StringIO) -> None:
        xp(None, o=output)

        assert CRE_ANSI.sub("", output.getvalue()) == ("tests/debugging/xp_test.py:67\n    None (NoneType)\n")

    def starred_kwargs_test(self, output: StringIO) -> None:
        kwargs = {"o": output, "w": 256}
        xp(None, **kwargs)  # type: ignore because the values are typed as StringIO | int instead of StringIO and int

        assert CRE_ANSI.sub("", output.getvalue()) == ("tests/debugging/xp_test.py:73\n    None (NoneType)\n")
