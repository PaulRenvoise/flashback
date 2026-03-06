import collections
from types import ModuleType

import pytest
import re

from flashback.debugging.formatter import Formatter

from .fixtures import MockClass, mock_function, MockABC


CRE_ANSI = re.compile(
    r"(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]",
    re.IGNORECASE,
)


@pytest.fixture(scope="class")
def formatter() -> Formatter:
    return Formatter()


class FormatterTest:
    def format_test(self, formatter: Formatter) -> None:
        arguments = [(None, None)]
        content = formatter.format("<filename>", 1, arguments, None)

        assert CRE_ANSI.sub("", content) == ("<filename>:1\n    None (NoneType)")

    def format_long_test(self, formatter: Formatter) -> None:
        arguments = [(None, "a" * 150)]
        content = formatter.format("<filename>", 1, arguments, None)

        assert CRE_ANSI.sub("", content) == (
            "<filename>:1\n"
            "    (\n"
            "        'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'\n"  # noqa: E501
            "        'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'\n"
            "    ) (str)"
        )

    def format_empty_test(self, formatter: Formatter) -> None:
        arguments = []
        content = formatter.format("<filename>", 1, arguments, None)

        assert CRE_ANSI.sub("", content) == ("<filename>:1")

    def format_raw_test(self, formatter: Formatter) -> None:
        arguments = [(None, None)]
        content = formatter.format("<filename>", 1, arguments, None)

        assert content == (
            "\x1b[2m<filename>:1\x1b[0m\n\x1b[38;5;7m    \x1b[39m\x1b[38;5;167mNone\x1b[39m \x1b[2m(NoneType)\x1b[0m"
        )

    def format_named_test(self, formatter: Formatter) -> None:
        arguments = [("var", None)]
        content = formatter.format("<filename>", 1, arguments, None)

        assert CRE_ANSI.sub("", content) == ("<filename>:1\n  var:\n    None (NoneType)")

    def format_multiple_test(self, formatter: Formatter) -> None:
        arguments = [("var_1", None), ("var_2", None), ("var_3", None)]
        content = formatter.format("<filename>", 1, arguments, None)

        assert CRE_ANSI.sub("", content) == (
            "<filename>:1\n  var_1:\n    None (NoneType)\n  var_2:\n    None (NoneType)\n  var_3:\n    None (NoneType)"
        )

    def format_warning_test(self, formatter: Formatter) -> None:
        arguments = [(None, None)]
        content = formatter.format("<filename>", 1, arguments, "warning")

        assert CRE_ANSI.sub("", content) == ("<filename>:1 (warning)\n    None (NoneType)")

    def int_test(self, formatter: Formatter) -> None:
        arguments = [(None, 1)]
        content = formatter.format("<filename>", 1, arguments, None)

        assert CRE_ANSI.sub("", content) == ("<filename>:1\n    1 (int)")

    def bool_test(self, formatter: Formatter) -> None:
        arguments = [(None, True)]
        content = formatter.format("<filename>", 1, arguments, None)

        assert CRE_ANSI.sub("", content) == ("<filename>:1\n    True (bool)")

    def str_test(self, formatter: Formatter) -> None:
        arguments = [(None, "abc")]
        content = formatter.format("<filename>", 1, arguments, None)

        assert CRE_ANSI.sub("", content) == ("<filename>:1\n    'abc' (str)")

    def bytes_test(self, formatter: Formatter) -> None:
        arguments = [(None, b"abc")]
        content = formatter.format("<filename>", 1, arguments, None)

        assert CRE_ANSI.sub("", content) == ("<filename>:1\n    b'abc' (bytes)")

    def list_test(self, formatter: Formatter) -> None:
        arguments = [(None, [1, 2, 3])]
        content = formatter.format("<filename>", 1, arguments, None)

        assert CRE_ANSI.sub("", content) == ("<filename>:1\n    [\n        1,\n        2,\n        3,\n    ] (list)")

    def tuple_test(self, formatter: Formatter) -> None:
        arguments = [(None, (1, 2, 3))]
        content = formatter.format("<filename>", 1, arguments, None)

        assert CRE_ANSI.sub("", content) == ("<filename>:1\n    (\n        1,\n        2,\n        3,\n    ) (tuple)")

    def set_test(self, formatter: Formatter) -> None:
        arguments = [(None, {1, 2, 3})]
        content = formatter.format("<filename>", 1, arguments, None)

        assert CRE_ANSI.sub("", content) == ("<filename>:1\n    {\n        1,\n        2,\n        3,\n    } (set)")

    def frozenset_test(self, formatter: Formatter) -> None:
        arguments = [(None, frozenset({1, 2, 3}))]
        content = formatter.format("<filename>", 1, arguments, None)

        assert CRE_ANSI.sub("", content) == (
            "<filename>:1\n    frozenset({\n        1,\n        2,\n        3,\n    }) (frozenset)"
        )

    def deque_test(self, formatter: Formatter) -> None:
        arguments = [(None, collections.deque([1, 2, 3]))]
        content = formatter.format("<filename>", 1, arguments, None)

        assert CRE_ANSI.sub("", content) == (
            "<filename>:1\n    deque([\n        1,\n        2,\n        3,\n    ]) (deque)"
        )

    def dict_test(self, formatter: Formatter) -> None:
        arguments = [(None, {"a": 1, "b": 2, "c": 3})]
        content = formatter.format("<filename>", 1, arguments, None)

        assert CRE_ANSI.sub("", content) == (
            "<filename>:1\n    {\n        'a': 1,\n        'b': 2,\n        'c': 3,\n    } (dict)"
        )

    def ordereddict_test(self, formatter: Formatter) -> None:
        arguments = [(None, collections.OrderedDict({"a": 1, "b": 2, "c": 3}))]
        content = formatter.format("<filename>", 1, arguments, None)

        assert CRE_ANSI.sub("", content) == (
            "<filename>:1\n    OrderedDict({\n        'a': 1,\n        'b': 2,\n        'c': 3,\n    }) (OrderedDict)"
        )

    def defaultdict_test(self, formatter: Formatter) -> None:
        arguments = [(None, collections.defaultdict(int, {"a": 1, "b": 2, "c": 3}))]
        content = formatter.format("<filename>", 1, arguments, None)

        assert CRE_ANSI.sub("", content) == (
            "<filename>:1\n"
            "    defaultdict(<class 'int'>, {\n"
            "        'a': 1,\n"
            "        'b': 2,\n"
            "        'c': 3,\n"
            "    }) (defaultdict)"
        )

    def counter_test(self, formatter: Formatter) -> None:
        arguments = [(None, collections.Counter(["a", "b", "b", "c", "c", "c"]))]
        content = formatter.format("<filename>", 1, arguments, None)

        assert CRE_ANSI.sub("", content) == (
            "<filename>:1\n    Counter({\n        'a': 1,\n        'b': 2,\n        'c': 3,\n    }) (Counter)"
        )

    def generator_test(self, formatter: Formatter) -> None:
        arguments = [(None, (i for i in range(1, 4)))]
        content = formatter.format("<filename>", 1, arguments, None)

        assert CRE_ANSI.sub("", content) == (
            "<filename>:1\n    (\n        1,\n        2,\n        3,\n    ) (generator)"
        )

    def function_test(self, formatter: Formatter) -> None:
        arguments = [(None, mock_function)]
        content = formatter.format("<filename>", 1, arguments, None)

        assert CRE_ANSI.sub("", content) == ("<filename>:1\n    mock_function(a: int, b: int) -> int (function)")

    def module_test(self, formatter: Formatter) -> None:
        arguments = [(None, collections)]
        content = formatter.format("<filename>", 1, arguments, None)

        content = CRE_ANSI.sub("", content)
        assert "Name:" in content
        assert "Location:" in content
        assert "Contents:" in content
        assert "OrderedDict (type)" in content
        assert "(module)" in content

    def module_with_empty_path_test(self, formatter: Formatter) -> None:
        module = ModuleType("mock_module")
        module.__path__ = []  # type: ignore[attr-defined]

        arguments = [(None, module)]
        content = formatter.format("<filename>", 1, arguments, None)

        content = CRE_ANSI.sub("", content)
        assert "Name:" in content
        assert "Location:" in content
        assert "<unknown>" in content

    def abc_meta_test(self, formatter: Formatter) -> None:
        arguments = [(None, MockClass)]
        content = formatter.format("<filename>", 1, arguments, None)

        assert CRE_ANSI.sub("", content) == ("<filename>:1\n    MockClass < object (type)")

    def type_test(self, formatter: Formatter) -> None:
        arguments = [(None, MockABC)]
        content = formatter.format("<filename>", 1, arguments, None)

        assert CRE_ANSI.sub("", content) == ("<filename>:1\n    MockABC < ABC < object (ABCMeta)")

    def namedtuple_test(self, formatter: Formatter) -> None:
        MockNamedTuple = collections.namedtuple("MockNamedTuple", ["a", "b"])  # noqa: PYI024
        arguments = [(None, MockNamedTuple(a=1, b=2))]
        content = formatter.format("<filename>", 1, arguments, None)

        assert CRE_ANSI.sub("", content) == ("<filename>:1\n    MockNamedTuple(a=1, b=2) (MockNamedTuple)")

    def method_test(self, formatter: Formatter) -> None:
        arguments = [(None, MockClass().mock_method)]
        content = formatter.format("<filename>", 1, arguments, None)

        assert CRE_ANSI.sub("", content) == ("<filename>:1\n    MockClass.mock_method() -> None (method)")

    def staticmethod_test(self, formatter: Formatter) -> None:
        arguments = [(None, MockClass().mock_staticmethod)]
        content = formatter.format("<filename>", 1, arguments, None)

        assert CRE_ANSI.sub("", content) == ("<filename>:1\n    MockClass.mock_staticmethod() -> None (function)")

    def classmethod_test(self, formatter: Formatter) -> None:
        arguments = [(None, MockClass().mock_classmethod)]
        content = formatter.format("<filename>", 1, arguments, None)

        assert CRE_ANSI.sub("", content) == ("<filename>:1\n    MockClass.mock_classmethod() -> None (method)")

    def property_test(self, formatter: Formatter) -> None:
        arguments = [(None, MockClass().mock_property)]
        content = formatter.format("<filename>", 1, arguments, None)

        assert CRE_ANSI.sub("", content) == ("<filename>:1\n    1 (int)")

    def long_str_test(self, formatter: Formatter) -> None:
        arguments = [
            (
                None,
                "This is a very long string that needs to be formatted, and since it contains more than 120 characters, it will be first wrapped, and then formatted.",  # noqa: E501
            ),
        ]
        content = formatter.format("<filename>", 1, arguments, None)

        assert CRE_ANSI.sub("", content) == (
            "<filename>:1\n"
            "    (\n"
            "        'This is a very long string that needs to be formatted, and since it contains more than 120 characters, it wil'\n"  # noqa: E501
            "        'l be first wrapped, and then formatted.'\n"
            "    ) (str)"
        )

    def mixed_iterable_test(self, formatter: Formatter) -> None:
        arguments = [(None, [1, "a", 1500000000, b"b", True, [1, 2, 3], {"a": 1, "b": 2, "c": 3}])]
        content = formatter.format("<filename>", 1, arguments, None)

        assert CRE_ANSI.sub("", content) == (
            "<filename>:1\n"
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

    def nested_dict_test(self, formatter: Formatter) -> None:
        arguments = [(None, {"a": 1, "b": {"a": 1, "b": 2, "c": {"a": 1, "b": 2, "c": 3}}, "c": 3})]
        content = formatter.format("<filename>", 1, arguments, None)

        assert CRE_ANSI.sub("", content) == (
            "<filename>:1\n"
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

    def complex_dict_test(self, formatter: Formatter) -> None:
        dictionary = {
            "regex": re.compile(r"abc", flags=re.IGNORECASE),
            "set": {1, 2, 3},
            "list": [{"a": i, "b": (i for i in range(3))} for i in range(3)],
            "str": "This is a not-so-long yet not-so-short sentence.\n" * 3,
        }
        arguments = [(None, dictionary)]
        content = formatter.format("<filename>", 1, arguments, None)

        assert CRE_ANSI.sub("", content) == (
            "<filename>:1\n"
            "    {\n"
            "        'regex': re.compile('abc', re.IGNORECASE),\n"
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

    def format_code_test(self, formatter: Formatter) -> None:
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

    def format_code_with_start_lineno_test(self, formatter: Formatter) -> None:
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

    def format_code_with_highlight_test(self, formatter: Formatter) -> None:
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

    def format_code_with_start_lineno_and_highlight_test(self, formatter: Formatter) -> None:
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
