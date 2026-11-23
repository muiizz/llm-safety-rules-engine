import pytest

from safetyrules.lexicon import RULES
from safetyrules.rules import Level, classify


@pytest.mark.parametrize("rule", RULES, ids=[r.rule_id for r in RULES])
def test_every_phrase_is_urgent_and_names_its_rule(rule: object) -> None:
    from safetyrules.lexicon import Rule

    assert isinstance(rule, Rule)
    for phrase in rule.phrases:
        result = classify(f"hello, {phrase.upper()}!! thanks")
        assert result.level is Level.URGENT
        assert rule.rule_id in result.rule_ids


@pytest.mark.parametrize(
    "text", ["", "I had a salad for lunch", "my chest feels fine", "walked 5000 steps today"]
)
def test_routine_messages_stay_routine(text: str) -> None:
    result = classify(text)
    assert result.level is Level.ROUTINE
    assert result.rule_ids == ()


def test_phrase_must_be_contiguous_tokens() -> None:
    assert classify("pain and then chest").level is Level.ROUTINE


def test_phrase_must_match_whole_tokens() -> None:
    assert classify("seizures").level is Level.ROUTINE
    assert classify("a seizure").level is Level.URGENT


@pytest.mark.parametrize(
    "text",
    [
        "seenay mai drd hai",
        "SALAM, SAANS NAHI AA RAAAHI",
        "woh bahosh ho gaye",
        "mirgi ka daurah pada hai",
        "ضروري: سینے میں د\u200cرد ہے",
        "سينه دردَ کر رها ہے",
        "بچَے كو جھٹكے لگ رہے ہيں",
        "I can't breathe",
        "I CAN\u2019T breathe",
    ],
)
def test_spelling_and_script_variants_are_still_urgent(text: str) -> None:
    assert classify(text).level is Level.URGENT
