def compact(iterable):
    """
    Removes None items from `iterable`.

    Examples:
        ```python
        from flashback.iterating import compact

        for user_id in compact([1058, None, 85, 9264, 19475, None]):
            print(user_id)
        #=> 1058
        #=> 85
        #=> 9264
        #=> 19475
        ```

    Params:
        iterable (Iterable<Any>): the iterable to remove None from

    Returns:
        tuple<Any>: the iterable without duplicates
    """
    return tuple(item for item in iterable if item is not None)
