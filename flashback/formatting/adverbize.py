def adverbize(number):
    """
    Transforms a number to its numeral adverb representation.

    Since this method should be mostly used in logging messages, only English is supported.

    Examples:
        ```python
        from flashback.formatting import adverbize

        adverbize(1)
        #=> "once"

        adverbize(3)
        #=> "thrice"

        adverbize(144)
        #=> "144 times"
        ```

    Params:
        number (int): the number for transform to a numeral adverb

    Returns:
        str: the numeral adverb
    """
    number = int(number)

    if number == 1:
        numeral = "once"
    elif number == 2:
        numeral = "twice"
    elif number == 3:
        numeral = "thrice"
    else:
        numeral = f"{number} times"

    return numeral
