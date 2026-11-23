"""Print the round-by-round results table from the saved result files."""

import json
from pathlib import Path

RESULTS = Path(__file__).parent / "results"
ROUNDS = ("R0", "R1", "R2", "R3")


def _row(label: str) -> str:
    result = json.loads((RESULTS / f"{label}.json").read_text())["test"]
    mutation = json.loads((RESULTS / f"mutation-{label}.json").read_text())
    score = mutation["killed"] / mutation["total"]
    cells = [f"{result[lang]['urgent_recall']:.2f}" for lang in ("en", "ru", "ur")]
    missed = result["all"]["missed_urgent"]
    total = result["all"]["confusion"]["tp"] + missed
    false_urgent = result["all"]["false_urgent_rate"]
    return (
        f"| {label} | {mutation['killed']}/{mutation['total']} ({score:.2f}) "
        f"| {' | '.join(cells)} | {missed} of {total} | {false_urgent:.3f} |"
    )


def table() -> str:
    head = (
        "| Round | Mutants killed | Recall en | Recall ru | Recall ur | Missed urgent "
        "| False urgent rate |\n|---|---|---|---|---|---|---|"
    )
    return "\n".join([head, *(_row(label) for label in ROUNDS)])


if __name__ == "__main__":
    print(table())
