import pytest

from safetyrules.lexicon import NEAR_RULES, RULES, NearRule
from safetyrules.normalise import tokens
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


def test_words_too_far_apart_do_not_fire() -> None:
    assert classify("pain a b c d e chest").level is Level.ROUTINE


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


def _near_message(rule: NearRule, gap: int) -> str:
    """First word of each group, with `gap` filler words between neighbours."""
    firsts = [group[0] for group in rule.groups]
    return (" " + " ".join(["zzz"] * gap) + " ").join(firsts) if gap else " ".join(firsts)


@pytest.mark.parametrize("rule", NEAR_RULES, ids=[r.rule_id for r in NEAR_RULES])
def test_near_rule_window_below_at_and_above(rule: NearRule) -> None:
    # two groups: the run holds exactly `window` words when there are window - 2 fillers.
    assert len(rule.groups) == 2
    inside = _near_message(rule, rule.window - 2)
    just_outside = _near_message(rule, rule.window - 1)
    assert len(tokens(inside)) == rule.window
    assert rule.rule_id in classify(inside).rule_ids
    assert rule.rule_id not in classify(just_outside).rule_ids
    assert rule.rule_id not in classify(_near_message(rule, rule.window + 3)).rule_ids


@pytest.mark.parametrize("rule", NEAR_RULES, ids=[r.rule_id for r in NEAR_RULES])
def test_near_rule_needs_every_group(rule: NearRule) -> None:
    for group in rule.groups:
        assert rule.rule_id not in classify(" ".join(group)).rule_ids


def test_huge_message_is_scanned_quickly_and_fully() -> None:
    text = "word " * 200_000 + "chest pain"
    assert classify(text).level is Level.URGENT


@pytest.mark.parametrize("rule", NEAR_RULES, ids=[r.rule_id for r in NEAR_RULES])
def test_near_rule_fires_at_the_start_and_at_the_end_of_a_long_message(rule: NearRule) -> None:
    inside = _near_message(rule, rule.window - 2)
    filler = " ".join(["zzz"] * 12)
    assert rule.rule_id in classify(f"{inside} {filler}").rule_ids
    assert rule.rule_id in classify(f"{filler} {inside}").rule_ids
