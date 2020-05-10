from pygments.filters import Filter
from pygments.token import Name, Operator


class DecoratorOperatorFilter(Filter):
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
        for ttype, value in stream:
            if ttype is Name.Decorator:
                yield Operator, '@'
                yield Name.Decorator, value[1:]
            else:
                yield ttype, value
