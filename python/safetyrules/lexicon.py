"""The toy lexicon. Every phrase here is invented for this teaching repo.

Nothing here comes from a real clinical system. TODO(Muizz): a native reader should check the
Roman Urdu and Urdu script entries before any number is called hand checked.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Rule:
    rule_id: str
    lang: str
    phrases: tuple[str, ...]


RULES: tuple[Rule, ...] = (
    Rule("EN-CHEST", "en", ("chest pain", "pain in my chest", "chest hurts")),
    Rule(
        "EN-BREATH",
        "en",
        ("cannot breathe", "can't breathe", "cant breathe", "trouble breathing", "short of breath"),
    ),
    Rule("EN-FAINT", "en", ("passed out", "unconscious", "fainted", "not waking up")),
    Rule("EN-SEIZURE", "en", ("seizure", "having a fit")),
    Rule("EN-BLOOD", "en", ("vomiting blood", "vomited blood", "coughing up blood")),
)
