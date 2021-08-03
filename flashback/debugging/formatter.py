from io import StringIO
import inspect
from textwrap import wrap

import pygments
from pygments.formatters.terminal256 import Terminal256Formatter
from pygments.lexers.python import PythonLexer

from .filters import CallHighlightFilter, DecoratorOperatorFilter, TypeHighlightFilter
from .styles import Jellybeans


class Formatter:
    """
    Implements a formatter to prettify arguments received by `flashback.debugging.xp` and parsed
    by `flashback.debugging.parser`.

    Currently has special formatting for the following types:
        - str / bytes
        - list / tuple / set / frozenset / deque
        - dict / OrderedDict / defaultdict / Counter
        - module
        - type / ABCMeta
        - function / method
        - Generator

    Formats all other types via their __repr__ method.
    """
    TYPE_TO_SYMBOLS = {
        "deque": ("deque([\n", "])"),
        "frozenset": ("frozenset({\n", "})"),
        "list": ("[\n", "]"),
        "set": ("{\n", "}"),
        "tuple": ("(\n", ")"),
        "Counter": ("Counter({\n", "})"),
        "defaultdict": ("defaultdict(_TYPE_, {\n", "})"),
        "dict": ("{\n", "}"),
        "OrderedDict": ("OrderedDict({\n", "})"),
    }
    DIM_START = "\033[2m"
    DIM_END = "\033[0m"

    def __init__(self, indent_str="    "):
        """
        Params:
            indent_str (str): the indentation string to use
        """
        self._indent_str = indent_str
        self._indent_str_len = len(indent_str)

        self._width = None

        self._buffer = None

        self._code_lexer = PythonLexer(
            ensurenl=False,
            filters=[
                DecoratorOperatorFilter(),
                CallHighlightFilter(),
                TypeHighlightFilter(
                    names=[
                        "bool",
                        "bytearray",
                        "bytes",
                        "dict",
                        "float",
                        "frozenset",
                        "int",
                        "list",
                        "object",
                        "set",
                        "str",
                        "tuple",
                    ],
                ),
            ]
        )
        self._code_formatter = Terminal256Formatter(style=Jellybeans)

    def format(self, filename, lineno, arguments, warning, width=120):
        """
        Formats the output of `Parser.parse` following the given style and width.

        Params:
            filename (str): the filename from where `flashback.debugging.xp` has been called
            lineno (int): the line number from where `flashback.debugging.xp` has been called
            arguments (list<tuple>): the arguments to format, as name-value couples
            warning (str): the error encountered when parsing the code or None
            width (int): the maximum width before wrapping the output

        Returns:
            str: the formatted arguments, and location of the call to `flashback.debugging.xp`
        """
        self._width = width

        # We need to use ANSI color coding because pygments can only highlight code
        content = f"\033[2m{filename}:{lineno}"
        if warning:
            content += f" ({warning})"
        content += "\033[0m\n"

        if len(arguments) == 0:
            return content[:-1]  # Remove the last newline

        arguments_content = []
        for (name, value) in arguments:
            argument_content = f"  {name}:\n" if name is not None else ""

            # self._format is called recursively, so we use a stream
            # to progressively write the formatting without passing it around
            self._buffer = StringIO()

            self._format(value)

            buf = self._buffer.getvalue()

            argument_content += self._highlight(buf)
            argument_content += f" \033[2m({value.__class__.__name__})\033[0m"

            arguments_content.append(argument_content)

        content += "\n".join(arguments_content)

        return content

    def format_code(self, lines, start_lineno=1, highlight=None):
        """
        Formats code with syntax highlighting and line numbers, with optional highlighting of
        specific range of lines.

        Params:
            lines (Iterable<str>): the lines of code to render
            start_lineno (int): the line number of the code's first line
            highlight (tuple<int>): the start and end indices of the code to highlight

        Returns:
            str: the formatted and highlighted code
        """
        linenos = list(range(start_lineno, start_lineno + len(lines) + 2))

        pad_len = len(str(max(linenos)))
        lines_with_linenos = []
        for lineno, line in zip(linenos, lines):
            lines_with_linenos.append(f"{lineno:{pad_len}} {line}")

        if highlight is not None:
            start = highlight[0]
            end = highlight[1]

            # Dim the context instead of highlighting the focus
            highlighted_lines = []

            highlighted_lines.append(self.DIM_START)
            highlighted_lines.append(self._highlight("".join(lines_with_linenos[:start])))
            highlighted_lines.append(f"{self.DIM_END}\n")

            highlighted_lines.append(self._highlight("".join(lines_with_linenos[start:end])))

            highlighted_lines.append(f"{self.DIM_START}\n")
            highlighted_lines.append(self._highlight("".join(lines_with_linenos[end:])))
            highlighted_lines.append(self.DIM_END)

            return "".join(highlighted_lines)

        return self._highlight("".join(lines_with_linenos))

    def _format(self, value, current_indent=1, force_indent=True):
        if force_indent:
            self._buffer.write(current_indent * self._indent_str)

        next_indent = current_indent + 1

        try:
            # Converts classes such as OrderedDict, Counter, etc.
            class_name = value.__class__.__name__

            method = getattr(self, f"_format_{class_name}")
            method(value, current_indent, next_indent)
        except AttributeError:
            self._format_raw(value, current_indent, next_indent)

    def _format_ABCMeta(self, meta, _current_indent, _next_indent):  # pylint: disable=invalid-name
        self._format_type(meta, _current_indent, _next_indent)

    def _format_type(self, cls, _current_indent, _next_indent):
        self._buffer.write(" < ".join([x.__qualname__ for x in cls.__mro__]))

    def _format_module(self, module, current_indent, next_indent):
        prefix = current_indent * self._indent_str
        nested_prefix = next_indent * self._indent_str
        suffix = "\n"

        self._buffer.write("Name:\n")
        self._buffer.write(nested_prefix + module.__name__ + suffix)
        self._buffer.write(prefix + "Location:\n")
        self._buffer.write(nested_prefix + module.__path__[0] + suffix)
        self._buffer.write(prefix + "Contents:\n")
        nested_prefix += "- "
        for key, value in module.__dict__.items():
            if not key.startswith("_"):
                content = f"{key} ({value.__class__.__name__})"
                self._buffer.write(nested_prefix + content + suffix)

    def _format_method(self, method, _current_indent, _next_indent):
        self._format_function(method, _current_indent, _next_indent)

    def _format_function(self, function, _current_indent, _next_indent):
        self._buffer.write(function.__qualname__)
        self._buffer.write(str(inspect.signature(function)))

    def _format_Counter(self, counter, current_indent, next_indent):  # pylint: disable=invalid-name
        self._format_mapping(counter, current_indent, next_indent)

    def _format_defaultdict(self, default_dict, current_indent, next_indent):
        self._format_mapping(default_dict, current_indent, next_indent)

    def _format_OrderedDict(self, ordered_dict, current_indent, next_indent):  # pylint: disable=invalid-name
        self._format_mapping(ordered_dict, current_indent, next_indent)

    def _format_dict(self, dictionary, current_indent, next_indent):
        self._format_mapping(dictionary, current_indent, next_indent)

    def _format_mapping(self, mapping, current_indent, next_indent):
        prefix = next_indent * self._indent_str
        separator = ": "
        suffix = ",\n"
        start, end = self.TYPE_TO_SYMBOLS[mapping.__class__.__name__]

        # We're be processing a defaultdict
        if "_TYPE_" in start:
            start = start.replace("_TYPE_", repr(mapping.default_factory))

        self._buffer.write(start)
        for key, value in mapping.items():
            self._buffer.write(prefix)
            self._format(key, next_indent, False)
            self._buffer.write(separator)
            self._format(value, next_indent, False)
            self._buffer.write(suffix)
        self._buffer.write(current_indent * self._indent_str + end)

    def _format_list(self, iterable, current_indent, next_indent):
        self._format_iterables(iterable, current_indent, next_indent)

    def _format_set(self, iterable, current_indent, next_indent):
        self._format_iterables(iterable, current_indent, next_indent)

    def _format_frozenset(self, iterable, current_indent, next_indent):
        self._format_iterables(iterable, current_indent, next_indent)

    def _format_tuple(self, iterable, current_indent, next_indent):
        self._format_iterables(iterable, current_indent, next_indent)

    def _format_deque(self, iterable, current_indent, next_indent):
        self._format_iterables(iterable, current_indent, next_indent)

    def _format_iterables(self, iterable, current_indent, next_indent):
        suffix = ",\n"
        start, end = self.TYPE_TO_SYMBOLS[iterable.__class__.__name__]

        self._buffer.write(start)
        for value in iterable:
            self._format(value, next_indent, True)
            self._buffer.write(suffix)
        self._buffer.write(current_indent * self._indent_str + end)

    def _format_bytes(self, string, current_indent, next_indent):
        self._format_str(string, current_indent, next_indent)

    def _format_str(self, string, current_indent, next_indent):
        # We substract 3 to take in account the quotes and the newline
        width = self._width - (next_indent * self._indent_str_len) - 3

        if len(string) <= width:
            self._buffer.write(repr(string))
        else:
            start = "(\n"
            prefix = next_indent * self._indent_str
            suffix = "\n"
            end = ")"

            # Wrap the lines to be shorter than width, keeping the newlines
            lines = []
            for line in string.splitlines(True):
                begin = 0
                for pos in range(width, len(line), width):
                    lines.append(line[begin:pos])
                    begin = pos
                lines.append(line[begin:])

            self._buffer.write(start)
            for line in lines:
                self._buffer.write(prefix + repr(line) + suffix)
            self._buffer.write(current_indent * self._indent_str + end)

    def _format_generator(self, generator, current_indent, next_indent):
        start = "(\n"
        suffix = ",\n"
        end = ")"

        self._buffer.write(start)
        for item in generator:
            self._format(item, next_indent, True)
            self._buffer.write(suffix)
        self._buffer.write(current_indent * self._indent_str + end)

    def _format_raw(self, value, current_indent, next_indent):
        representation = repr(value)
        lines = representation.splitlines(True)

        if len(lines) > 1 or (len(representation) + (current_indent * self._indent_str_len)) >= self._width:
            start = "(\n"
            prefix = next_indent * self._indent_str
            suffix = "\n"
            end = ")"

            self._buffer.write(start)
            wrap_at = self._width - (next_indent * self._indent_str_len)
            for line in lines:
                sub_lines = wrap(line, wrap_at)
                for sub_line in sub_lines:
                    self._buffer.write(prefix + sub_line + suffix)
            self._buffer.write(current_indent * self._indent_str + end)
        else:
            self._buffer.write(representation)

    def _highlight(self, value):
        return pygments.highlight(value, lexer=self._code_lexer, formatter=self._code_formatter)
