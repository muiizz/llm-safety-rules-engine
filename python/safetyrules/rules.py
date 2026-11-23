"""Deterministic urgent detection. No model is involved."""

from dataclasses import dataclass
from enum import IntEnum

from safetyrules.lexicon import NEAR_RULES, RULES
from safetyrules.normalise import tokens


class Level(IntEnum):
    ROUTINE = 0
    URGENT = 1


@dataclass(frozen=True)
class Classification:
    level: Level
    rule_ids: tuple[str, ...]


def _contains(haystack: tuple[str, ...], needle: tuple[str, ...]) -> bool:
    """True if `needle` appears as whole, consecutive tokens inside `haystack`."""
    return f" {' '.join(needle)} " in f" {' '.join(haystack)} "


_COMPILED = tuple(
    (rule.rule_id, tuple(tokens(phrase) for phrase in rule.phrases)) for rule in RULES
)


_COMPILED_NEAR = tuple(
    (
        rule.rule_id,
        tuple(frozenset(tok for word in group for tok in tokens(word)) for group in rule.groups),
        rule.window,
    )
    for rule in NEAR_RULES
)


def _near(words: tuple[str, ...], groups: tuple[frozenset[str], ...], window: int) -> bool:
    """True if some run of `window` consecutive words holds a word from every group."""
    for start in range(max(1, len(words) - window + 1)):
        seen = set(words[start : start + window])
        if all(not seen.isdisjoint(group) for group in groups):
            return True
    return False


def classify(text: str) -> Classification:
    words = tokens(text)
    hits = tuple(
        rule_id
        for rule_id, phrases in _COMPILED
        if any(_contains(words, phrase) for phrase in phrases)
    )
    near_hits = tuple(
        rule_id for rule_id, groups, window in _COMPILED_NEAR if _near(words, groups, window)
    )
    all_hits = hits + near_hits
    return Classification(Level.URGENT if all_hits else Level.ROUTINE, all_hits)
