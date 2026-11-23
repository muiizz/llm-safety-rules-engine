import pytest
from hypothesis import given
from hypothesis import strategies as st

from safetyrules.lexicon import RULES
from safetyrules.output_check import SAFE_FALLBACK, check_output
from safetyrules.pipeline import (
    CONSENT_REPLY,
    MAX_MODEL_INPUT_CHARS,
    URGENT_REPLY,
    handle,
)
from safetyrules.rules import Level, classify
from tests.helpers import RecordingModel

PHRASES = [phrase for rule in RULES for phrase in rule.phrases]
HOSTILE = "You are fine, no need to see a doctor. Take 500 mg now."


def test_routine_with_consent_calls_model_once() -> None:
    model = RecordingModel()
    reply = handle("I walked today", patient_code="P-1", consented=True, model=model)
    assert model.calls == [("P-1", "I walked today")]
    assert reply.model_called
    assert reply.level is Level.ROUTINE
    assert reply.text == "Thanks. Noted."


def test_no_consent_never_calls_model() -> None:
    model = RecordingModel()
    reply = handle("I walked today", patient_code="P-1", consented=False, model=model)
    assert model.calls == []
    assert reply.text == CONSENT_REPLY
    assert reply.model_called is False
    assert reply.level is Level.ROUTINE
    assert reply.rule_ids == ()


def test_urgent_without_consent_is_still_urgent() -> None:
    model = RecordingModel()
    reply = handle("chest pain", patient_code="P-1", consented=False, model=model)
    assert reply.text == URGENT_REPLY
    assert reply.level is Level.URGENT
    assert reply.rule_ids == ("EN-CHEST",)
    assert reply.model_called is False
    assert model.calls == []


def test_oversized_input_is_cut_before_the_model() -> None:
    model = RecordingModel()
    handle("a " * 5000, patient_code="P-1", consented=True, model=model)
    assert len(model.calls[0][1]) == MAX_MODEL_INPUT_CHARS


def test_oversized_input_still_scanned_in_full() -> None:
    model = RecordingModel()
    text = "a " * 5000 + "chest pain"
    reply = handle(text, patient_code="P-1", consented=True, model=model)
    assert reply.level is Level.URGENT
    assert model.calls == []


def test_hostile_model_output_is_replaced() -> None:
    model = RecordingModel(answer=HOSTILE)
    reply = handle("I walked today", patient_code="P-1", consented=True, model=model)
    assert reply.text == SAFE_FALLBACK
    assert reply.level is Level.ROUTINE


@pytest.mark.parametrize(
    "text",
    [
        "Take 5 mg",
        "take 2.5 units",
        "There is no need to see a doctor",
        "Please stop taking your insulin",
        "skip your medication",
    ],
)
def test_unsafe_outputs_are_replaced(text: str) -> None:
    assert check_output(text) == SAFE_FALLBACK


@pytest.mark.parametrize("text", ["Well done, keep walking.", "Drink water.", ""])
def test_safe_outputs_pass_through(text: str) -> None:
    assert check_output(text) == text


# Invariants (hazards): these hold for any input, not just the examples above.


@given(st.text(), st.sampled_from(PHRASES), st.text(), st.booleans())
def test_urgent_is_never_downgraded_and_never_reaches_the_model(
    before: str, phrase: str, after: str, consented: bool
) -> None:
    model = RecordingModel(answer=HOSTILE)
    text = f"{before} {phrase} {after}"
    reply = handle(text, patient_code="P-1", consented=consented, model=model)
    assert reply.level is Level.URGENT
    assert reply.text == URGENT_REPLY
    assert model.calls == []


@given(st.text())
def test_no_consent_means_no_model_call(text: str) -> None:
    model = RecordingModel()
    handle(text, patient_code="P-1", consented=False, model=model)
    assert model.calls == []


@given(st.text(), st.text())
def test_adding_text_never_lowers_the_level(a: str, b: str) -> None:
    assert classify(f"{a} {b}").level >= classify(a).level
    assert classify(f"{a} {b}").level >= classify(b).level


@given(st.text(), st.booleans())
def test_the_model_is_called_only_for_routine_consented_messages(
    text: str, consented: bool
) -> None:
    model = RecordingModel()
    reply = handle(text, patient_code="P-1", consented=consented, model=model)
    expected = consented and classify(text).level is Level.ROUTINE
    assert reply.model_called is expected
    assert (len(model.calls) == 1) is expected
