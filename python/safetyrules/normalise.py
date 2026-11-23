"""Turn raw patient text into comparable tokens.

Rules run on the normalised form, never on the raw text. Roman Urdu has no standard spelling and
Urdu script is often typed with Arabic letter forms and stray marks, so this step folds those.
"""

import re
import unicodedata
from collections.abc import Callable

# Arabic-script letters that keyboards produce in place of the Urdu forms.
_ARABIC_TO_URDU = str.maketrans({"ي": "ی", "ى": "ی", "ك": "ک", "ه": "ہ"})
_REPEATED_LATIN = re.compile(r"([a-z])\1+")
_BE_HOSH = re.compile(r"\bbe hosh\b")

# Common Roman Urdu spellings. Keys are folded the same way as the text, so "ultee" is stored as
# "ulte". The loop in `_fixpoint` folds the replacements again.
_ROMAN_SPELLINGS = {
    "mai": "mein",
    "main": "mein",
    "nahin": "nahi",
    "nai": "nahi",
    "drd": "dard",
    "seenay": "seene",
    "seena": "seene",
    "sine": "seene",
    "bahosh": "behosh",
    "daurah": "daura",
    "dora": "daura",
    "ultee": "ulti",
    "khun": "khoon",
}

_ROMAN_ALIASES = {_REPEATED_LATIN.sub(r"\1", k): v for k, v in _ROMAN_SPELLINGS.items()}

_DROPPED = {"Mn", "Cf"}  # combining marks (such as Urdu vowel marks) and invisible joiners


def _step(text: str) -> str:
    folded = unicodedata.normalize("NFKC", text).casefold()
    kept = "".join(c for c in folded if unicodedata.category(c) not in _DROPPED)
    spaced = "".join(" " if unicodedata.category(c)[0] in "PSZC" else c for c in kept)
    spaced = spaced.translate(_ARABIC_TO_URDU)
    spaced = _REPEATED_LATIN.sub(r"\1", spaced)
    spaced = _BE_HOSH.sub("behosh", " ".join(spaced.split()))
    return " ".join(_ROMAN_ALIASES.get(word, word) for word in spaced.split())


def _plain_step(text: str) -> str:
    folded = unicodedata.normalize("NFKC", text).casefold()
    spaced = "".join(" " if unicodedata.category(c)[0] in "PSZC" else c for c in folded)
    return " ".join(spaced.split())


def _fixpoint(step: Callable[[str], str], text: str) -> str:
    """Apply `step` until it stops changing the text. Capped so hostile input cannot spin."""
    current = text
    for _ in range(4):
        following = step(current)
        if following == current:
            return current
        current = following
    return current


def normalise(text: str) -> str:
    """Full folding for the rules: scripts, spellings, repeated letters.

    Applying `normalise` twice gives the same result as once.
    """
    return _fixpoint(_step, text)


def plain(text: str) -> str:
    """Light folding that keeps spelling intact: case, width and punctuation only.

    The output check uses this, because it matches English words as written. Folding repeated
    letters there would turn "need" into "ned" and silently break its patterns.
    """
    return _fixpoint(_plain_step, text)


def tokens(text: str) -> tuple[str, ...]:
    return tuple(normalise(text).split())
