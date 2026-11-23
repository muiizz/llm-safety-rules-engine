"""Seeded paraphrase generator: spelling and script noise a real patient might produce."""

import random

# Roman Urdu has no standard spelling. These are common alternatives.
ROMAN_VARIANTS: dict[str, tuple[str, ...]] = {
    "saans": ("sans", "saans", "sanss"),
    "seene": ("seenay", "seena", "sine"),
    "behosh": ("be hosh", "bahosh", "behosh"),
    "daura": ("daurah", "dora", "daura"),
    "khoon": ("khun", "khoon", "khoon"),
    "mein": ("mai", "main", "mein"),
    "nahi": ("nahin", "nai", "nahi"),
    "dard": ("dard", "drd", "dard"),
    "ulti": ("ulti", "ultee", "ulti"),
}
# Arabic-script letters that keyboards produce in place of the Urdu forms.
URDU_VARIANTS = {"ی": "ي", "ک": "ك", "ہ": "ه"}
TASHKEEL = "َ"  # fatha, a mark many keyboards add
ZWNJ = "‌"
LATIN_VOWELS = "aeiou"


def _stretch(word: str, rng: random.Random) -> str:
    spots = [i for i, ch in enumerate(word) if ch in LATIN_VOWELS]
    if not spots:
        return word
    i = rng.choice(spots)
    return word[:i] + word[i] * rng.choice((2, 3)) + word[i + 1 :]


def _latin(text: str, lang: str, rng: random.Random) -> str:
    words = text.split(" ")
    out: list[str] = []
    for word in words:
        if lang == "ru" and word in ROMAN_VARIANTS and rng.random() < 0.7:
            out.append(rng.choice(ROMAN_VARIANTS[word]))
        elif lang == "en" and word == "can't" and rng.random() < 0.7:
            out.append("cant")
        elif rng.random() < 0.15:
            out.append(_stretch(word, rng))
        else:
            out.append(word)
    result = " ".join(out)
    return result.upper() if rng.random() < 0.15 else result


def _urdu(text: str, rng: random.Random) -> str:
    out: list[str] = []
    for ch in text:
        if ch in URDU_VARIANTS and rng.random() < 0.5:
            out.append(URDU_VARIANTS[ch])
        else:
            out.append(ch)
        if "؀" <= ch <= "ۿ" and rng.random() < 0.08:
            out.append(rng.choice((TASHKEEL, ZWNJ)))
    return "".join(out)


def paraphrase(text: str, lang: str, seed: str) -> str:
    """Return one noisy variant. The same (text, lang, seed) always gives the same result."""
    rng = random.Random(seed)
    noisy = _urdu(text, rng) if lang == "ur" else _latin(text, lang, rng)
    return noisy + rng.choice(("", "", "!", "!!", "...", "?"))
