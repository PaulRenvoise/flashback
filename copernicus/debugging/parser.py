import ast
import inspect
import os
import sys
from textwrap import dedent

import regex


class Parser:
    """
    Implements a parser to extract the code context from which `copernicus.debugging.xp` is called.

    First, goes back in the call stack to locate the call made to `copernicus.debugging.xp`
    with the regex `copernicus.debugging.Parser.CRE_XP`,
    then extracts the complete statement (handling multi-lines calls),
    and finds out the name and representation of the given arguments based on the identified snippet.

    If needed, flattens the multi-line parameters to use them as argument names, using
    `copernicus.debugging.Parser.CRE_OPENING_BRACKET` and `copernicus.debugging.Parser.CRE_CLOSING_BRACKET`.
    """
    COMPLEX_NODES = (
        ast.Attribute,
        ast.BoolOp,
        ast.BinOp,
        ast.Call,
        ast.Compare,
        ast.DictComp,
        ast.GeneratorExp,
        ast.IfExp,
        ast.ListComp,
        ast.Subscript,
        ast.SetComp
    )
    CRE_XP = regex.compile(r"xp\s*\(")

    CRE_OPENING_BRACKET = regex.compile(r"(\{|\[|\()\s")
    CRE_CLOSING_BRACKET = regex.compile(r"\s(\}|\]|\))")

    def __init__(self, _offset=2):
        # This is useful for tests or direct call to `Parser.parse` (in that case use 1)
        self._offset = _offset

    def parse(self, *arguments):
        """
        Parses the arguments received from the code context in which `copernicus.debugging.xp` has been called,
        enriches the arguments values with their names (or representation).

        We must accept all arguments in a greedy way to emulate the behavior of `copernicus.debugging.xp`,
        as we call directly this method when testing.

        Params:
            - `arguments (tuple<Any>)` every positional arguments

        Returns:
            - `str` the filename from where `copernicus.debugging.xp` has been called
            - `int` the line number from where `copernicus.debugging.xp` has been called
            - `list<tuple>` the arguments parsed, as name-value couples
            - `str` the error encountered when parsing the code that called `copernicus.debugging.xp` or None
        """
        try:
            # We access [2] because an end-user call to xp() calls this code (thus, two layers of calls)
            # If this code would have been called directly by the end-user, we would need to access [1]
            calling_frame = inspect.stack(context=1)[self._offset]

            filename = os.path.relpath(calling_frame.filename)

            if calling_frame.code_context:
                calling_node, calling_code, lineno, warning = self._parse_code(calling_frame, filename)
                if calling_node and calling_code:
                    parsed_arguments = self._parse_arguments(calling_node, calling_code, arguments)
                else:  # parsing failed
                    parsed_arguments = self._default_arguments_parsing(arguments)
            else:
                lineno = calling_frame.lineno
                parsed_arguments = self._default_arguments_parsing(arguments)
                warning = 'error parsing code, no code context found'
        except Exception as e:  # pylint: disable=broad-except
            filename = '<unknown>'
            lineno = 0
            parsed_arguments = self._default_arguments_parsing(arguments)
            warning = f"error parsing code, {e} ({e.__class__.__name__})"

        return filename, lineno, parsed_arguments, warning

    def _parse_code(self, calling_frame, filename):
        calling_source, _ = inspect.findsource(calling_frame.frame)
        calling_lineno = calling_frame.lineno
        calling_index = calling_lineno - 1
        calling_line = calling_source[calling_index]

        if not self.CRE_XP.search(calling_line):
            return None, None, calling_lineno, f"error parsing code, function call not found at line {calling_lineno}"

        code = dedent(calling_line)
        calling_node = None
        try:
            calling_node = ast.parse(code, filename=filename).body[0].value
        except (SyntaxError, AttributeError) as e:
            extra_index = calling_index
            brackets = 1

            while brackets:
                brackets = code.count('(') - code.count(')')
                extra_index += 1

                calling_lines = calling_source[calling_index:extra_index]
                code = dedent(''.join(calling_lines))
                try:
                    calling_node = ast.parse(code, filename=filename).body[0].value

                    break
                except (SyntaxError, AttributeError):
                    pass

            if not calling_node:
                return None, None, calling_lineno, f"error parsing code, {e} ({e.__class__.__name__})"

        if not isinstance(calling_node, ast.Call):
            return None, None, calling_lineno, f"error parsing code, found {calling_node.__class__} not ast.Call"

        code_lines = [line for line in code.split('\n') if line]
        if sys.version < '3.8':
            code_lines[-1] = code_lines[-1][:-1]

        return calling_node, code_lines, calling_lineno, None

    def _parse_arguments(self, calling_node, code_lines, arguments):  # pylint: disable=too-many-locals
        parsed_arguments = []

        arguments_positions = self._get_arguments_positions(calling_node, code_lines)
        for i, argument in enumerate(arguments):
            try:
                arg_node = calling_node.args[i]
            except IndexError:
                parsed_arguments.append((None, argument))

                continue

            if isinstance(arg_node, ast.Name):
                parsed_arguments.append((arg_node.id, argument))
            elif isinstance(arg_node, self.COMPLEX_NODES):
                position = arguments_positions[i]

                name_lines = []
                # We do end_line + 1 to have the range contain the actual end_line defined above
                for current_line in range(position['start_line'], position['end_line'] + 1):
                    start = position['start_col'] if current_line == position['start_line'] else None
                    end = position['end_col'] if current_line == position['end_line'] else None

                    name_lines.append(code_lines[current_line][start:end].strip(' '))

                argument_name = ' '.join(name_lines)
                argument_name = self.CRE_CLOSING_BRACKET.sub(r"\1", self.CRE_OPENING_BRACKET.sub(r"\1", argument_name))
                argument_name = argument_name.strip()

                parsed_arguments.append((argument_name, argument))
            else:
                parsed_arguments.append((None, argument))

        return parsed_arguments

    @staticmethod
    def _get_arguments_positions(calling_node, code_lines):
        arguments_positions = []

        if sys.version >= '3.8':
            for arg_node in calling_node.args:
                positions = {
                    'start_line': arg_node.lineno - 1,
                    'start_col': arg_node.col_offset,
                    'end_line': arg_node.end_lineno - 1,
                    'end_col': arg_node.end_col_offset
                }

                arguments_positions.append(positions)
        else:
            for i, arg_node in enumerate(calling_node.args):
                positions = {
                    'start_line': arg_node.lineno - 1,
                    'start_col' : arg_node.col_offset, # maybe arg_node.col_offset?
                    'end_line': len(code_lines) - 1, # FIXME: not optimized
                    'end_col': None
                }
                if isinstance(arg_node, (ast.ListComp, ast.GeneratorExp)):
                    positions['start_col'] -= 1

                if i > 0:
                    arguments_positions[-1]['end_line'] = positions['start_line']
                    arguments_positions[-1]['end_col'] = positions['start_col'] - 2

                arguments_positions.append(positions)

        return arguments_positions

    @staticmethod
    def _default_arguments_parsing(arguments):
        return [(None, argument) for argument in arguments]
