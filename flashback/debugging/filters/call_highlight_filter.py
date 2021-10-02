from pygments.filters import Filter
from pygments.token import Name


class CallHighlightFilter(Filter):
    """
    Modifies the token type of a Name to Name.Function if its value is followed by an opening
    parenthesis.
    """
    def __init__(self, **kwargs):
        """
        Params:
            kwargs (dict): every additional keyword parameters
        """
        Filter.__init__(self, **kwargs)

    def filter(self, lexer, stream):
        """
        Iterates over the stream of tokens and searches for a name followed by an opening paren to
        change its type to Name.Function.

        Many colorscheme highlight calls, but pygments treats a function call as a simple Name,
        this filter fixes that.

        Because it needs to look at the next token before making a decision about the current one,
        this filter takes the first item of the stream, stores it into a stack, and then iterates
        over the stream (now with an offset of 1), and makes a decision of token tx-1 based on its
        current token tx. Once the decision is made it adds back the token tx-1 and the token tx to
        the stack, and repeats the process. Once the stream is exhausted, it yields the content of
        the stack.

        Params:
            lexer (pygments.lexer.Lexer): the lexer instance
            stream (generator): the stream of couples tokentype-value

        Yields:
            tuple<pygments.token._TokenType, str>: the token type and token value
        """
        try:
            stack = [next(stream)]
        except StopIteration:
            stack = []

        for ttype, value in stream:
            previous_ttype, previous_value = stack.pop()

            if previous_ttype in Name and value == "(":
                stack.append((Name.Function, previous_value))
            else:
                stack.append((previous_ttype, previous_value))

            stack.append((ttype, value))

        for items in stack:
            yield items
