# pylint: disable=no-self-use,redefined-outer-name

from io import StringIO

import pytest
import regex

from flashback.debugging import xp

CRE_ANSI = regex.compile(r"(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]", regex.I)


@pytest.fixture
def output():
    return StringIO()


class TestXp:
    def test_xp(self, output):
        xp(None, o=output)

        assert CRE_ANSI.sub('', output.getvalue()) == (
            "tests/debugging/test_xp.py:20\n"
            "    None (NoneType)\n"
        )

    def test_xp_raw(self, output):
        xp(None, o=output)

        assert output.getvalue() == (
            "\x1b[2mtests/debugging/test_xp.py:28\x1b[0m\n"
            "\x1b[38;5;7m    \x1b[39m\x1b[38;5;167mNone\x1b[39m \x1b[2m(NoneType)\x1b[0m\n"
        )

    def test_xp_flush(self, output):
        xp(None, o=output, f=False)

        assert CRE_ANSI.sub('', output.getvalue()) == (
            "tests/debugging/test_xp.py:36\n"
            "    None (NoneType)\n"
        )

    def test_xp_width(self, output):
        xp('This string is longer than 40 chars.', o=output, w=40)

        assert CRE_ANSI.sub('', output.getvalue()) == (
            "tests/debugging/test_xp.py:44\n"
            "    (\n"
            "        'This string is longer than 40'\n"
            "        ' chars.'\n"
            "    ) (str)\n"
        )

    def test_xp_return(self, output):
        result = xp(1 + 1, o=output)

        assert CRE_ANSI.sub('', output.getvalue()) == (
            "tests/debugging/test_xp.py:55\n"
            "  1 + 1:\n"
            "    2 (int)\n"
        )
        assert result == 2

    def test_xp_return_none(self, output):
        result = xp(o=output)

        assert CRE_ANSI.sub('', output.getvalue()) == (
            "tests/debugging/test_xp.py:65\n"
        )
        assert result is None

    def test_xp_return_multiple(self, output):
        result = xp(1, 2, 3, o=output)

        assert CRE_ANSI.sub('', output.getvalue()) == (
            "tests/debugging/test_xp.py:73\n"
            "    1 (int)\n"
            "    2 (int)\n"
            "    3 (int)\n"
        )
        assert result == (1, 2, 3)

    def test_xp_no_space(self, output):
        xp(None,o=output)  # pylint: disable=bad-whitespace

        assert CRE_ANSI.sub('', output.getvalue()) == (
            "tests/debugging/test_xp.py:84\n"
            "    None (NoneType)\n"
        )

    def test_xp_starred_kwargs(self, output):
        kwargs = {'o': output, 'w': 256}
        xp(None, **kwargs)

        assert CRE_ANSI.sub('', output.getvalue()) == (
            "tests/debugging/test_xp.py:93\n"
            "    None (NoneType)\n"
        )
