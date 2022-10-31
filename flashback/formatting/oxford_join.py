from typing import Sequence


def oxford_join(sequence: Sequence[str], sep: str = ", ", couple_sep: str = " and ", last_sep: str = ", and ", quotes: bool = False) -> str:
    """
    Joins a list of string to a comma-separated sentence in a more english fashion than the
    builtin `.join()`.

    Examples:
        ```python
        from flashback.formatting import oxford_join

        oxford_join("A", "B")
        #=> "A and B"

        oxford_join("A", "B", "C")
        #=> "A, B, and C"

        oxford_join("A", "B", "C", last_sep=", or ")
        #=> "A, B, or C"
        ```

    Params:
        sequence: the sequence holding the items to join
        sep: the separator used when there is more than two items in the sequence
        couple_sep: the separator to use if there is only two items in the sequence
        last_sep: the separator to use for the last two items of the sequence
        quotes: whether or not to add quotes around each item of the sequence

    Returns:
        the joined strings
    """
    if len(sequence) == 0:
        return ""

    if quotes:
        sequence = [f"\"{item}\"" for item in sequence]
    else:
        sequence = [str(item) for item in sequence]

    if len(sequence) == 1:
        return sequence[0]

    if len(sequence) == 2:
        return couple_sep.join(sequence)

    enumeration = sep.join(sequence[:-1])

    return f"{enumeration}{last_sep}{sequence[-1]}"
