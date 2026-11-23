"""Build the synthetic eval set. Deterministic: same code and seed give the same files."""

import json
import random
from pathlib import Path
from typing import TypedDict

from evals.paraphrase import paraphrase
from evals.sources import HARD_NEGATIVES, LANGS, PREFIXES, ROUTINE, SUFFIXES, URGENT

SEED = "portfolio-v1"
VARIANTS_PER_BASE = 2  # each base message appears once as written, plus this many noisy copies
DATA_DIR = Path(__file__).parent / "data"


class Case(TypedDict):
    id: str
    lang: str
    text: str
    label: str  # "urgent" or "routine"
    kind: str  # "urgent", "routine", "hard_negative"
    base: str
    variant: int
    split: str  # "dev" or "test"


def _frame(text: str, lang: str, rng: random.Random) -> str:
    return rng.choice(PREFIXES[lang]) + text + rng.choice(SUFFIXES[lang])


def _bases() -> list[tuple[str, str, str, str, str]]:
    """(base_id, lang, text, kind, split) for every base message."""
    out: list[tuple[str, str, str, str, str]] = []
    for concept, by_lang in URGENT.items():
        for lang in LANGS:
            for i, text in enumerate(by_lang[lang]):
                split = "dev" if i % 2 == 0 else "test"
                out.append((f"u-{concept}-{lang}-{i}", lang, text, "urgent", split))
    for lang in LANGS:
        for i, text in enumerate(ROUTINE[lang]):
            out.append((f"r-{lang}-{i}", lang, text, "routine", "dev" if i % 2 == 0 else "test"))
        for i, text in enumerate(HARD_NEGATIVES[lang]):
            out.append(
                (f"h-{lang}-{i}", lang, text, "hard_negative", "dev" if i % 2 == 0 else "test")
            )
    return out


def build() -> list[Case]:
    cases: list[Case] = []
    for base_id, lang, text, kind, split in _bases():
        rng = random.Random(f"{SEED}:{base_id}")
        framed = _frame(text, lang, rng)
        label = "urgent" if kind == "urgent" else "routine"
        for variant in range(VARIANTS_PER_BASE + 1):
            body = (
                framed if variant == 0 else paraphrase(framed, lang, f"{SEED}:{base_id}:{variant}")
            )
            cases.append(
                {
                    "id": f"{base_id}-v{variant}",
                    "lang": lang,
                    "text": body,
                    "label": label,
                    "kind": kind,
                    "base": base_id,
                    "variant": variant,
                    "split": split,
                }
            )
    return cases


def dump(cases: list[Case], split: str) -> str:
    rows = [json.dumps(c, ensure_ascii=False, sort_keys=True) for c in cases if c["split"] == split]
    return "\n".join(rows) + "\n"


def main() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    cases = build()
    for split in ("dev", "test"):
        (DATA_DIR / f"{split}.jsonl").write_text(dump(cases, split), encoding="utf-8")
    print(f"wrote {len(cases)} cases to {DATA_DIR}")


if __name__ == "__main__":
    main()
