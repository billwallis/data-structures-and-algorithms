"""
Implementing the Soundex algorithm.

https://en.wikipedia.org/wiki/Soundex
"""

import logging
from typing import Literal

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(message)s")


DEFAULT_CHAR = " "
REDUCE_CHAR = "-"
DUPLICATE_CHAR = "+"
ENCODING = {
    **{
        # These are simply dropped in the SQL version
        "a": DUPLICATE_CHAR,
        "e": DUPLICATE_CHAR,
        "i": DUPLICATE_CHAR,
        "o": DUPLICATE_CHAR,
        "u": DUPLICATE_CHAR,
    },
    **{
        # These are simply dropped in the SQL version
        "y": REDUCE_CHAR,
        "h": REDUCE_CHAR,
        "w": REDUCE_CHAR,
    },
    **{
        "b": "1",
        "f": "1",
        "p": "1",
        "v": "1",
    },
    **{
        "c": "2",
        "g": "2",
        "j": "2",
        "k": "2",
        "q": "2",
        "s": "2",
        "x": "2",
        "z": "2",
    },
    **{
        "d": "3",
        "t": "3",
    },
    **{
        "l": "4",
    },
    **{
        "m": "5",
        "n": "5",
    },
    **{
        "r": "6",
    },
}


def _encode(word: str) -> str:
    return "".join([ENCODING.get(c.lower(), DEFAULT_CHAR) for c in word])


def _str_get(string: str, index: int) -> str:
    if index < 0:  # DON'T wrap-around like normal
        return ""
    try:
        return string[index]
    except IndexError:
        return ""


def last_3(word: str, index: int) -> tuple[str, str, str]:
    """
    Return the word's previous 3 characters relative to the index.

    The index does not "wrap around" like Python indexes usually do. Out of
    bounds indexes return an empty string.

    For example:

        last_3("abcd", 1) == ("", "a", "b")
    """

    return (
        _str_get(word, index - 2),
        _str_get(word, index - 1),
        _str_get(word, index),
    )


def _soundex(word: str, variant: Literal["american", "tsql"]) -> str:
    logger.debug(f"step 0: {word}")
    if word.strip() == "":
        return ""

    # T-SQL seem to keep only the first word
    if variant == "tsql":
        word = word.split(" ", maxsplit=1)[0]

    first = word[0].strip().upper()
    logger.debug(f"step 1: {first}  ({_encode(first)})")
    encoded_word = _encode(word)
    logger.debug(f"step 2: {encoded_word}")

    soundex = ""
    for i in range(len(encoded_word)):
        n2, n1, n = last_3(encoded_word, i)
        if not (
            # if digit is any special chars, skip them
            n in {DEFAULT_CHAR, REDUCE_CHAR, DUPLICATE_CHAR}
            # if digit is repeated, skip the repeats
            or n == n1
            # if a digit is repeated with the REDUCE_CHAR as a separator (American version only)
            or (variant == "american" and n == n2 and n1 == REDUCE_CHAR)
        ):
            soundex += n

    logger.debug(f"step 3: {soundex}")
    if soundex and soundex[0] == _encode(first):
        soundex = soundex[1:]

    logger.debug(f"step 4: {soundex}")
    final = first + (soundex + "000")[:3]
    logger.debug(f"step 5: {final}")

    return final


# To match SQL Server's Transact-SQL result
def tsql_soundex(word: str) -> str:
    return _soundex(word, "tsql")


def american_soundex(word: str) -> str:
    return _soundex(word, "american")
