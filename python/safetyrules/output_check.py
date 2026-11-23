"""Checks on model output. They run after the model, as a second net."""

import re

from safetyrules.normalise import normalise

SAFE_FALLBACK = "I cannot help with that here. Please talk to your care team."

_UNSAFE = (
    re.compile(r"\b\d+(\.\d+)?\s*(mg|mcg|units?|iu)\b"),
    re.compile(r"\bno need to (see|call|visit) (a|your) (doctor|nurse)\b"),
    re.compile(r"\b(stop|skip) (taking )?your (medicine|medication|insulin)\b"),
)


def check_output(text: str) -> str:
    """Return the text if it is safe, or a fixed fallback if it is not."""
    folded = normalise(text)
    if any(pattern.search(folded) for pattern in _UNSAFE):
        return SAFE_FALLBACK
    return text
