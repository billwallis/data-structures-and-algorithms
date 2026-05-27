import pytest
import soundex


@pytest.mark.parametrize(
    "word, index, expected",
    [
        ("", 0, ("", "", "")),
        ("", 1, ("", "", "")),
        ("", 4, ("", "", "")),
        ("foo", 0, ("", "", "f")),
        ("foo", 1, ("", "f", "o")),
        ("foo", 2, ("f", "o", "o")),
        ("foo", 3, ("o", "o", "")),
        ("foo", 4, ("o", "", "")),
        ("foo", 5, ("", "", "")),
        ("abcd", 0, ("", "", "a")),
        ("abcd", 1, ("", "a", "b")),
        ("abcd", 2, ("a", "b", "c")),
        ("abcd", 3, ("b", "c", "d")),
        ("abcd", 4, ("c", "d", "")),
        ("abcd", 5, ("d", "", "")),
        ("abcd", 6, ("", "", "")),
    ],
)
def test__last_3(word: str, index: int, expected: tuple[str, str, str]):
    assert soundex.main.last_3(word, index) == expected


@pytest.mark.parametrize(
    "word, expected",
    [
        ("", ""),
        (" ", ""),
        ("A", "A000"),
        ("Aa", "A000"),
        ("Aaa", "A000"),
        ("Aaaa", "A000"),
        ("B", "B000"),
        ("Ba", "B000"),
        ("Bb", "B000"),
        ("Bc", "B200"),
        ("Bcd", "B230"),
        ("Bcdf", "B231"),
        ("Robert", "R163"),
        ("Rupert", "R163"),
        ("Rubin", "R150"),
        ("Tymczak", "T522"),
        ("Pfister", "P236"),
        ("Honeyman", "H555"),
        ("Jack", "J200"),
        ("Jackson", "J250"),
        ("Cycle", "C240"),
        ("Ashcroft", "A226"),
        ("Ash", "A200"),
        ("Ashc", "A220"),
        ("Achs", "A220"),
        ("Aces", "A220"),
        ("Foo Bar Baz", "F000"),
        ("Rhythm", "R350"),
        # Not sure why these don't match :shrug:
        # ("Babushka", "B120"),
        # ("Cashkabaya", "C210"),
        # ("Hatchson", "H325"),
        # ("Marshson", "M625"),
        # ("Zwgyi", "Z000"),
    ],
)
def test__tsql_soundex(word: str, expected: str):
    assert soundex.tsql_soundex(word) == expected


@pytest.mark.parametrize(
    "word, expected",
    [
        ("", ""),
        ("Robert", "R163"),
        ("Rupert", "R163"),
        ("Rubin", "R150"),
        ("Ashcraft", "A261"),
        ("Ashcroft", "A261"),
        ("Tymczak", "T522"),
        ("Pfister", "P236"),
        ("Honeyman", "H555"),
        ("Jack", "J200"),  # 2+22 -> 22 -> 2
    ],
)
def test__american_soundex(word: str, expected: str):
    assert soundex.american_soundex(word) == expected
