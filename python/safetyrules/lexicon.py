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


@dataclass(frozen=True)
class NearRule:
    """Fires when every group has a word inside one run of `window` consecutive words."""

    rule_id: str
    lang: str
    groups: tuple[tuple[str, ...], ...]
    window: int


RULES: tuple[Rule, ...] = (
    Rule("EN-CHEST", "en", ("chest pain", "pain in my chest", "chest hurts")),
    Rule(
        "EN-BREATH",
        "en",
        ("cannot breathe", "can't breathe", "cant breathe", "trouble breathing", "short of breath"),
    ),
    Rule("EN-FAINT", "en", ("passed out", "unconscious", "fainted", "not waking up")),
    Rule("EN-SEIZURE", "en", ("seizure", "having a fit", "convulsing", "convulsion")),
    Rule("EN-BLOOD", "en", ("vomiting blood", "vomited blood", "coughing up blood")),
    Rule("RU-CHEST", "ru", ("seene mein dard", "seena dard", "chhati mein dard")),
    Rule("RU-BREATH", "ru", ("saans nahi aa rahi", "saans lene mein takleef", "saans phool rahi")),
    Rule("RU-FAINT", "ru", ("behosh ho gaya", "behosh ho gaye", "behosh hain", "hosh nahi")),
    Rule("RU-SEIZURE", "ru", ("mirgi ka daura", "daura pad", "jhatkay lag")),
    Rule("RU-BLOOD", "ru", ("khoon ki ulti", "ulti mein khoon", "khaansi mein khoon")),
    Rule("UR-CHEST", "ur", ("سینے میں درد", "سینہ درد", "چھاتی میں درد")),
    Rule("UR-BREATH", "ur", ("سانس نہیں آ رہی", "سانس لینے میں تکلیف", "سانس پھول رہی")),
    Rule("UR-FAINT", "ur", ("بے ہوش ہو گیا", "بے ہوش ہو گئے", "بے ہوش ہیں", "ہوش نہیں")),
    Rule("UR-SEIZURE", "ur", ("مرگی کا دورہ", "دورہ پڑ", "جھٹکے لگ")),
    Rule("UR-BLOOD", "ur", ("خون کی الٹی", "الٹی میں خون", "کھانسی میں خون")),
)

NEAR_RULES: tuple[NearRule, ...] = (
    NearRule(
        "EN-CHEST-NEAR",
        "en",
        (("chest",), ("pain", "hurting", "hurts", "crushing", "tight")),
        5,
    ),
    NearRule(
        "EN-BREATH-NEAR",
        "en",
        (
            ("breathe", "breathing", "breath"),
            ("cannot", "cant", "hard", "hardly", "struggling", "trouble", "short", "difficulty"),
        ),
        5,
    ),
    NearRule(
        "EN-BLOOD-NEAR",
        "en",
        (("blood",), ("vomit", "vomiting", "vomited", "cough", "coughing")),
        5,
    ),
    NearRule("RU-CHEST-NEAR", "ru", (("seene", "seena", "seenay", "chhati"), ("dard", "drd")), 4),
    NearRule(
        "RU-BREATH-NEAR",
        "ru",
        (("saans", "sans"), ("nahi", "nahin", "takleef", "mushkil", "phool")),
        4,
    ),
    NearRule(
        "RU-FAINT-NEAR",
        "ru",
        (("behosh",), ("ho", "hain", "hai", "gaya", "gaye", "tha", "hui")),
        3,
    ),
    NearRule(
        "RU-SEIZURE-NEAR",
        "ru",
        (("daura", "mirgi", "jhatkay"), ("pad", "pada", "lag", "raha", "rahe")),
        4,
    ),
    NearRule("RU-BLOOD-NEAR", "ru", (("khoon",), ("ulti", "khaansi")), 4),
    NearRule("UR-CHEST-NEAR", "ur", (("سینے", "سینہ", "چھاتی"), ("درد",)), 4),
    NearRule("UR-BREATH-NEAR", "ur", (("سانس",), ("نہیں", "تکلیف", "مشکل", "پھول")), 4),
    NearRule(
        "UR-FAINT-NEAR",
        "ur",
        (("ہوش",), ("نہیں", "ہیں", "ہے", "گیا", "گئے", "تھا", "ہوئی")),
        3,
    ),
    NearRule(
        "UR-SEIZURE-NEAR",
        "ur",
        (("دورہ", "مرگی", "جھٹکے"), ("پڑ", "پڑا", "لگ", "رہا", "رہی", "رہے")),
        4,
    ),
    NearRule("UR-BLOOD-NEAR", "ur", (("خون",), ("الٹی", "کھانسی")), 4),
)
