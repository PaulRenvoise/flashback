def ordinalize(number):
    """
    Transforms a number to its ordinal representation.

    Since this method should be mostly used in logging messages, only English is supported.

    Examples:
        ```python
        from flashback.formatting import ordinalize

        ordinalize(1)
        #=>  "1st"

        ordinalize(3)
        #=> "3rd"

        ordinalize(144)
        #=> "144th"
        ```

    Params:
        number (int): the number to transform to an ordinal number

    Returns:
        str: the number with the correct ordinal suffix
    """
    number = int(number)

    if number == 1:
        suffix = "st"
    elif number == 2:
        suffix = "nd"
    elif number == 3:
        suffix = "rd"
    elif number in {4, 5, 6, 7, 8, 9, 10, 11, 12, 13}:
        suffix = "th"
    else:
        modulo = abs(number) % 100
        if modulo > 13:
            modulo %= 10

        if modulo == 1:
            suffix = "st"
        elif modulo == 2:
            suffix = "nd"
        elif modulo == 3:
            suffix = "rd"
        else:
            suffix = "th"

    return f"{number}{suffix}"
