"""Turn raw patient text into comparable tokens.

Rules run on the normalised form, never on the raw text.
"""

import unicodedata


def _step(text: str) -> str:
    folded = unicodedata.normalize("NFKC", text).casefold()
    chars = [" " if unicodedata.category(c)[0] in "PSZC" else c for c in folded]
    return " ".join("".join(chars).split())


def normalise(text: str) -> str:
    """Return the fixed point of one normalisation step.

    Applying `normalise` twice gives the same result as once. The loop is capped so that
    hostile input cannot make it run forever.
    """
    current = text
    for _ in range(4):
        following = _step(current)
        if following == current:
            return current
        current = following
    return current


def tokens(text: str) -> tuple[str, ...]:
    return tuple(normalise(text).split())
