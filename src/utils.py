def clean_whitespace(value: str) -> str:
    """Removes the excess whitespace from the given string.

    For example: "A    long title    " -> "A long title"

    Args:
        value (str): the given string

    Returns:
        str: the string without the excess whitespace
    """
    return " ".join(value.split())


def normalize_str(value: str) -> str:
    """Normalizes the given string.

    The logic of the normalization:
        1. Splits the string to individual parts/words in order to remove excess whitespace.
        2. Joins the parts/words with an underscore.
        3. Converts the string to lower case.

    For example: "A   long movie title" -> "a_long_movie_title".

    Args:
        value (str): the given string

    Returns:
        str: the normalized string
    """

    return "_".join(value.split()).lower()


def get_non_empty(prompt: str) -> str:
    """Asks the user the prompt and excepts a valid non empty value.

    If the user enters an empty value it prints an error and asks the user again.

    Args:
        prompt (str): the given prompt to display to the user.

    Returns:
        str: the value the user entered.
    """

    while True:
        value = clean_whitespace(input(prompt))
        if value:
            return value

        print("\n--- ERROR: Value must not be empty. ---")


def get_int(prompt: str) -> int:
    """Asks the user the prompt and excepts a valid number value.

    If the user enters an invalid number it prints an error and asks the user again.

    Args:
        prompt (str): the given prompt to display to the user.

    Returns:
        int: the number value the user entered.
    """

    while True:
        value = clean_whitespace(input(prompt))
        try:
            return int(value)
        except ValueError:
            print("\n--- ERROR: Must be a valid number. ---")


if __name__ == "__main__":
    pass
