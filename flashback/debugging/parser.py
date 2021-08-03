import ast
import os
from textwrap import dedent

import regex

from .get_call_context import get_call_context
from .get_frameinfo import get_frameinfo


class Parser:
    """
    Implements a parser to extract the code context from which `flashback.debugging.xp` is called.

    First, goes back in the call stack to locate the call made to `flashback.debugging.xp`,
    then extracts the complete statement (handling multi-lines calls),
    and finds out the name and representation of the given arguments based on the identified snippet.

    If needed, flattens the multi-line parameters to use them as argument names, using
    `CRE_OPENING_BRACKET` and `CRE_CLOSING_BRACKET`.
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
    CRE_OPENING_BRACKET = regex.compile(r"(\{|\[|\()\s")
    CRE_CLOSING_BRACKET = regex.compile(r"\s(\}|\]|\))")

    def __init__(self, _offset=2):
        # This is useful for tests or direct call to `Parser.parse` (in that case use 1)
        self._offset = _offset

    def parse(self, *arguments):
        """
        Parses the arguments received from the code context in which `flashback.debugging.xp` has
        been called, and enriches the arguments values with their names (or representation).

        We must accept all arguments in a greedy way to emulate the behavior of
        `flashback.debugging.xp`, as we call directly this method when testing.

        Params:
            arguments (tuple<Any>): every positional arguments

        Returns:
            str: the filename from where `flashback.debugging.xp` has been called
            int: the line number from where `flashback.debugging.xp` has been called
            list<tuple>: the arguments parsed, as name-value couples
            str: the error encountered when parsing the code or None
        """
        try:
            # We access [2] because an end-user call to xp() calls this code (thus, two layers of calls)
            # If this code would have been called directly by the end-user, we would need to access [1]
            frameinfo = get_frameinfo(self._offset)

            filename = os.path.relpath(frameinfo.filename)
            lineno = frameinfo.lineno

            node, code, warning = self._parse_call(frameinfo, filename)
            if node and code:
                parsed_arguments = self._parse_arguments(node, code, arguments)
            else:  # parsing failed
                parsed_arguments = self._default_arguments_parsing(arguments)
        except Exception as e:  # pylint: disable=broad-except
            filename = "<unknown>"
            lineno = 0
            parsed_arguments = self._default_arguments_parsing(arguments)
            warning = f"error parsing code, {e} ({e.__class__.__name__})"

        return filename, lineno, parsed_arguments, warning

    @staticmethod
    def _parse_call(frameinfo, filename):
        context, _, boundaries = get_call_context(frameinfo)
        if not context:
            return None, None, "error parsing code, no code context found"

        call_statement = dedent("".join(context[slice(*boundaries)]))

        node = ast.parse(call_statement, filename=filename).body[0].value
        if not isinstance(node, ast.Call):
            return None, None, f"error parsing code, found ast.{node.__class__.__name__} instead of ast.Call"

        call_statement_lines = [line for line in call_statement.split("\n") if line]

        return node, call_statement_lines, None

    def _parse_arguments(self, call_node, code_lines, arguments):  # pylint: disable=too-many-locals
        parsed_arguments = []

        arguments_positions = self._get_arguments_positions(call_node, code_lines)
        for i, argument in enumerate(arguments):
            try:
                arg_node = call_node.args[i]
            except IndexError:
                parsed_arguments.append((None, argument))

                continue

            if isinstance(arg_node, ast.Name):
                parsed_arguments.append((arg_node.id, argument))
            elif isinstance(arg_node, self.COMPLEX_NODES):
                position = arguments_positions[i]

                name_lines = []
                # We do end_line + 1 to have the range contain the actual end_line defined above
                for current_line in range(position["start_line"], position["end_line"] + 1):
                    start = position["start_col"] if current_line == position["start_line"] else None
                    end = position["end_col"] if current_line == position["end_line"] else None

                    name_lines.append(code_lines[current_line][start:end].strip(" "))

                argument_name = " ".join(name_lines)
                argument_name = self.CRE_CLOSING_BRACKET.sub(r"\1", self.CRE_OPENING_BRACKET.sub(r"\1", argument_name))
                argument_name = argument_name.strip()

                parsed_arguments.append((argument_name, argument))
            else:
                parsed_arguments.append((None, argument))

        return parsed_arguments

    @staticmethod
    def _get_arguments_positions(call_node, code_lines):
        # This whole method exist only because before python 3.8.0, the
        # end_lineno and end_col_offset attribute are not given for all ast nodes (https://bugs.python.org/issue33416),
        # so finding the position of a given argument is dependent on the following ones.
        # Since 3.8.0, it's as simple as:
        #     start_line = arg_node.lineno - 1
        #     start_col = arg_node.col_offset
        #     end_line = arg_node.end_lineno - 1
        #     end_col = arg_node.end_col_offset
        arguments_positions = []

        default_end_line = len(code_lines) - 1
        default_end_col = -1
        for i, arg_node in enumerate(call_node.args):
            positions = {
                "start_line": arg_node.lineno - 1,
                "start_col": arg_node.col_offset,
                "end_line": default_end_line,
                "end_col": default_end_col
            }
            if isinstance(arg_node, (ast.ListComp, ast.GeneratorExp)):
                positions["start_col"] -= 1

            if i > 0:
                arguments_positions[-1]["end_line"] = positions["start_line"]

                # Handles cases where there is no space after the comma
                try:
                    comma_index = code_lines[positions["start_line"]][:positions["start_col"]].rindex(",")
                    separator_len = positions["start_col"] - comma_index
                except ValueError:
                    # No comma found on this line, meaning we're multiline: ",\r"
                    separator_len = 2

                arguments_positions[-1]["end_col"] = positions["start_col"] - separator_len

            arguments_positions.append(positions)

        if arguments_positions and call_node.keywords:
            kwarg_node = call_node.keywords[0]

            arguments_positions[-1]["end_line"] = kwarg_node.value.lineno - 1

            # Handles cases where there is no space after the comma
            try:
                comma_index = code_lines[kwarg_node.value.lineno - 1][:kwarg_node.value.col_offset].rindex(",")
                separator_len = kwarg_node.value.col_offset - comma_index
            except ValueError:
                # No comma found on this line, meaning we're multiline: ",\r"
                separator_len = kwarg_node.value.col_offset - 2

            arguments_positions[-1]["end_col"] = kwarg_node.value.col_offset - separator_len

        return arguments_positions

    @staticmethod
    def _default_arguments_parsing(arguments):
        return [(None, argument) for argument in arguments]
