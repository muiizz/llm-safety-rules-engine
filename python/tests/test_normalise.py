import pytest
from hypothesis import given
from hypothesis import strategies as st

from safetyrules.normalise import normalise, plain, tokens


def test_case_punctuation_and_space() -> None:
    assert normalise("  Chest,  PAIN!! ") == "chest pain"


def test_empty() -> None:
    assert normalise("") == ""
    assert tokens("") == ()


def test_tokens() -> None:
    assert tokens("Can't breathe") == ("can", "t", "breathe")


@pytest.mark.parametrize("raw", ["ｃｈｅｓｔ　ｐａｉｎ", "chest​pain", "ﬁre"])
def test_compatibility_forms_fold(raw: str) -> None:
    assert normalise(normalise(raw)) == normalise(raw)


@given(st.text())
def test_normalise_is_idempotent(text: str) -> None:
    once = normalise(text)
    assert normalise(once) == once


def test_loop_is_capped_so_hostile_input_cannot_spin(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[str] = []

    def never_settles(text: str) -> str:
        calls.append(text)
        return text + "x"

    monkeypatch.setattr("safetyrules.normalise._step", never_settles)
    assert normalise("a") == "axxxx"
    assert len(calls) == 4


@given(st.text())
def test_plain_is_idempotent(text: str) -> None:
    once = plain(text)
    assert plain(once) == once


def test_plain_keeps_spelling() -> None:
    assert plain("No NEED to see  a doctor!") == "no need to see a doctor"
    assert normalise("No NEED to see  a doctor!") == "no ned to se a doctor"


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("saaans", "sans"),
        ("khoon kii ulti", "khon ki ulti"),
        ("seenay mai drd", "sene mein dard"),
        ("be hosh", "behosh"),
        ("BEHOSH", "behosh"),
        ("ultee", "ulti"),
        ("khun", "khon"),
        ("daurah", "daura"),
    ],
)
def test_roman_urdu_spellings_fold(raw: str, expected: str) -> None:
    assert normalise(raw) == expected


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("سينه", "سینہ"),
        ("ك", "ک"),
        ("ى", "ی"),
        ("د\u200cرد", "درد"),
        ("سَینے", "سینے"),
        ("سینے، میں\u2003درد؟", "سینے میں درد"),
    ],
)
def test_urdu_script_variants_fold(raw: str, expected: str) -> None:
    assert normalise(raw) == expected
