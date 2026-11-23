"""Deterministic urgent detection. No model is involved."""

from dataclasses import dataclass
from enum import IntEnum

from safetyrules.lexicon import RULES
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


def classify(text: str) -> Classification:
    words = tokens(text)
    hits = tuple(
        rule_id
        for rule_id, phrases in _COMPILED
        if any(_contains(words, phrase) for phrase in phrases)
    )
    return Classification(Level.URGENT if hits else Level.ROUTINE, hits)
