"""Confusion counts and rates, per language and overall."""

from collections.abc import Callable
from typing import Any

from evals.sources import LANGS


def score(
    cases: list[dict[str, str]], predict: Callable[[str], bool], *, list_misses: bool
) -> dict[str, Any]:
    """`predict(text)` returns True when the engine says urgent."""
    groups: dict[str, list[dict[str, str]]] = {lang: [] for lang in LANGS}
    for case in cases:
        groups[case["lang"]].append(case)
    out: dict[str, Any] = {}
    for name, group in [*groups.items(), ("all", cases)]:
        tp = fn = fp = tn = hard_fp = hard_n = 0
        missed: list[str] = []
        for case in group:
            said_urgent = predict(case["text"])
            if case["label"] == "urgent":
                if said_urgent:
                    tp += 1
                else:
                    fn += 1
                    missed.append(case["id"])
            else:
                if case["kind"] == "hard_negative":
                    hard_n += 1
                    hard_fp += int(said_urgent)
                if said_urgent:
                    fp += 1
                else:
                    tn += 1
        urgent_n = tp + fn
        routine_n = fp + tn
        row: dict[str, Any] = {
            "confusion": {"tp": tp, "fn": fn, "fp": fp, "tn": tn},
            "urgent_recall": round(tp / urgent_n, 4) if urgent_n else None,
            "missed_urgent": fn,
            "false_urgent_rate": round(fp / routine_n, 4) if routine_n else None,
            "false_urgent_on_hard_negatives": f"{hard_fp}/{hard_n}",
        }
        if list_misses:
            row["missed_ids"] = missed
        out[name] = row
    return out


def table(result: dict[str, Any]) -> str:
    lines = [
        "| lang | urgent recall | missed urgent | false urgent rate | hard negatives wrongly urgent"
        " |",
        "|---|---|---|---|---|",
    ]
    for name, row in result.items():
        c = row["confusion"]
        lines.append(
            f"| {name} | {row['urgent_recall']} | {row['missed_urgent']} of {c['tp'] + c['fn']} "
            f"| {row['false_urgent_rate']} | {row['false_urgent_on_hard_negatives']} |"
        )
    return "\n".join(lines)
