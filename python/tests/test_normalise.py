import pytest
from hypothesis import given
from hypothesis import strategies as st

from safetyrules.normalise import normalise, tokens


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
