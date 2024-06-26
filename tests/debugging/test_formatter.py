import collections

import pytest
import regex

from flashback.debugging.formatter import Formatter

from .fixtures import MockClass, mock_function, MockABC


CRE_ANSI = regex.compile(r"(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]", regex.IGNORECASE)


@pytest.fixture(scope="class")
def formatter():
    return Formatter()


class TestFormatter:
    def test_format(self, formatter):
        arguments = [(None, None)]
        content = formatter.format("<filename>", "<lineno>", arguments, None)

        assert CRE_ANSI.sub("", content) == ("<filename>:<lineno>\n    None (NoneType)")

    def test_format_long(self, formatter):
        arguments = [(None, "a" * 150)]
        content = formatter.format("<filename>", "<lineno>", arguments, None)

        assert (
            CRE_ANSI.sub("", content)
            == (
                "<filename>:<lineno>\n"
                "    (\n"
                "        'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'\n"  # noqa: E501
                "        'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'\n"
                "    ) (str)"
            )
        )

    def test_format_empty(self, formatter):
        arguments = []
        content = formatter.format("<filename>", "<lineno>", arguments, None)

        assert CRE_ANSI.sub("", content) == ("<filename>:<lineno>")

    def test_format_raw(self, formatter):
        arguments = [(None, None)]
        content = formatter.format("<filename>", "<lineno>", arguments, None)

        assert content == (
            "\x1b[2m<filename>:<lineno>\x1b[0m\n"
            "\x1b[38;5;7m    \x1b[39m\x1b[38;5;167mNone\x1b[39m \x1b[2m(NoneType)\x1b[0m"
        )

    def test_format_named(self, formatter):
        arguments = [("var", None)]
        content = formatter.format("<filename>", "<lineno>", arguments, None)

        assert CRE_ANSI.sub("", content) == ("<filename>:<lineno>\n  var:\n    None (NoneType)")

    def test_format_multiple(self, formatter):
        arguments = [("var_1", None), ("var_2", None), ("var_3", None)]
        content = formatter.format("<filename>", "<lineno>", arguments, None)

        assert CRE_ANSI.sub("", content) == (
            "<filename>:<lineno>\n"
            "  var_1:\n"
            "    None (NoneType)\n"
            "  var_2:\n"
            "    None (NoneType)\n"
            "  var_3:\n"
            "    None (NoneType)"
        )

    def test_format_warning(self, formatter):
        arguments = [(None, None)]
        content = formatter.format("<filename>", "<lineno>", arguments, "warning")

        assert CRE_ANSI.sub("", content) == ("<filename>:<lineno> (warning)\n    None (NoneType)")

    def test_int(self, formatter):
        arguments = [(None, 1)]
        content = formatter.format("<filename>", "<lineno>", arguments, None)

        assert CRE_ANSI.sub("", content) == ("<filename>:<lineno>\n    1 (int)")

    def test_bool(self, formatter):
        arguments = [(None, True)]
        content = formatter.format("<filename>", "<lineno>", arguments, None)

        assert CRE_ANSI.sub("", content) == ("<filename>:<lineno>\n    True (bool)")

    def test_str(self, formatter):
        arguments = [(None, "abc")]
        content = formatter.format("<filename>", "<lineno>", arguments, None)

        assert CRE_ANSI.sub("", content) == ("<filename>:<lineno>\n    'abc' (str)")

    def test_bytes(self, formatter):
        arguments = [(None, b"abc")]
        content = formatter.format("<filename>", "<lineno>", arguments, None)

        assert CRE_ANSI.sub("", content) == ("<filename>:<lineno>\n    b'abc' (bytes)")

    def test_list(self, formatter):
        arguments = [(None, [1, 2, 3])]
        content = formatter.format("<filename>", "<lineno>", arguments, None)

        assert CRE_ANSI.sub("", content) == (
            "<filename>:<lineno>\n    [\n        1,\n        2,\n        3,\n    ] (list)"
        )

    def test_tuple(self, formatter):
        arguments = [(None, (1, 2, 3))]
        content = formatter.format("<filename>", "<lineno>", arguments, None)

        assert CRE_ANSI.sub("", content) == (
            "<filename>:<lineno>\n    (\n        1,\n        2,\n        3,\n    ) (tuple)"
        )

    def test_set(self, formatter):
        arguments = [(None, {1, 2, 3})]
        content = formatter.format("<filename>", "<lineno>", arguments, None)

        assert CRE_ANSI.sub("", content) == (
            "<filename>:<lineno>\n    {\n        1,\n        2,\n        3,\n    } (set)"
        )

    def test_frozenset(self, formatter):
        arguments = [(None, frozenset({1, 2, 3}))]
        content = formatter.format("<filename>", "<lineno>", arguments, None)

        assert CRE_ANSI.sub("", content) == (
            "<filename>:<lineno>\n"
            "    frozenset({\n"
            "        1,\n"
            "        2,\n"
            "        3,\n"
            "    }) (frozenset)"
        )

    def test_deque(self, formatter):
        arguments = [(None, collections.deque([1, 2, 3]))]
        content = formatter.format("<filename>", "<lineno>", arguments, None)

        assert CRE_ANSI.sub("", content) == (
            "<filename>:<lineno>\n    deque([\n        1,\n        2,\n        3,\n    ]) (deque)"
        )

    def test_dict(self, formatter):
        arguments = [(None, {"a": 1, "b": 2, "c": 3})]
        content = formatter.format("<filename>", "<lineno>", arguments, None)

        assert CRE_ANSI.sub("", content) == (
            "<filename>:<lineno>\n    {\n        'a': 1,\n        'b': 2,\n        'c': 3,\n    } (dict)"
        )

    def test_ordereddict(self, formatter):
        arguments = [(None, collections.OrderedDict({"a": 1, "b": 2, "c": 3}))]
        content = formatter.format("<filename>", "<lineno>", arguments, None)

        assert CRE_ANSI.sub("", content) == (
            "<filename>:<lineno>\n"
            "    OrderedDict({\n"
            "        'a': 1,\n"
            "        'b': 2,\n"
            "        'c': 3,\n"
            "    }) (OrderedDict)"
        )

    def test_defaultdict(self, formatter):
        arguments = [(None, collections.defaultdict(int, {"a": 1, "b": 2, "c": 3}))]
        content = formatter.format("<filename>", "<lineno>", arguments, None)

        assert CRE_ANSI.sub("", content) == (
            "<filename>:<lineno>\n"
            "    defaultdict(<class 'int'>, {\n"
            "        'a': 1,\n"
            "        'b': 2,\n"
            "        'c': 3,\n"
            "    }) (defaultdict)"
        )

    def test_counter(self, formatter):
        arguments = [(None, collections.Counter(["a", "b", "b", "c", "c", "c"]))]
        content = formatter.format("<filename>", "<lineno>", arguments, None)

        assert CRE_ANSI.sub("", content) == (
            "<filename>:<lineno>\n"
            "    Counter({\n"
            "        'a': 1,\n"
            "        'b': 2,\n"
            "        'c': 3,\n"
            "    }) (Counter)"
        )

    def test_generator(self, formatter):
        arguments = [(None, (i for i in range(1, 4)))]
        content = formatter.format("<filename>", "<lineno>", arguments, None)

        assert CRE_ANSI.sub("", content) == (
            "<filename>:<lineno>\n    (\n        1,\n        2,\n        3,\n    ) (generator)"
        )

    def test_function(self, formatter):
        arguments = [(None, mock_function)]
        content = formatter.format("<filename>", "<lineno>", arguments, None)

        assert CRE_ANSI.sub("", content) == ("<filename>:<lineno>\n    mock_function(a, b) (function)")

    def test_module(self, formatter):
        arguments = [(None, collections)]
        content = formatter.format("<filename>", "<lineno>", arguments, None)

        content = CRE_ANSI.sub("", content)
        assert "Name:" in content
        assert "Location:" in content
        assert "Contents:" in content
        assert "OrderedDict (type)" in content
        assert "(module)" in content

    def test_abc_meta(self, formatter):
        arguments = [(None, MockClass)]
        content = formatter.format("<filename>", "<lineno>", arguments, None)

        assert CRE_ANSI.sub("", content) == ("<filename>:<lineno>\n    MockClass < object (type)")

    def test_type(self, formatter):
        arguments = [(None, MockABC)]
        content = formatter.format("<filename>", "<lineno>", arguments, None)

        assert CRE_ANSI.sub("", content) == ("<filename>:<lineno>\n    MockABC < ABC < object (ABCMeta)")

    def test_namedtuple(self, formatter):
        MockNamedTuple = collections.namedtuple("MockNamedTuple", ["a", "b"])  # noqa: PYI024
        arguments = [(None, MockNamedTuple(a=1, b=2))]
        content = formatter.format("<filename>", "<lineno>", arguments, None)

        assert CRE_ANSI.sub("", content) == ("<filename>:<lineno>\n    MockNamedTuple(a=1, b=2) (MockNamedTuple)")

    def test_method(self, formatter):
        arguments = [(None, MockClass().mock_method)]
        content = formatter.format("<filename>", "<lineno>", arguments, None)

        assert CRE_ANSI.sub("", content) == ("<filename>:<lineno>\n    MockClass.mock_method() (method)")

    def test_staticmethod(self, formatter):
        arguments = [(None, MockClass().mock_staticmethod)]
        content = formatter.format("<filename>", "<lineno>", arguments, None)

        assert CRE_ANSI.sub("", content) == ("<filename>:<lineno>\n    MockClass.mock_staticmethod() (function)")

    def test_classmethod(self, formatter):
        arguments = [(None, MockClass().mock_classmethod)]
        content = formatter.format("<filename>", "<lineno>", arguments, None)

        assert CRE_ANSI.sub("", content) == ("<filename>:<lineno>\n    MockClass.mock_classmethod() (method)")

    def test_property(self, formatter):
        arguments = [(None, MockClass().mock_property)]
        content = formatter.format("<filename>", "<lineno>", arguments, None)

        assert CRE_ANSI.sub("", content) == ("<filename>:<lineno>\n    1 (int)")

    def test_long_str(self, formatter):
        arguments = [
            (
                None,
                "This is a very long string that needs to be formatted, and since it contains more than 120 characters, it will be first wrapped, and then formatted.",  # noqa: E501
            ),
        ]
        content = formatter.format("<filename>", "<lineno>", arguments, None)

        assert (
            CRE_ANSI.sub("", content)
            == (
                "<filename>:<lineno>\n"
                "    (\n"
                "        'This is a very long string that needs to be formatted, and since it contains more than 120 characters, it wil'\n"  # noqa: E501
                "        'l be first wrapped, and then formatted.'\n"
                "    ) (str)"
            )
        )

    def test_mixed_iterable(self, formatter):
        arguments = [(None, [1, "a", 1500000000, b"b", True, [1, 2, 3], {"a": 1, "b": 2, "c": 3}])]
        content = formatter.format("<filename>", "<lineno>", arguments, None)

        assert CRE_ANSI.sub("", content) == (
            "<filename>:<lineno>\n"
            "    [\n"
            "        1,\n"
            "        'a',\n"
            "        1500000000,\n"
            "        b'b',\n"
            "        True,\n"
            "        [\n"
            "            1,\n"
            "            2,\n"
            "            3,\n"
            "        ],\n"
            "        {\n"
            "            'a': 1,\n"
            "            'b': 2,\n"
            "            'c': 3,\n"
            "        },\n"
            "    ] (list)"
        )

    def test_nested_dict(self, formatter):
        arguments = [(None, {"a": 1, "b": {"a": 1, "b": 2, "c": {"a": 1, "b": 2, "c": 3}}, "c": 3})]
        content = formatter.format("<filename>", "<lineno>", arguments, None)

        assert CRE_ANSI.sub("", content) == (
            "<filename>:<lineno>\n"
            "    {\n"
            "        'a': 1,\n"
            "        'b': {\n"
            "            'a': 1,\n"
            "            'b': 2,\n"
            "            'c': {\n"
            "                'a': 1,\n"
            "                'b': 2,\n"
            "                'c': 3,\n"
            "            },\n"
            "        },\n"
            "        'c': 3,\n"
            "    } (dict)"
        )

    def test_complex_dict(self, formatter):
        dictionary = {
            "regex": regex.compile(r"abc", regex.IGNORECASE),
            "set": {1, 2, 3},
            "list": [{"a": i, "b": (i for i in range(3))} for i in range(3)],
            "str": "This is a not-so-long yet not-so-short sentence.\n" * 3,
        }
        arguments = [(None, dictionary)]
        content = formatter.format("<filename>", "<lineno>", arguments, None)

        assert CRE_ANSI.sub("", content) == (
            "<filename>:<lineno>\n"
            "    {\n"
            "        'regex': regex.Regex('abc', flags=regex.I | regex.V0),\n"
            "        'set': {\n"
            "            1,\n"
            "            2,\n"
            "            3,\n"
            "        },\n"
            "        'list': [\n"
            "            {\n"
            "                'a': 0,\n"
            "                'b': (\n"
            "                    0,\n"
            "                    1,\n"
            "                    2,\n"
            "                ),\n"
            "            },\n"
            "            {\n"
            "                'a': 1,\n"
            "                'b': (\n"
            "                    0,\n"
            "                    1,\n"
            "                    2,\n"
            "                ),\n"
            "            },\n"
            "            {\n"
            "                'a': 2,\n"
            "                'b': (\n"
            "                    0,\n"
            "                    1,\n"
            "                    2,\n"
            "                ),\n"
            "            },\n"
            "        ],\n"
            "        'str': (\n"
            "            'This is a not-so-long yet not-so-short sentence.\\n'\n"
            "            'This is a not-so-long yet not-so-short sentence.\\n'\n"
            "            'This is a not-so-long yet not-so-short sentence.\\n'\n"
            "        ),\n"
            "    } (dict)"
        )

    def test_format_code(self, formatter):
        code = [
            "framelist = []\n",
            "while frame:\n",
            "    frameinfo = (frame,) + getframeinfo(frame, context)\n",
            "    framelist.append(FrameInfo(*frameinfo))\n",
            "    frame = frame.f_back\n",
            "return framelist\n",
        ]

        content = formatter.format_code(code)

        assert "\x1b[39m" in content
        for lineno, line in enumerate(content.splitlines(), 1):
            assert str(lineno) in line

    def test_format_code_with_start_lineno(self, formatter):
        code = [
            "framelist = []\n",
            "while frame:\n",
            "    frameinfo = (frame,) + getframeinfo(frame, context)\n",
            "    framelist.append(FrameInfo(*frameinfo))\n",
            "    frame = frame.f_back\n",
            "return framelist\n",
        ]
        start_lineno = 1489

        content = formatter.format_code(code, start_lineno=start_lineno)

        assert "\x1b[39m" in content
        for lineno, line in enumerate(content.splitlines(), start_lineno):
            assert str(lineno) in line

    def test_format_code_with_highlight(self, formatter):
        code = [
            "framelist = []\n",
            "while frame:\n",
            "    frameinfo = (frame,) + getframeinfo(frame, context)\n",
            "    framelist.append(FrameInfo(*frameinfo))\n",
            "    frame = frame.f_back\n",
            "return framelist\n",
        ]

        content = formatter.format_code(code, highlight=(2, 3))

        content_lines = content.splitlines()
        assert content_lines[0][:4] == "\x1b[2m"
        assert content_lines[1][-4:] == "\x1b[0m"
        assert content_lines[2][-4:] == "\x1b[2m"
        assert content_lines[-1][-4:] == "\x1b[0m"

    def test_format_code_with_start_lineno_and_highlight(self, formatter):
        code = [
            "framelist = []\n",
            "while frame:\n",
            "    frameinfo = (frame,) + getframeinfo(frame, context)\n",
            "    framelist.append(FrameInfo(*frameinfo))\n",
            "    frame = frame.f_back\n",
            "return framelist\n",
        ]
        start_lineno = 1489

        content = formatter.format_code(code, start_lineno=start_lineno, highlight=(2, 3))

        content_lines = content.splitlines()
        assert "\x1b[39m" in content
        for lineno, line in enumerate(content_lines, start_lineno):
            assert str(lineno) in line
        assert content_lines[0][:4] == "\x1b[2m"
        assert content_lines[1][-4:] == "\x1b[0m"
        assert content_lines[2][-4:] == "\x1b[2m"
        assert content_lines[-1][-4:] == "\x1b[0m"
