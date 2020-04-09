from io import StringIO
import inspect
from textwrap import wrap

import pygments
from pygments.lexers import Python3Lexer  # pylint: disable=no-name-in-module
from pygments.formatters import Terminal256Formatter  # pylint: disable=no-name-in-module

from ..formatting import snakeize
from ..importing import import_class_from_path


class Formatter:
    """
    Implements a formatter to prettify arguments received by `copernicus.debugging.xp`
    and parsed by `copernicus.debugging.Parser.parse`.

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
    LIST_TYPE_TO_SYMBOLS = {
        'list': ('[\n', ']'),
        'set': ('{\n', '}'),
        'frozenset': ('{\n', '}'),
        'tuple': ('(\n', ')'),
        'deque': ('[\n', ']')
    }

    def __init__(self, indent_str='    '):
        self._indent_str = indent_str
        self._indent_str_len = len(indent_str)

        self._width = None

        self._buffer = None

        self._style_cache = {}
        self._code_lexer = Python3Lexer(ensurenl=False)

    def format(self, filename, lineno, arguments, warning, style='jellybeans', width=120):
        """
        Formats the output of `copernicus.debugging.Parser.parse` following the given style and width.

        Params:
            - `filename (str)` the filename from where `copernicus.debugging.xp` has been called
            - `lineno (int)` the line number from where `copernicus.debugging.xp` has been called
            - `arguments (list<tuple>)` the arguments to format, as name-value couples
            - `warning (str)` the error encountered when parsing the code that called `copernicus.debugging.xp` or None
            - `style (str)` the style to use when formatting code (default: 'jellybeans')
            - `width (int)` the maximum width before wrapping the output (default: 120)

        Returns:
            -   `str` the location of the call to `copernicus.debugging.xp` and the formatted arguments
        """
        self._width = width

        style_class = import_class_from_path(style, '.styles')
        code_formatter = self._style_cache.setdefault(style, Terminal256Formatter(style=style_class))

        # We need to use ANSI color coding because pygments can only highlight code
        content = f"\033[2m{filename}:{lineno}"
        if warning:
            content += f" ({warning})"
        content += "\033[0m\n"

        if len(arguments) == 0:
            return content[:-1]  # Remove the last newline

        arguments_content = []
        for (name, value) in arguments:
            argument_content = f"  {name}:\n" if name is not None else ''

            # self._format is called recursively, so we use a stream
            # to progressively write the formatting without passing it around
            self._buffer = StringIO()

            self._format(value)

            buffered_content = self._buffer.getvalue()
            argument_content += pygments.highlight(buffered_content, lexer=self._code_lexer, formatter=code_formatter)

            argument_content += f" \033[2m({value.__class__.__name__})\033[0m"

            arguments_content.append(argument_content)

        content += '\n'.join(arguments_content)

        return content

    def _format(self, value, current_indent=1, force_indent=True):
        if force_indent:
            self._buffer.write(current_indent * self._indent_str)

        next_indent = current_indent + 1

        try:
            # Converts classes such as OrderedDict, Counter, etc.
            # Converts ABCMeta types to abc_meta
            class_name = snakeize(value.__class__.__name__, acronyms=['ABC'])

            method = getattr(self, f"_format_{class_name}")
            method(value, current_indent, next_indent)
        except AttributeError:
            self._format_raw(value, current_indent, next_indent)

    def _format_abc_meta(self, meta, _current_indent, _next_indent):
        self._format_type(meta, _current_indent, _next_indent)

    def _format_type(self, cls, _current_indent, _next_indent):
        self._buffer.write(' < '.join([x.__qualname__ for x in cls.__mro__]))

    def _format_module(self, module, current_indent, next_indent):
        prefix = current_indent * self._indent_str
        nested_prefix = next_indent * self._indent_str
        suffix = '\n'

        self._buffer.write('Name:\n')
        self._buffer.write(nested_prefix + module.__name__ + suffix)
        self._buffer.write(prefix + 'Location:\n')
        self._buffer.write(nested_prefix + module.__path__[0] + suffix)
        self._buffer.write(prefix + 'Contents:\n')
        nested_prefix += '- '
        for key, value in module.__dict__.items():
            if not key.startswith('_'):
                content = f"{key} ({value.__class__.__name__})"
                self._buffer.write(nested_prefix + content + suffix)

    def _format_method(self, method, _current_indent, _next_indent):
        self._format_function(method, _current_indent, _next_indent)

    def _format_function(self, function, _current_indent, _next_indent):
        self._buffer.write(function.__qualname__)
        self._buffer.write(str(inspect.signature(function)))

    def _format_counter(self, counter, current_indent, next_indent):
        self._format_dict(counter, current_indent, next_indent)

    def _format_defaultdict(self, default_dict, current_indent, next_indent):
        self._format_dict(default_dict, current_indent, next_indent)

    def _format_ordered_dict(self, ordered_dict, current_indent, next_indent):
        self._format_dict(ordered_dict, current_indent, next_indent)

    def _format_dict(self, dictionary, current_indent, next_indent):
        start = '{\n'
        prefix = next_indent * self._indent_str
        separator = ': '
        suffix = ',\n'
        end = '}'

        self._buffer.write(start)
        for key, value in dictionary.items():
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
        suffix = ',\n'
        start, end = self.LIST_TYPE_TO_SYMBOLS[iterable.__class__.__name__]

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
            start = '(\n'
            prefix = next_indent * self._indent_str
            suffix = '\n'
            end = ')'

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
                print(prefix + repr(line) + suffix)
                self._buffer.write(prefix + repr(line) + suffix)
            self._buffer.write(current_indent * self._indent_str + end)

    def _format_generator(self, generator, current_indent, next_indent):
        start = '(\n'
        suffix = ',\n'
        end = ')'

        self._buffer.write(start)
        for item in generator:
            self._format(item, next_indent, True)
            self._buffer.write(suffix)
        self._buffer.write(current_indent * self._indent_str + end)

    def _format_raw(self, value, current_indent, next_indent):
        representation = repr(value)
        lines = representation.splitlines(True)

        if len(lines) > 1 or (len(representation) + (current_indent * self._indent_str_len)) >= self._width:
            start = '(\n'
            prefix = next_indent * self._indent_str
            suffix = '\n'
            end = ')'

            self._buffer.write(start)
            wrap_at = self._width - (next_indent * self._indent_str_len)
            for line in lines:
                sub_lines = wrap(line, wrap_at)
                for sub_line in sub_lines:
                    self._buffer.write(prefix + sub_line + suffix)
            self._buffer.write(current_indent * self._indent_str + end)
        else:
            self._buffer.write(representation)
