from pygments.filters import Filter
from pygments.token import Name


class CallHighlightFilter(Filter):
    """Highlight a normal Name (and Name.*) token with a different token type.
    Example::
        filter = NameHighlightFilter(
            names=['foo', 'bar', 'baz'],
            tokentype=Name.Function,
        )
    This would highlight the names "foo", "bar" and "baz"
    as functions. `Name.Function` is the default token type.
    Options accepted:
    `names` : list of strings
      A list of names that should be given the different token type.
      There is no default.
    `tokentype` : TokenType or string
      A token type or a string containing a token type name that is
      used for highlighting the strings in `names`.  The default is
      `Name.Function`.
    """
    def __init__(self, **kwargs):
        Filter.__init__(self, **kwargs)

        self.tokentype = kwargs.get('tokentype')

    def filter(self, lexer, stream):
        """
        TODO: explain
        """
        try:
            stack = [next(stream)]
        except StopIteration:
            stack = []

        for future_ttype, future_value in stream:
            print(future_ttype, future_value)
            ttype, value = stack.pop()
            if ttype in Name and future_value == '(':
                stack.append((self.tokentype, value))
            else:
                stack.append((ttype, value))

            stack.append((future_ttype, future_value))

        for items in stack:
            yield items
