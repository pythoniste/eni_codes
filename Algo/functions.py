"""An advanced exercise about strings handling"""


def first_most_recurring(s: str) -> str | None:
    """
    Find the first most recurring characters or None if there isn't one.

    >>> first_most_recurring("ABC")
    >>> first_most_recurring("ABAC")
    'A'
    >>> first_most_recurring("ABBAC")
    'A'
    >>> first_most_recurring("DADBBBC")
    'B'
    """

    length = len(s)

    # chars is a dictionary made by recursion over a set of letters composing `s`:
    # - keys are a tuple containing:
    #     - the number of occurrences of the character
    #     - the position of the first character
    # - values are the different characters
    #
    # because the position of the letter in the string `s` is unique, there can't be two identical keys.
    # We iterate over unique characters because we used a set.
    chars = {(s.count(c), length - s.index(c)): c for c in set(s)}

    # The key of the previous dictionary has been chosen to match the way max will work:
    # the larger number of occurence will come first.
    # if two letters have the same, the position of the string will sort them out.
    result = max(chars.keys())

    if result[0] == 1:
        # result[0] is the winner.
        # But if the number of occurrences of the winner is 1, that means that there is no duplicate.
        # we return None instead
        return None

    return chars[result]


def first_most_recurring_2(s: str) -> str | None:
    """
    Find the first most recurring characters or None if there isn't one.

    Having the real character position of a relative position from the end of the string is the same thing

    >>> first_most_recurring_2("ABC")
    >>> first_most_recurring_2("ABAC")
    'A'
    >>> first_most_recurring_2("ABBAC")
    'A'
    >>> first_most_recurring_2("DADBBBC")
    'B'
    """

    chars = {(s.count(c), - s.index(c)): c for c in set(s)}
    result = max(chars.keys())

    if result[0] == 1:
        return None

    return chars[result]


if __name__ == "__main__":
    # This allows to use docstrings as test cases and run them.
    import doctest
    doctest.testmod()
